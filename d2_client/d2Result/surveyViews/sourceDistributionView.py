from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from rest_framework.views import APIView
from d2Result.surveyViews.utils.check_and_aggregate import CheckAndAggregate
from d2Result.models import d2ResultModel
import copy
from pymongo_aggregate.aggregate_rule import AggregateRule
import logging
logger = logging.getLogger('django')


class SourceDistributeView(APIView):
    def post(self, request, *args, **kwargs):
        check_and_aggregate = CheckAndAggregate()
        rules = AggregateRule()
        get_data = check_and_aggregate.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            # 所有
            base_aggreate = check_and_aggregate.init_aggregate_rules(get_data)
            # 都需要先连表
            if get_data['data']['source']['isAll'] == 1:
                base_aggreate.append(rules.look_up_role('d2_spider_model', 'GspiderId', 'GspiderId', 'spider'))
            # a_aggreate 负面
            a_aggreate = copy.deepcopy(base_aggreate)
            # 正面
            b_aggreate = copy.deepcopy(base_aggreate)

            base_aggreate.append(rules.sort_by_count('spider.GspiderClassification'))
            base_res_list = d2ResultModel._get_collection().aggregate(base_aggreate)

            a_aggreate.append(rules.equal_rule('GresultAttribute', '负面'))
            a_aggreate.append(rules.sort_by_count('spider.GspiderClassification'))
            a_res_list = d2ResultModel._get_collection().aggregate(a_aggreate)

            b_aggreate.append(rules.equal_rule('GresultAttribute','正面'))
            b_aggreate.append(rules.sort_by_count('spider.GspiderClassification'))
            b_res_list = d2ResultModel._get_collection().aggregate(b_aggreate)
            count = 0
            channel = dict()
            for res in base_res_list:
                count += 1
                key = res['_id'][0]

                channel[key] = {'total':0, 'positive': 0, 'negative': 0, 'neutral': 0}
                channel[key]['name'] = key
                channel[key]['total'] = res['count']
            for res in a_res_list:
                key = res['_id'][0]
                channel[key]['negative'] = res['count']

            for res in b_res_list:
                key = res['_id'][0]
                channel[key]['positive'] = res['positive']
            channel_list = []
            for k, v in channel.items():
                v['neutral'] = v['total'] - v['negative'] - v['positive']
                channel_list.append(v)
            return JsonResponse({'code': 0, 'msg': '成功', 'data': {'count':len(channel_list), 'list': channel_list}})
