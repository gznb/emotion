import time
import base64
import hmac
from configuration import OUT_TIME


class Token_hander():

    def __init__(self):
        self.out_time = OUT_TIME

    def build_token(self, message):
        """
        hax_message: 待加密字符串内容  格式： '当前时间戳：message：过期时间戳'
        :param message: 需要生成token的字符串
        :param time: 过期时间
        :return: token
        """
        ts_str = str(time.time() + self.out_time)
        ts_byte = ts_str.encode("utf-8")
        sha1_tshexstr  = hmac.new(message.encode("utf-8"),ts_byte,'sha1').hexdigest()
        token = ts_str+':'+sha1_tshexstr
        b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
        return b64_token.decode("utf-8")


    def check_token(self, key, token):
        """
        :param token: 待检验的token
        :return: False   or  new token

        """
        try:
            token_str = base64.urlsafe_b64decode(token).decode('utf-8')
            token_list = token_str.split(':')
            if len(token_list) != 2:
                return False
            ts_str = token_list[0]

            # 关于时间的检验，暂时关闭
            # if float(ts_str) < time.time():
            #     # token expired
            #     return False
            known_sha1_tsstr = token_list[1]
            sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
            calc_sha1_tsstr = sha1.hexdigest()
            if calc_sha1_tsstr != known_sha1_tsstr:
                # token certification failed
                return False
            # token certification success
            return True
        except Exception as e:
            return False
