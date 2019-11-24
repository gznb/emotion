import datetime
import simplejson
from d2User.models import d2UserModel
from mongoengine.errors import ValidationError, NotUniqueError
from django.http import JsonResponse, HttpResponseServerError
from configuration import USERREGISTER, TRIALDURATION, INITIALLEVEL, EXTENSIONOFTIME, OUT_TIME
from tools.token import Token_hander
from django_redis import get_redis_connection

def Zregister(request):
    try:
        get_data = simplejson.loads(request.body)
        Zusername = get_data.get('username')
        Zcompany = get_data.get('company')
        Ztelephone = get_data.get('telephone')
        Zemail = get_data.get('email')
        Zregion = get_data.get('region')
        
        
        # 关键信息不为空判断
        if Zusername is None or Zcompany is None or Ztelephone is None:
            rev_data = USERREGISTER[1]
            return JsonResponse(rev_data)


        # 没有被注册， 开始注册，初始化有关字段，密码为电话号码
        newUser = d2UserModel(
            GuserUsername= Zusername,
            GuserPassword= Ztelephone, 
            GuserTelephone= Ztelephone,
            GuserCompany= Zcompany,
            GuserEmail= Zemail,
            GuserRegion= Zregion,
            GuserPosition= INITIALLEVEL,
            GuserPurchaseDate= datetime.datetime.now(),
            GuserRegistrationDate = datetime.datetime.now(),
            GuserLastLogin = datetime.datetime.now(),
            GuserAvailableTime= TRIALDURATION,
            GuserExtendedDate= EXTENSIONOFTIME,
        )
        
        # 尝试插入
        try:
            newUser.save()
        except NotUniqueError as err:  # 重复注册
            rev_data = USERREGISTER[2]
            return JsonResponse(rev_data)
        except ValidationError as err:  # 字段异常
            rev_data = USERREGISTER[4]
            print(err)
            return JsonResponse(rev_data)
        except Exception as err:        # 服务器异常
            return HttpResponseServerError()
        else:   
            # 新建 token， 放入redis， 发送给客户端
            tokenClass = Token_hander()
            token = tokenClass.build_token(Ztelephone)
            conn = get_redis_connection()
            conn.set(token, Ztelephone, ex=OUT_TIME)
            conn.hmset(Ztelephone, {'telephone': Ztelephone, 'username':Zusername})
            conn.expire(Ztelephone, 86400)
            rev_data = USERREGISTER[0]
            rev_data['data'] = {
                'token': token,
                'username': Zusername
            }
            return JsonResponse(rev_data)
    except Exception as err:
        return HttpResponseServerError()