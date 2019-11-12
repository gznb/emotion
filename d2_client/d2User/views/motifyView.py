import simplejson
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError
from d2User.models import d2UserModel
from configuration import USERMODIFY, OUT_TIME
from tools.token import Token_hander
from django_redis import get_redis_connection
from mongoengine.errors import ValidationError

def Zmodify(request):
    '''
    需要得到密码，原来的密码，现在的密码，然后知道一些其他的资料
    '''
    try:

        if request.method == "POST":

            get_data = simplejson.loads(request.body)
            

            Ztelephone = None
            Zoldpassword = None

            Ztoken = request.META.get('HTTP_X_TOKEN')
            
            conn = get_redis_connection()
            tokenClass = Token_hander()
            
            user  = None
            # 如果 上传了token
            if Ztoken is not None:
                Ztelephone = conn.get(Ztoken)
                if Ztelephone is not None:
                    Ztelephone = Ztelephone.decode('UTF-8')
                
            # 发现token 中的 失效了, 就需要从这里得到原来的账号和密码
            if Ztelephone is None:
                Ztelephone = get_data.get('telephone')

            # 检查token是不是有效的
            tp = tokenClass.check_token(Ztelephone, Ztoken)

            # token 检查通过，就是已经登录
            if tp:
                conn.expire(Ztoken, time=OUT_TIME)
                Zoldpassword = get_data.get('oldpassword')
                if Zoldpassword is None:
                    rev_data = USERMODIFY[2]
                    return JsonResponse(rev_data)
                # 检查密码
                user = d2UserModel.objects(GuserTelephone=Ztelephone, GuserPassword= Zoldpassword).first()
                if user is None:
                    rev_data = USERMODIFY[5]
                    return JsonResponse(rev_data)

                # 判断有关信息是否需要修改
                Znewpassword = get_data.get('newpassword')
                # 必须要修改初始化的密码，不能和账号一样
                if Znewpassword is None:
                    if Zoldpassword == Ztelephone:
                        rev_data = USERMODIFY[3]
                        return JsonResponse(rev_data)

                if Znewpassword == Ztelephone:
                    rev_data = USERMODIFY[3]
                    return JsonResponse(rev_data)

                # 如果有输入其他信息，有则修改，没有则算了
                if Znewpassword is not None:
                    user.GuserPassword = Znewpassword   
                
                Zusername = get_data.get('username')
                if Zusername is not None:
                    user.GuserUsername = Zusername
                
                Zcompany = get_data.get('company')
                if Zcompany is not None:
                    user.GuserCompany = Zcompany

                Zemail = get_data.get('email')
                if Zemail is not None:
                    user.GuserEmail = Zemail
                
                Zregion = get_data.get('region')
                if Zregion is not None:
                    user.GuserRegion = Zregion

                try:
                    user.save()
                except ValidationError as err:
                    rev_data = USERMODIFY[4]
                    return JsonResponse(rev_data)
                except Exception as err:
                    print(err)
                    return HttpResponseServerError()
                else:
                    rev_data = USERMODIFY[0]
                    return JsonResponse(rev_data)
            else:
                rev_data = USERMODIFY[1]
                return JsonResponse(rev_data)
                
        else:
            return HttpResponseNotFound()
    except Exception as err:
        print(err)
        return HttpResponseServerError()