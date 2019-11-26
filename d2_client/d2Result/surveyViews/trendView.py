from django.http import JsonResponse,  HttpResponseServerError, HttpResponseNotFound
from d2Result.models import d2ResultModel
from rest_framework.views import APIView
from d2Result.surveyViews.utils.check_and_aggregate import CheckAndAggregate
from pymongo_aggregate.aggregate_rule import AggregateRule
import datetime
import logging
import copy
logger = logging.getLogger('django')

class TrendView(APIView):
    aggregate_rules = []
    data_table = list()
    rules = AggregateRule()
    # 初始化时间周期表中的 time
    def init_time_table(self, time_interval, old_time):
        data_table = list()
        if time_interval == 1:
            for i in range(24):
                r = datetime.timedelta(days=1, hours=i)

                t = old_time + r
                data_table.append({
                    'time': t.strftime('%Y-%m-%d %H:%M:%S'),
                    'thisInfoCounts': 0,
                    'thisNegativeCounts': 0,
                    'lastInfoCounts': 0,
                    'lastNegativeCounts': 0
                })
        else:
            for i in range(time_interval):
                r = datetime.timedelta(days=i+time_interval)
                t = old_time + r
                data_table.append({
                    'time': t.strftime('%Y-%m-%d'),
                    'thisInfoCounts': 0,
                    'thisNegativeCounts': 0,
                    'lastInfoCounts': 0,
                    'lastNegativeCounts': 0
                })

        self.data_table = data_table

    def cal_date_table(self, aggregate_rules, this_counts, last_counts, old_time, time_interval):
        # print(aggregate_rules)
        # 如果是以一天为周期，则是  24小时
        b = 24
        time_seconds = 60 * 60
        if time_interval > 1:
            b = time_interval
        data_table = copy.deepcopy(self.data_table)
        # data_table = self.data_table
        res_list = d2ResultModel._get_collection().aggregate(aggregate_rules)
        for res in res_list:
            # 时间差 = 当前时间 - 最早时间 old_time
            # print(1)
            now_time = res['now_time']

            time_diff = now_time - old_time
            # print(time_diff)
            if time_interval == 1:
                a = time_diff.seconds // time_seconds
                # 日期天数不会被计算在秒中
                a += 24*time_diff.days
            else:
                a = time_diff.days
            if a >= b:
                # print(a, b, a - b)
                data_table[a - b][this_counts] += res['count']
            else:
                # print(a, b)
                data_table[a][last_counts] += res['count']
            self.data_table = data_table

    def get_periodic_table(self, get_data, init_aggregate_rules):
        aggregate_rules = copy.deepcopy(init_aggregate_rules)
        time_interval = get_data['data']['timeInterval']
        begin_time = get_data['data']['thisPeriod']['beginTime']
        end_time = get_data['data']['thisPeriod']['endTime']
        old_time = begin_time - (end_time - begin_time)
        aggregate_rules.append(self.rules.my_sort('GresultReleaseTime', -1))
        self.init_time_table(time_interval, old_time)
        # 判断周期间隔
        if time_interval == 1:
            time_format = '%Y-%m-%d %H'
        else:
            time_format = '%Y-%m-%d'
        # 计算总体
        aggregate_rules.append(self.rules.time_group(time_format, 'GresultReleaseTime'))
        self.cal_date_table(aggregate_rules, 'thisInfoCounts', 'lastInfoCounts', old_time, time_interval)
        # 计算负面
        aggregate_rules = copy.deepcopy(init_aggregate_rules)
        aggregate_rules.append(self.rules.equal_rule('GresultAttribute', '负面'))
        aggregate_rules.append(self.rules.time_group(time_format, 'GresultReleaseTime'))
        self.cal_date_table(aggregate_rules, 'thisNegativeCounts', 'lastNegativeCounts', old_time, time_interval)

    def post(self, request, *args, **kwargs):
        check_and_aggregate = CheckAndAggregate()
        get_data = check_and_aggregate.check_format(request)
        # print(11)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:

            aggregate_rules = check_and_aggregate.init_aggregate_rules(get_data,is_old=True)
            # print(222)
            # print(aggregate_rules)
            # print(11)
            self.get_periodic_table(get_data, aggregate_rules)
            # print('-'*30)
            # print(self.data_table)
            return JsonResponse({'code': 0, 'msg': '成功', 'data': {'count': len(self.data_table), 'list': self.data_table}})
