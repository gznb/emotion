import simplejson
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest
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
        get_data = simplejson.loads(request.body)
        
        try:


            Ztelephone = get_data['telephone']

            Zoldpassword = get_data['oldpassword']
        except Exception as err:
            print(err)
            rev_data = USERMODIFY[2]
            return JsonResponse(rev_data)

        user = d2UserModel.objects(GuserTelephone=Ztelephone, GuserPassword= Zoldpassword).first()
        if user is None:
            rev_data = USERMODIFY[5]
            return JsonResponse(rev_data)
        print(Ztelephone)
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

    except Exception as err:
        print(err)
        return HttpResponseServerError()