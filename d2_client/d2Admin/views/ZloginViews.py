from django.http import JsonResponse, HttpResponseServerError
from d2Admin.models import d2AdminModel
from django_redis import get_redis_connection
from configuration import OUT_TIME
from rest_framework.views import APIView
from my_rest_framework.token import TokenHander

import logging
logger = logging.getLogger('django')


class LoginView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        telephone = request.data.get('telephone')
        password = request.data.get('password')
        if not telephone or not password:
            return JsonResponse({'code': 2, 'msg': '账号或者密码不能为空', 'data': {}})
        try:
            admin = d2AdminModel.objects(GadminTelephone=telephone, GadminPassword=password).first()
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        if admin:
            token_obj = TokenHander()
            token = token_obj.build_token(telephone)
            conn = get_redis_connection()
            conn.set(token, telephone, ex=OUT_TIME)
            rev_data = {'code': 0, 'msg': '登陆成功', 'data': {'token': token,'username': admin.GadminUsername}}
        else:
            rev_data = {'code': 1, 'msg': "账号或者密码错误", 'data': {}}
        return JsonResponse(rev_data)
