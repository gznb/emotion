from d2Result.utils.check_get_data import CheckReceiveFormat
from django.http import JsonResponse, HttpResponseServerError
from pymongo_aggregate.aggregate_rule import AggregateRule
import traceback
import logging
logger = logging.getLogger('django')


class CheckAndAggregate(object):

    def __init__(self):
        self.check = CheckReceiveFormat()
        self.rules = AggregateRule()

    # 具体的检查数据见下面详细说明
    def check_format(self, request):
        """
                {
            "orderId": 2,
            "data": {
                "timeInterval" : 1,
                "thisPeriod": {
                    "beginTime": "2019-11-19 11:12:44",
                    "endTime":   "2019-11-20 11:12:44"
                },
                "source": {
                    "isAll": 1,
                    "count": 4,
                    "list": ["搜索引擎", "报纸", "贴吧", "论坛"]
                },
                "word": {
                    "isAll": 1,
                    "count": 2,
                    "list": ["太平洋集团", "严介和"]
                },
                "sort": 'time | score'
            }
        }
        :param request:
        :return:
        """
        order_id = request.data.get('orderId')
        data = request.data['data']
        time_interval = data.get('timeInterval')
        this_period = data.get('thisPeriod')
        source = data.get('source')
        word = data.get('word')
        sort_rule = data.get('sort')
        try:
            order_id = self.check.check_order_id({'orderId': order_id})
            time_interval = self.check.check_time_interval({'timeInterval': time_interval})
            begin_time, end_time = self.check.check_period(this_period, time_interval)
            s_is_all, s_count, s_list = self.check.check_source(source)
            w_is_all, w_count, w_list = self.check.check_word(word)
            if sort_rule is not None:
                sort_rule = self.check.check_sort_rule({'sort': sort_rule})
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 2, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            get_data = dict()
            data = dict()
            get_data['orderId'] = order_id
            data['timeInterval'] = time_interval
            data['thisPeriod'] = {
                'beginTime': begin_time,
                'endTime': end_time
            }
            data['word'] = {
                'isAll': w_is_all,
                'count': w_count,
                'list': w_list,
            }
            data['source'] = {
                'isAll': s_is_all,
                'count': s_count,
                'list': s_list
            }
            if sort_rule is not None:
                data['sort'] = sort_rule
            get_data['data'] = data
            return get_data

    # 具体查询数据见下面详细说明
    def init_aggregate_rules(self, get_data, is_old=False):
        """
        {
            "orderId": 2,
            "data": {
                "timeInterval" : 1,
                "thisPeriod": {
                    "beginTime": "2019-11-19 11:12:44",
                    "endTime":   "2019-11-20 11:12:44"
                },
                "source": {
                    "isAll": 1,
                    "count": 4,
                    "list": ["搜索引擎", "报纸", "贴吧", "论坛"]
                },
                "word": {
                    "isAll": 1,
                    "count": 2,
                    "list": ["太平洋集团", "严介和"]
                }
            }
        }
        :param get_data:
        :return:
        """
        aggregate_rules = []
        order_id = get_data['orderId']
        aggregate_rules.append(self.rules.equal_rule('GorderId', order_id))
        data = get_data['data']
        begin_time = data['thisPeriod']['beginTime']
        end_time = data['thisPeriod']['endTime']
        if is_old:
            old_time = begin_time - (end_time - begin_time)
            aggregate_rules.append(self.rules.time_interval_rule('GresultReleaseTime', old_time, end_time))
        else:
            aggregate_rules.append(self.rules.time_interval_rule('GresultReleaseTime', begin_time, end_time))
        w_is_all = data['word']['isAll']
        if w_is_all != 1:
            w_list = data['word']['list']
            aggregate_rules.append(self.rules.list_in_rule('GresultKeyword', w_list))
        s_is_all = data['source']['isAll']
        if s_is_all != 1:
            s_list = data['source']['list']
            aggregate_rules.append(self.rules.look_up_role('d2_spider_model', 'GspiderId', 'GspiderId', 'spider'))
            aggregate_rules.append(self.rules.list_in_rule('spider.GspiderClassification', s_list))
        return aggregate_rules
