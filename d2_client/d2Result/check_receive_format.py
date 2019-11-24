from conf.code_msg import CODE_MSG_DICT
from tools.filtering_char import automatic_filtering_invisible_char
import datetime
from check_data.check_field import CheckField


class CheckReceiveFormat(object):

    def __init__(self):
        self.code_msg = CODE_MSG_DICT
        self.check_file = CheckField.instance()

    def is_initialization(self, obj):
        """
        初始化检查，是否为合法的数据格式
        {
            "orderId": 0  # int
        }
        :param obj: dict
        :return: 如果成功则返回标准数据格式, 否则返回错误信息
        """
        ret_data = {}
        temp = self.check_file.is_order_id(obj.get('orderId'))
        # 如果
        if temp[0] % 20 == 0:
            ret_data['orderId'] = temp[2]
            return True, ret_data
        else:
            return False, temp[0], temp[1]

    def check_period(self, obj, time_interval):
        """
        # 周期检查
        :param obj: 字典，包含起始时间和结束时间
                    {
                        "beginTime": "2019-11-8 15:20",
                        "endTime":  "2019-11-9 15:20"
                    }
        :param time_interval:  1,2,3  天
        :return:  (code, msg, [dict])
        """
        begin_time = self.check_file.is_time_str(obj.get('beginTime'))
        end_time = self.check_file.is_time_str(obj.get('endTime'))
        if begin_time[0] % 20 == 0 and end_time[0] % 20 == 0:
            a = begin_time[2]
            b = end_time[2]
            if a > b:
                a, b = b, a
            time_interval = datetime.timedelta(days=time_interval)
            # 开始时间和结束时间差与给定时间周期不吻合
            if a + time_interval != b:
                return 204, self.code_msg['204']
            else:
                return 200, 200, {'beginTime': a, 'endTime': b}
        else:
            # 如果时间存在问题
            if begin_time[0] % 20 != 0:
                return begin_time
            else:
                return end_time

    def check_source(self, obj):
        """
        检查来源
        :param obj:
        :return:
        """
        is_all = obj.get('isAll')
        count = obj.get('count')
        source_list = obj.get('list')

        # 如果是全选，那么就不去查看其它参数
        if is_all is not None and isinstance(is_all, int) and is_all == 1:
            return 220, 220, {'isAll': is_all, 'count': count, 'list': source_list}

        # 空检查
        if is_all is None or count is None or source_list is None:
            return 221, self.code_msg['221'].format('来源')
        # 类型检查
        if not isinstance(is_all, int) and not isinstance(count, int) and not isinstance(source_list, list):
            return 222, self.code_msg['222'].format('来源')
        # 列表里面仔细检查，如果存在空串，则去除，最后count,以最后列表长度为标准
        s_list = []
        for source in source_list:
            if not isinstance(source, str):
                return 222, self.code_msg['222'].format('来源')
            source = automatic_filtering_invisible_char(source)
            if len(source) > 0:
                s_list.append(source)
        count = len(s_list)
        return 220, 220, {'isAll': is_all, 'count': count, 'list': s_list}

    def check_word(self, obj):
        """
        暂时引用了 来源检查函数
        :param obj:
        :return:
        """
        temp = self.check_source(obj)
        if temp[0] % 20 == 0:
            return temp
        else:
            return temp[0], self.code_msg[temp[0]].format('检测词')

    def is_survey_trend(self, obj):
        """
        {
            "orderId": 0,
            "data": {
                "timeInterval" : 1,  
                "thisPeriod": {   
                    "beginTime": "2019-11-8 15:20", 
                    "endTime":  "2019-11-9  15:20"  
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
        :return: 
        """
        ret_data = {}
        # 订单编号检查
        order_id = self.check_file.is_order_id(obj.get('orderId'))
        if order_id[0] % 20 == 0:
            ret_data['orderId'] = order_id[2]
        else:
            return False, order_id[0], order_id[1]
        # 周期间隔检查
        data = obj.get('data')
        if data is None:
            return False, 223, self.code_msg['223']
        if not isinstance(data, dict):
            return False, 224, self.code_msg['224']
        obj = data
        time_interval = self.check_file.is_time_interval(obj.get('timeInterval'))
        if time_interval[0] % 20 == 0:
            ret_data['timeInterval'] = time_interval[2]
        else:
            return False, time_interval[0], time_interval[1]

        # 周期检查
        period = self.check_period(obj.get('thisPeriod'), time_interval[2])
        if period[0] % 20 == 0:
            ret_data['thisPeriod'] = period[2]
        else:
            return False, period[0], period[1]

        # 来源检查
        source = self.check_source(obj.get('source'))
        if source[0] % 20 == 0:
            ret_data['source'] = source[2]
        else:
            return False, source[0], source[1]

        # 检测词检测
        word = self.check_word(obj.get('word'))
        if word[0] % 20 == 0:
            ret_data['word'] = word[2]
        else:
            return False, word[0], word[1]
        return True, ret_data
