# encoding:utf-8

import re
from conf.field_conf import PHONE_PREFIX
from conf.code_msg import CODE_MSG_DICT
from tools.filtering_char import automatic_filtering_invisible_char
import datetime
from conf.time_conf import DATETIME_FORMAT_STR


class CheckField(object):
    def __init__(self, *args, **kwargs):
        self.phone_prefix = PHONE_PREFIX
        self.code_msg = CODE_MSG_DICT

    @classmethod
    def instance(cls, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        if not hasattr(CheckField, "_instance"):
            CheckField._instance = CheckField(*args, **kwargs)
        return CheckField._instance

    def is_telephon(self, telephone):
        """
        :param telephone：传递过来的是只包含可见字符的字符串
        :return: (code, msg)
        """
        # 检测号码是否为空。
        if telephone is None:
            raise ValueError('手机号码不能为空')

        # 判断类型
        if not isinstance(telephone, str):
            raise TypeError('手机号码只能是数字字符串')

        # 吸收掉空格等字符
        telephone = automatic_filtering_invisible_char(telephone)
        if len(telephone) != 11:
            raise ValueError('手机号码必须为11位')
        else:
            # 检查是不是全部为数字
            if telephone.isdigit():
                # 检查是不是包含在三大运营商提供的前缀里面
                if telephone[:3] in self.phone_prefix:
                    return telephone
                else:
                    raise ValueError('该手机号码不在三大运营商之内')
            else:
                # 手机号码应该为数字字符串
                raise TypeError('手机号码只能是数字字符串')

    def is_username(self, username):
        """
        :param username: 只能是可见字符
        :return: (code, msg)
        """
        # 空检查
        if username is None:
            # 用户名不能为空
            raise TypeError('用户名不能为空')
            # return 121, self.code_msg['121']
        # 类型检查
        if not isinstance(username, str):
            # 用户名必须为字符串
            raise TypeError('用户名必须为字符串')
            # return 122, self.code_msg['122']
        # 空串检查
        username = automatic_filtering_invisible_char(username)
        if len(username) == 0:
            # 用户名不能为空
            raise ValueError('用户名不能为空')
            # return 121, self.code_msg['121']
        # 长度检查
        if len(username) > 16 or len(username) < 2:
            # 用户名长度必须大于2位并且小于16位!!!
            raise ValueError('用户名长度必须大于2位并且小于16位!!!')
            # return 123, self.code_msg['123']
        else:
            return username

    def is_email(self, email):
        """
        邮箱检查
        :param email:
        :return:
        """
        # 空检查
        if email is None:
            # 邮箱不能为空
            raise TypeError('邮箱不能为空')
            # return 141, self.code_msg['141']
        # 类型检查
        if not isinstance(email, str):
            # 邮箱必须为字符串
            raise TypeError('邮箱必须为字符串')
            # return 142, self.code_msg['142']
        # 空串检查
        email = automatic_filtering_invisible_char(email)
        if len(email) == 0:
            # 邮箱不能为空
            raise ValueError('邮箱不能为空')
            # return 141, self.code_msg['141']
        # 邮箱合法性检查
        email_rule = r'^[0-9a-zA-Z\_\-]+(\.[0-9a-zA-Z\_\-]+)*@[0-9a-zA-Z]+(\.[0-9a-zA-Z]+){1,}$'
        if not re.match(email_rule, email):
            # 非法邮箱
            raise ValueError('非法邮箱')
            # return 143, self.code_msg['141']
        return email

    def is_order_id(self, order_id):
        """
        检查订单id
        :param order_id:
        :return: 失败只返回2个参数，成功返回3个
        """
        # 空检查
        if order_id is None:
            # 订单编号不能为空
            raise TypeError('订单编号不能为空')
            # return 161, self.code_msg['161']
        # 类型检查
        if not isinstance(order_id, int):
            # 订单编号必须为数字
            raise TypeError('订单编号必须为数字')
            # return 162, self.code_msg['162']

        # 不能小于 0
        if order_id < 0:
            # 订单编号必须 >= 0
            raise ValueError('订单编号必须 >= 0')
            # return 163, self.code_msg['163']
        return order_id

    def is_time_interval(self, time_interval):
        """
        检查时间周期
        :param time_interval:
        :return: (code, msg, [time_interval])
        180: (code, msg, time_interval)

        """
        # 空检查
        if time_interval is None:
            # 时间周期不能为空
            raise TypeError('时间周期不能为空')
            # return 181, self.code_msg['181']
        # 类型检查
        if not isinstance(time_interval, int):
            # 时间周期必须为数字
            raise TypeError('时间周期必须为数字')
            # return 182, self.code_msg['182']

        # 不能小于 1
        if int(time_interval) < 1:
            # 时间周期必须 >= 1
            raise ValueError('时间周期必须 >= 1')
            # return 183, self.code_msg['183']
        return time_interval

    def is_time_str(self, time):
        """
        时间检查
        :param time:
        :return:  (code, msg [timestamp])
        200 正常, 后面携带timestamp,类型为 datetime
        1. 为空 201
        2. 不是字符串类型 202
        3. 不是标准时间字符串 203
        """
        # 空检查
        if time is None:
            # 时间不能为空
            raise TypeError('时间不能为空')
            # return 201, self.code_msg['201']
        # 类型检查
        if not isinstance(time, str):
            # 时间必须为字符串类型
            raise TypeError('时间必须为字符串类型')
            # return 202, self.code_msg['202']
        # 空串检查
        time = time.strip()
        if len(time) == 0:
            # 时间不能为空
            raise ValueError('时间不能为空')
            # return 201, self.code_msg['201']
        try:
            # 检查是否为标准时间字符串
            # print(time)
            timestamp = datetime.datetime.strptime(time, DATETIME_FORMAT_STR)
        except ValueError as err:
            # 时间必须为'%Y-%m-%d %H:%M:%S'格式例如'2011-11-11 11:11:11'
            raise ValueError("时间必须为'%Y-%m-%d %H:%M:%S'格式例如'2011-11-11 11:11:11'")
            # return 203, self.code_msg['203']
        else:
            return timestamp

    def is_int_str(self, int_str):
        if not isinstance(int_str, (str, int)):
            raise TypeError('类型错误')
        else:
            try:
                temp = int(int_str)
            except ValueError as err:
                raise ValueError('应该为数字字符串或者是数字, 不能包含其他字符')
            else:
                return temp


    def is_url(self, url):
        if not isinstance(url, str):
            raise TypeError('url类型错误')
        url = automatic_filtering_invisible_char(url)
        if len(url) < 5:
            raise ValueError('url值错误')
        else:
            return url


    def is_attribute(self, attribute):
        if not isinstance(attribute, str):
            raise TypeError('类型错误')
        else:
            attribute = automatic_filtering_invisible_char(attribute)
            if attribute == '正面':
                return attribute
            elif attribute == '中性':
                return attribute
            elif attribute == '负面':
                return attribute
            else:
                raise ValueError('属性必须3种属性中之一')