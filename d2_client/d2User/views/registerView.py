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



def Zregister(request):
    pass
    # try:
    #     get_data = simplejson.loads(request.body)
    #     Zusername = get_data.get('username')
    #     Zcompany = get_data.get('company')
    #     Ztelephone = get_data.get('telephone')
    #     Zemail = get_data.get('email')
    #     Zregion = get_data.get('region')
    #
    #
    #     # 关键信息不为空判断
    #     if Zusername is None or Zcompany is None or Ztelephone is None:
    #         rev_data = USERREGISTER[1]
    #         return JsonResponse(rev_data)
    #
    #
    #     # 没有被注册， 开始注册，初始化有关字段，密码为电话号码
    #     newUser = d2UserModel(
    #         GuserUsername= Zusername,
    #         GuserPassword= Ztelephone,
    #         GuserTelephone= Ztelephone,
    #         GuserCompany= Zcompany,
    #         GuserEmail= Zemail,
    #         GuserRegion= Zregion,
    #         GuserPosition= INITIALLEVEL,
    #         GuserPurchaseDate= datetime.datetime.now(),
    #         GuserRegistrationDate = datetime.datetime.now(),
    #         GuserLastLogin = datetime.datetime.now(),
    #         GuserAvailableTime= TRIALDURATION,
    #         GuserExtendedDate= EXTENSIONOFTIME,
    #     )
    #
    #     # 尝试插入
    #     try:
    #         newUser.save()
    #     except NotUniqueError as err:  # 重复注册
    #         rev_data = USERREGISTER[2]
    #         return JsonResponse(rev_data)
    #     except ValidationError as err:  # 字段异常
    #         rev_data = USERREGISTER[4]
    #         print(err)
    #         return JsonResponse(rev_data)
    #     except Exception as err:        # 服务器异常
    #         return HttpResponseServerError()
    #     else:
    #         # 新建 token， 放入redis， 发送给客户端
    #         tokenClass = Token_hander()
    #         token = tokenClass.build_token(Ztelephone)
    #         conn = get_redis_connection()
    #         conn.set(token, Ztelephone, ex=OUT_TIME)
    #         conn.hmset(Ztelephone, {'telephone': Ztelephone, 'username':Zusername})
    #         conn.expire(Ztelephone, 86400)
    #         rev_data = USERREGISTER[0]
    #         rev_data['data'] = {
    #             'token': token,
    #             'username': Zusername
    #         }
    #         return JsonResponse(rev_data)
    # except Exception as err:
    #     return HttpResponseServerError()


class RegisterView(APIView):
    authentication_classes = []
    # parser_classes = [JSONParser, ]
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
