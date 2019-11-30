from django.http import JsonResponse, HttpResponseServerError
from d2Result.utils.check_get_data import CheckReceiveFormat
from rest_framework.views import APIView
from pymongo_aggregate.aggregate_rule import AggregateRule
from d2Result.models import d2ResultModel
from conf.field_conf import SEARCH_DICT
import logging
logger = logging.getLogger('django')


class DetailedView(APIView):

    def __init__(self):
        self.aggregate_rules = []
        self.p_pos = 1
        self.p_count = 1
        super().__init__()

    # 检查格式并整合查询语句
    def check_format(self, request):
        order_id = request.data.get('orderId')
        data = request.data.get('data')
        this_period = data.get('thisPeriod')
        source = data.get('source')
        word = data.get('word')
        page = data.get('page')
        search = data.get('search')
        attribute = data.get('attribute')
        check = CheckReceiveFormat()
        try:
            order_id = check.check_order_id({'orderId': order_id})

            begin_time, end_time = check.check_period(this_period)

            s_is_all, s_count, s_list = check.check_source(source)

            w_is_all, w_count, w_list = check.check_word(word)

            p_pos, p_count = check.check_page(page)
            self.p_pos = p_pos
            self.p_count = p_count
            is_default, key, value = check.check_search(search)
            attribute_is_default, attribute_value = check.check_attribute_search(attribute)
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 2, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            rules = AggregateRule()
            self.aggregate_rules.append(rules.equal_rule('GorderId', order_id))
            # 将属性判断加在前面
            if attribute_is_default != 1:
                # print(attribute_value)
                # print(111)
                self.aggregate_rules.append(rules.equal_rule("GresultAttribute", attribute_value))
            self.aggregate_rules.append(rules.time_interval_rule('GresultReleaseTime', begin_time, end_time))
            if w_is_all != 1:
                self.aggregate_rules.append(rules.list_in_rule('GresultKeyword', w_list))
            self.aggregate_rules.append(rules.look_up_role('d2_spider_model','GspiderId', 'GspiderId', 'spider'))
            if s_is_all != 1:
                self.aggregate_rules.append(rules.list_in_rule('spider.GspiderClassification', s_list))
            self.aggregate_rules = self.aggregate_rules + rules.skip_limit(p_pos, p_count)
            # print(is_default)
            if is_default != 1:
                if '渠道' in key:
                    key = 'spider.' + SEARCH_DICT[key]
                else:
                    # print(key)
                    key = SEARCH_DICT[key]
                self.aggregate_rules.append(rules.re_rule(key, value))

    def get_rev_data(self, res_list):
        rev_data = {'code': 0, 'msg': '成功','data': {'page': {'position':self.p_pos, 'count': self.p_count}}}
        total = 0
        result_list = []
        for res in res_list:
            total += 1
            dd = {
                'url': res['GresultRealUrl'],
                'title': res['GresultTitle'].strip(),
                'attribute': res['GresultAttribute'],
                'channel': res['spider'][0]['GspiderClassification'],
                'content': res['GresultDetailedInformating'].strip() if res['GresultDetailedInformating'] else "此渠道不包括正文",
                'crowTime': res['GresultNowTime'],
                'releaseTime': res['GresultReleaseTime'],
                'keyword': res['GresultKeyword']
            }
            result_list.append(dd)
        # rev_data['page']['count'] = min(rev_data['page']['count'], total)
        rev_data['data']['total'] = total
        rev_data['data']['list'] = result_list
        return rev_data

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            # pprint.pprint(self.aggregate_rules)
            res_list = d2ResultModel._get_collection().aggregate(self.aggregate_rules)
            rev_data = self.get_rev_data(res_list)
        return JsonResponse(rev_data)
