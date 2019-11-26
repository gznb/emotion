from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django_redis import get_redis_connection
from conf.time_conf import OUT_TIME
# 用drf的认证,写一个类,可以继承BaseAuthentication,也可以不用
# class LoginAuth(BaseAuthentication):


class LoginAuth(BaseAuthentication):
    # 函数名一定要叫authenticate,接收必须两个参数,第二个参数是request对象
    def authenticate(self, request):
        # 从request对象中取出token(也可以从其它地方取)
        # 中请求头中获得
        token = request.META.get('HTTP_X_TOKEN')
        # print(token)
        # print(request.data.get('token'))
        # 去数据库过滤,查询

        # ret = models.UserToken.objects.filter(token=token)
        conn = get_redis_connection()
        telephone = conn.get(token)
        if telephone:
            # 能查到,说明认证通过,返回空
            conn.expire(token, OUT_TIME)
            # 返回用户电话号码
            return telephone.decode('utf-8'), token
        # 如果查不到,抛异常
        raise exceptions.APIException(1000)