import time
import base64
import hmac
from configuration import OUT_TIME
from django_redis import get_redis_connection
# import itsdangerous

class TokenHander():
    def __init__(self):
        self.out_time = OUT_TIME
        self.conn = get_redis_connection()

    def build_token(self, message):
        """
        hax_message: 待加密字符串内容  格式： '当前时间戳：message：过期时间戳'
        :param message: 需要生成token的字符串
        :param time: 过期时间
        :return: token
        """
        # 得到当前时间
        ts_str = str(time.time())
        # 转变编码
        ts_byte = ts_str.encode("utf-8")
        sha1_tshexstr = hmac.new(message.encode("utf-8"),ts_byte, 'sha1').hexdigest()
        token = ts_str+':'+sha1_tshexstr
        b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
        return b64_token.decode("utf-8")

    # def create_token(self, data, expires_in):
    #     salt="gznb"
    #     t = itsdangerous.TimedJSONWebSignatureSerializer(salt, expires_in=expires_in)
    #     rest = t.dumps(data)
    #     token = rest.decode()
    #     return token
    #
    # def check_token(self, token):
    #     t = itsdangerous.TimedJSONWebSignatureSerializer('gznb')
    #     try:
    #         res = t.loads(token)
    #     except Exception as e:
    #         raise
    #     else:
    #         return res
    #
    # def check_session(self, token):
    #     result = self.check_token(token)
    #     if result:
    #         username=result.get('username')
    #         print(username)

