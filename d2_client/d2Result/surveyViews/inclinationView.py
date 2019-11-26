from django.http import JsonResponse,  HttpResponseServerError
from rest_framework.views import APIView
from d2Result.surveyViews.utils.check_and_aggregate import CheckAndAggregate
from d2Result.models import d2ResultModel
from pymongo_aggregate.aggregate_rule import AggregateRule
import logging
logger = logging.getLogger('django')


class InclinaView(APIView):

    def post(self, request, *args, **kwargs):
        check_and_aggregate = CheckAndAggregate()
        get_data = check_and_aggregate.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            rules = AggregateRule()
            a = check_and_aggregate.init_aggregate_rules(get_data, is_old=True)
            begin_time = get_data['data']['thisPeriod']['beginTime']
            end_time = get_data['data']['thisPeriod']['endTime']
            old_time = begin_time - (end_time-begin_time)
            get_data['data']['thisPeriod']['beginTime'] = old_time
            get_data['data']['thisPeriod']['endTime'] = begin_time
            b = check_and_aggregate.init_aggregate_rules(get_data, is_old=True)
            a.append(rules.sort_by_count('GresultAttribute'))
            b.append(rules.sort_by_count('GresultAttribute'))
            try:
                res_list_a = d2ResultModel._get_collection().aggregate(a)
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError()
            this_period = {'positive':0, 'negative':0, 'neutral':0}
            last_period = {'positive':0, 'negative':0, 'neutral':0}
            for res in res_list_a:
                # print(res['_id'])
                if res['_id'] == "正面":
                    this_period['positive'] = res['count']
                elif res['_id'] == '中性':
                    this_period['neutral'] = res['count']
                else:
                    this_period['negative'] = res['count']
            try:
                res_list_b = d2ResultModel._get_collection().aggregate(b)
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError()
            for res in res_list_b:
                if res['_id'] == "正面":
                    last_period['positive'] = res['count']
                elif res['_id'] == '中性':
                    last_period['neutral'] = res['count']
                else:
                    last_period['negative'] = res['count']
            return JsonResponse({'code': 0, 'msg': '成功', 'data':{'thisPeriod':this_period, 'lastPeriod':last_period}})
