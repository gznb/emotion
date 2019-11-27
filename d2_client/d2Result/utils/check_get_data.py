from conf.code_msg import CODE_MSG_DICT
from tools.filtering_char import automatic_filtering_invisible_char
from check_data.check_field import CheckField
import datetime
import logging
logger = logging.getLogger('django')

class CheckReceiveFormat(object):

    def __init__(self):
        self.code_msg = CODE_MSG_DICT
        self.check_file = CheckField.instance()

    # 正确后返回  order_id
    def check_order_id(self, obj):
        """
        初始化检查，是否为合法的数据格式
        {
            "orderId": 0  # int
        }
        :param obj: dict
        :return: 如果成功则返回标准数据格式, 否则返回错误信息
        """
        try:
            order_id = self.check_file.is_order_id(obj.get('orderId'))
        except TypeError as err:
            raise TypeError(err)
        except ValueError as err:
            raise ValueError(err)
        except Exception as err:
            raise err
        else:
            return order_id

    # 正确后返回 begin_time, end_time
    def check_period(self, obj, time_interval=None):
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
        try:
            begin_time = self.check_file.is_time_str(obj.get('beginTime'))
            end_time = self.check_file.is_time_str(obj.get('endTime'))
        except (TypeError, ValueError) as err:
            raise err
        except Exception as err:
            raise err
        # 如果开始时间和结束时间大小不一，会被自动转化为指定的大小
        if begin_time > end_time:
            begin_time, end_time = end_time, begin_time
        if time_interval is not None:
            if (end_time - begin_time) != datetime.timedelta(days=time_interval):
                raise ValueError('时间间隔和时间周期不匹配')
        return begin_time, end_time

    # 正确后返回 is_all, count, source_list
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
            return is_all, count, source_list

        # 空检查
        if is_all is None or count is None or source_list is None:
            raise TypeError('来源查询配置中不能含有空类型')

        # 类型检查
        if not isinstance(is_all, int) or not isinstance(count, int) or not isinstance(source_list, list):
            raise TypeError('来源查询配置中类型错误')
        # 列表里面仔细检查，如果存在空串，则去除，最后count,以最后列表长度为标准
        s_list = []
        for source in source_list:
            if not isinstance(source, str):
                raise TypeError('来源名称必须为字符串')
            source = automatic_filtering_invisible_char(source)
            if len(source) > 0:
                s_list.append(source)
        count = len(s_list)
        return is_all, count, s_list

    # 正确后返回 is_all, count, source_list
    def check_word(self, obj):
        """
        暂时引用了 来源检查函数
        :param obj:
        :return:
        """
        is_all = obj.get('isAll')
        count = obj.get('count')
        source_list = obj.get('list')

        # 如果是全选，那么就不去查看其它参数
        if is_all is not None and isinstance(is_all, int) and is_all == 1:
            return is_all, count, source_list

        # 空检查
        if is_all is None or count is None or source_list is None:
            raise TypeError('监测词查询配置不能含有空参数')

        # 类型检查
        if not isinstance(is_all, int) or not isinstance(count, int) or not isinstance(source_list, list):
            raise TypeError('监测词查询配置中类型错误')
        # 列表里面仔细检查，如果存在空串，则去除，最后count,以最后列表长度为标准
        w_list = []
        for source in source_list:
            if not isinstance(source, str):
                raise TypeError('监测词必须为字符串')
            source = automatic_filtering_invisible_char(source)
            if len(source) > 0:
                w_list.append(source)
        count = len(w_list)
        return is_all, count, w_list

    # 正确后返回 position, count
    def check_page(self, obj):
        position = obj.get('position')
        count = obj.get('count')
        if position is None or count is None:
            raise TypeError('当前页和页面大小都不能为空')

        if isinstance(position, int) and isinstance(count, int):
            if position < 1 or count < 1:
                raise ValueError('页码和页面大小均必须大于1')
            else:
                return position, count
        else:
            raise TypeError('页面查询参数必须为整数')

    # 正确后返回 is_default, key, value
    def check_search(self, obj):
        is_default = obj.get('isDefault')
        key = obj.get('key')
        value = obj.get('value')
        if is_default is None or key is None or value is None:
            is_default = 1
        if isinstance(is_default, int) and is_default == 1:
            return is_default, key, value

        if not isinstance(is_default, int) or not isinstance(key, str) or not isinstance(value, str):
            raise TypeError('特定搜索参数类型错误')
        key = automatic_filtering_invisible_char(key)
        value = automatic_filtering_invisible_char(value)
        # 如果检查没有特定搜索那么则啥都不管
        if not key or not value:
            is_default = 1
        return is_default, key, value

    # 正确后返回time_interval
    def check_time_interval(self, obj):
        try:
            time_interval = self.check_file.is_time_interval(obj.get('timeInterval'))
        except TypeError as err:
            raise TypeError(err)
        except ValueError as err:
            raise ValueError(err)
        except Exception as err:
            raise err
        else:
            return time_interval

    def check_result(self, obj):
        try:
            attribute = self.check_file.is_attribute(obj.get('attribute'))
            count = self.check_file.is_int_str(obj.get('count'))
            url_list = obj.get('list')
            u_list = list()
            for url in url_list:
                url = self.check_file.is_url(url)
                u_list.append(url)
        except (TypeError, ValueError) as err:
            raise err
        except Exception as err:
            raise err
        else:
            return attribute, len(u_list), u_list

    # 正确后返回 url
    def check_url(self, obj):
        try:
            url = self.check_file.is_url(obj.get('url'))
        except (TypeError, ValueError) as err:
            raise err
        except Exception as err:
            raise err
        else:
            return url

    # 正确后返回 sort_rule
    def check_sort_rule(self, obj):
        try:
            sort_rule = self.check_file.is_sort_rule(obj.get('sort'))
        except (ValueError, TypeError) as err:
            raise ValueError(err) from err
        except Exception as err:
            raise err
        else:
            return sort_rule