from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponse
import simplejson
from d2Admin.models import d2AdminModel
from django_redis import get_redis_connection
from tools.token import Token_hander
from configuration import OUT_TIME, ADMINLOGIN


def Zlogin(request):
    """
    注册
    :param request:
    :return:
    """
    try:
        # 接受数据
        get_data = simplejson.loads(request.body)

        telephone = get_data.get('telephone')
        password = get_data.get('password')
        print(telephone, password)
        # 判断是否为空
        if telephone is None or password is None:
            rev_data = ADMINLOGIN[1]
            return JsonResponse(rev_data)
        
        # 检查账号密码
        admin = d2AdminModel.objects(GadminTelephone=telephone, GadminPassword=password).first()
        if admin is None:
            rev_data = ADMINLOGIN[1]
            return JsonResponse(rev_data)
        
        # 通过验证
        try:
            conn = get_redis_connection()
        except Exception as err:
            print(err)
            return HttpResponseServerError()
        token_class = Token_hander()
        token = token_class.build_token(telephone)
        conn.set(token, telephone, ex=OUT_TIME)
        conn.hmset(telephone, {'telephone': telephone, 'username': admin['GadminUsername']})
        conn.expire(telephone, 56400)
        
        rev_data = ADMINLOGIN[0]
        rev_data['data'] = {
            'uuid': telephone,
            'name': admin['GadminUsername'], 
            'token': token
        }
        print(rev_data)
        return JsonResponse(rev_data)

    except Exception as err:
        print(err)
        return HttpResponseServerError()