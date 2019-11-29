from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError
from d2User.models import d2UserModel
from django_redis import get_redis_connection
from conf.time_conf import OUT_TIME
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from my_rest_framework.token import TokenHander
from conf.field_conf import INITIALLEVEL, EXTENSIONOFTIME, TRIALDURATION
import datetime
import logging
from check_data.check_field import CheckField
from mongoengine import errors
logger = logging.getLogger('django')


class RegisterView(APIView):
    authentication_classes = []
    check_field = CheckField()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        company = request.data.get('company')
        telephone = request.data.get('telephone')
        email = request.data.get('email')
        region = request.data.get('region')
        if not username or not company or not telephone or not email or not region:
            rev_data = {'code': 1, 'msg': "带*号是关键信息一定要填", 'data': {}}
            return JsonResponse(rev_data)
        new_user = d2UserModel(
            GuserUsername=username,
            GuserPassword=telephone,
            GuserTelephone=telephone,
            GuserCompany=company,
            GuserEmail=email,
            GuserRegion=region,
            GuserPosition=INITIALLEVEL,
            GuserPurchaseDate=datetime.datetime.now(),
            GuserRegistrationDate=datetime.datetime.now(),
            GuserLastLogin=datetime.datetime.now(),
            GuserAvailableTime=TRIALDURATION,
            GuserExtendedDate=EXTENSIONOFTIME,
        )
        rev_data = {}
        try:
            new_user.save()
        except errors.NotUniqueError as err:  # 重复注册
            rev_data = {'code': 2, 'msg': '该号码已经注册', 'data': {}}
            return JsonResponse(rev_data)
        except errors.ValidationError as err:  # 字段异常
            rev_data = {'code': 4, 'msg': '请检查自己输入信息是否合法', 'data': {}}
            logger.error(err)
            return JsonResponse(rev_data)
        except Exception as err:        # 服务器异常
            logger.error(err)
            return HttpResponseServerError()
        else:
            rev_data = {'code': 0, 'msg': "注册成功", 'data': {}}
            return JsonResponse(rev_data)
