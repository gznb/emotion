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

    @ staticmethod
    def _is_type(obj, *accept):
        """
        :param obj:  需要判断的类型
        :param *accept:  运行的类型列表
        :return:          如果是运行的类型，返回True, 不然就是 False
        """
        for a in accept:
            if isinstance(obj, a):
                return True
        else:
            return False

    def is_telephon(self, telephone):
        """
        :param telephone：传递过来的是只包含可见字符的字符串
        :return: (code, msg)
        """
        # 检测号码是否为空。
        if telephone is None:
            return 101, self.code_msg['101']

        # 判断类型
        if not self._is_type(telephone, str):
            return 103, self.code_msg['103']

        # 吸收掉空格等字符
        telephone = automatic_filtering_invisible_char(telephone)
        if len(telephone) == 0:
            return 101, self.code_msg['101']

        if len(telephone) != 11:
            return 102, self.code_msg['102']
        else:
            # 检查是不是全部为数字
            if telephone.isdigit():
                # 检查是不是包含在三大运营商提供的前缀里面
                if telephone[:3] in self.phone_prefix:
                    return 100, self.code_msg['100'], telephone
                else:
                    return 103, self.code_msg['103']
            else:
                return 104, self.code_msg['104']

    def is_username(self, username):
        """
        :param username: 只能是可见字符
        :return: (code, msg)
        """
        # 空检查
        if username is None:
            return 121, self.code_msg['121']
        # 类型检查
        if not self._is_type(username, str):
            return 122, self.code_msg['122']
        # 空串检查
        username = automatic_filtering_invisible_char(username)
        if len(username) == 0:
            return 121, self.code_msg['121']
        # 长度检查
        if len(username) > 16 or len(username) < 2:
            return 123, self.code_msg['123']
        else:
            return 120, self.code_msg['120'], username

    def is_email(self, email):
        """
        邮箱检查
        :param email:
        :return:
        """
        # 空检查
        if email is None:
            return 141, self.code_msg['141']
        # 类型检查
        if not self._is_type(email, str):
            return 142, self.code_msg['142']
        # 空串检查
        email = automatic_filtering_invisible_char(email)
        if len(email) == 0:
            return 141, self.code_msg['141']
        # 邮箱合法性检查
        email_rule = r'^[0-9a-zA-Z\_\-]+(\.[0-9a-zA-Z\_\-]+)*@[0-9a-zA-Z]+(\.[0-9a-zA-Z]+){1,}$'
        if not re.match(email_rule, email):
            return 143, self.code_msg['141']
        return 140, self.code_msg['140'], email

    def is_order_id(self, order_id):
        """
        检查订单id
        :param order_id:
        :return: 失败只返回2个参数，成功返回3个
        """
        # 空检查
        if order_id is None:
            return 161, self.code_msg['161']
        # 类型检查
        if not self._is_type(order_id, int):
            return 162, self.code_msg['162']

        # 不能小于 0
        if order_id < 0:
            return 163, self.code_msg['163']
        return 160, self.code_msg['160'], order_id

    def is_time_interval(self, time_interval):
        """
        检查时间周期
        :param time_interval:
        :return: (code, msg, [time_interval])
        180: (code, msg, time_interval)

        """
        # 空检查
        if time_interval is None:
            return 181, self.code_msg['181']
        # 类型检查
        if not self._is_type(time_interval, int):
            return 182, self.code_msg['182']

        # 不能小于 1
        if int(time_interval) < 1:
            return 183, self.code_msg['183']
        return 180, self.code_msg['180'], time_interval

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
            return 201, self.code_msg['201']
        # 类型检查
        if not self._is_type(time, str):
            return 202, self.code_msg['202']
        # 空串检查
        time = time.strip()
        if len(time) == 0:
            return 201, self.code_msg['201']
        try:
            # 检查是否为标准时间字符串
            # print(time)
            timestamp = datetime.datetime.strptime(time, DATETIME_FORMAT_STR)
        except ValueError as err:
            print(err)
            return 203, self.code_msg['203']
        else:
            return 200, self.code_msg, timestamp

