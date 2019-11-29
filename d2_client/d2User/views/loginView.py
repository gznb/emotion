from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError
from d2User.models import d2UserModel
from django_redis import get_redis_connection
from conf.time_conf import OUT_TIME
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from my_rest_framework.token import TokenHander
import logging
logger = logging.getLogger('django')


class LoginView(APIView):
    # 不进行token 验证
    authentication_classes = []
    # 只允许  json 数据，但是这里不知道什么原因无法使用?????
    parser_classes = [JSONParser, ]

    def post(self, request, *args, **kwargs):
        # self.dispatch()
        telephone = request.data.get('telephone')
        pwd = request.data.get('password')
        if not telephone or not pwd:
            return JsonResponse({'code': 2, 'msg': '账号或者密码不能为空', 'data': {}})
        if telephone == pwd:
            rev_data = {'code': 2, 'msg': "请修改初始密码，不修改将无法使用", 'data': {}}
            return JsonResponse(rev_data)
        try:
            user = d2UserModel.objects(GuserTelephone=telephone, GuserPassword=pwd).first()
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        if user:
            token_obj = TokenHander()
            token = token_obj.build_token(telephone)
            conn = get_redis_connection()
            conn.set(token, telephone, ex=OUT_TIME)
            rev_data = {'code': 0, 'msg': '登陆成功', 'data': {'token': token,'username': user.GuserUsername}}
        else:
            rev_data = {'code': 1, 'msg': "账号或者密码错误", 'data':{}}
        return JsonResponse(rev_data)
