from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponse
import simplejson
from d2Admin.models import d2AdminModel
from django_redis import get_redis_connection
from tools.token import Token_hander
from configuration import OUT_TIME, ADMINLOGIN

def Zlogin(request):
    '''
        注册
    '''
    try:
        # 接受数据
        get_data = simplejson.loads(request.body)

        Ztelephone = get_data.get('telephone')
        Zpassword = get_data.get('password')
        print(Ztelephone, Zpassword)
        # 判断是否为空
        if Ztelephone is None or Zpassword is None:
            rev_data = ADMINLOGIN[1]
            return JsonResponse(rev_data)
        
        # 检查账号密码
        admin = d2AdminModel.objects(GadminTelephone=Ztelephone, GadminPassword=Zpassword).first()
        if admin is None:
            rev_data = ADMINLOGIN[1]
            return JsonResponse(rev_data)
        
        # 通过验证
        try:
            conn = get_redis_connection()
        except Exception as err:
            print(err)
            return HttpResponseServerError()
        tokenClass = Token_hander()
        token = tokenClass.build_token(Ztelephone)
        conn.set(token, Ztelephone, ex=OUT_TIME)
        conn.hmset(Ztelephone, {'telephone':Ztelephone, 'username': admin['GadminUsername']})
        conn.expire(Ztelephone, 56400)
        
        rev_data = ADMINLOGIN[0]
        rev_data['data'] = {
            'uuid': Ztelephone, 
            'name': admin['GadminUsername'], 
            'token': token
        }
        print(rev_data)
        return JsonResponse(rev_data)

    except Exception as err:
        print(err)
        return HttpResponseServerError()