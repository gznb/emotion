from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from rest_framework.views import APIView
from d2Result.surveyViews.utils.check_and_aggregate import CheckAndAggregate
from d2Result.models import d2ResultModel
import datetime
from conf.time_conf import DATETIME_FORMAT_STR
from pymongo_aggregate.aggregate_rule import AggregateRule
import logging
logger = logging.getLogger('django')

class SpecificView(APIView):

    def post(self, request, *args, **kwargs):

        check_and_aggregate = CheckAndAggregate()
        rules = AggregateRule()
        get_data = check_and_aggregate.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            base_aggreate = check_and_aggregate.init_aggregate_rules(get_data)
            if get_data['data']['source']['isAll'] == 1:
                base_aggreate.append(rules.look_up_role('d2_spider_model', 'GspiderId', 'GspiderId', 'spider'))
            base_aggreate.append(rules.equal_rule('GresultAttribute', '负面'))
            # print(base_aggreate)
            base_res_list = d2ResultModel._get_collection().aggregate(base_aggreate)

            con_list = list()
            for res in base_res_list:
                d = {
                    'time': res['GresultReleaseTime'].strftime(DATETIME_FORMAT_STR),
                    'title': res['GresultTitle'].strip(),
                    'url': res['GresultRealUrl'],
                    'score': res['GresultScore'],
                    'source': res['spider'][0]['GspiderClassification']
                }
                con_list.append(d)

            return JsonResponse({'code': 0, 'msg': '成功', 'data': {'count':len(con_list), 'list': con_list}})
