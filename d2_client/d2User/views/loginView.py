from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError
from configuration import USERLOGINMSG, OUT_TIME
from d2User.models import d2UserModel
import simplejson
import pprint
from mongoengine import queryset
from tools.examine import examineTelephone
from tools.token import Token_hander
from django_redis import get_redis_connection 

def Zlogin(request):
    '''
        登陆成功，返回token, 以及 用户姓名
    '''
    try:

        if request.method == 'POST':
            get_data = simplejson.loads(request.body)
            try:
                Zpassword = get_data['password']
                Ztelephone = get_data['telephone']
            except Exception as err:
                print(err)
                return HttpResponseNotFound()

            conn = get_redis_connection()
            tokenClass = Token_hander()
            
            # 强迫修改默认密码
            if Ztelephone == Zpassword:
                rev_data = USERLOGINMSG[2]
                return JsonResponse(rev_data)
            
            # 电话号码检查
            tp, msg = examineTelephone(Ztelephone)

            if tp == 0:
                rev_data = USERLOGINMSG[3]
                rev_data['msg'] = msg
                return JsonResponse(rev_data)

            # 验证 是否存在
            user = d2UserModel.objects(GuserTelephone= Ztelephone, GuserPassword= Zpassword).first()
            if user is None:
                rev_data = USERLOGINMSG[1]
                return JsonResponse(rev_data)
            Zusername = user['GuserUsername']
            rev_data = USERLOGINMSG[0]
            rev_data['test'] = "enenen"
            token = tokenClass.build_token(Ztelephone)
            conn.set(token, Ztelephone, ex=OUT_TIME)

            conn.hmset(Ztelephone, {'telephone' : Ztelephone, 'username': Zusername})
            conn.expire(Ztelephone, 86400)
            rev_data['data'] = {
                'token': token,
                'username': Zusername,
            }
            return JsonResponse(rev_data)
        else:
            return HttpResponseNotFound()
    except Exception as err:
        print(err)
        return HttpResponseServerError()