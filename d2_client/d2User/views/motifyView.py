from django.http import JsonResponse,  HttpResponseServerError
from d2User.models import d2UserModel
from mongoengine.errors import ValidationError
from rest_framework.views import APIView

import logging
logger = logging.getLogger('django')


class MotifyView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        rev_data = {}
        telephone = request.data.get('telephone')
        old_password = request.data.get('oldpassword')
        if not telephone or not old_password:
            rev_data = {'code': 2, 'msg': '请输入手机号码和旧密码', 'data': {}}
            return JsonResponse(rev_data)

        # 检查是否存在该账号密码
        # print(telephone, old_password)
        user = d2UserModel.objects(GuserTelephone=telephone, GuserPassword=old_password).first()
        # print(user)
        if not user:
            rev_data = {'code': 5, 'msg': '账号或者原密码错误', 'data':{}}
            return JsonResponse(rev_data)

        new_passwprd = request.data.get('newpassword')
        if new_passwprd:
            if new_passwprd == old_password or new_passwprd == telephone:
                rev_data = {'code': 3, 'msg': '新密码不能为原密码，也不能为自己手机号码', 'data': {}}
                return JsonResponse(rev_data)

        if new_passwprd is not None:
            user.GuserPassword = new_passwprd

        username = request.data.get('username')
        if username is not None:
            user.GuserUsername = username

        company = request.data.get('company')
        if company is not None:
            user.GuserCompany = company

        email = request.data.get('email')
        if email is not None:
            user.GuserEmail = email

        region = request.data.get('region')
        if region is not None:
            user.GuserRegion = region
        try:
            user.save()
        except ValidationError as err:
            # print(err)
            rev_data = {'code': 4, 'msg': '输入信息不合法，请确认，不想修改信息可以不填写', 'data': {}}
            return JsonResponse(rev_data)
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            rev_data = {'code': 0, 'msg': "修改成功", 'data':{}}
            return JsonResponse(rev_data)

# def Zmodify(request):
#     '''
#     需要得到密码，原来的密码，现在的密码，然后知道一些其他的资料
#     '''
#     pass
#     # try:
#     #     get_data = simplejson.loads(request.body)
#     #
#     #     try:
#     #
#     #
#     #         Ztelephone = get_data['telephone']
#     #
#     #         Zoldpassword = get_data['oldpassword']
#     #     except Exception as err:
#     #         print(err)
#     #         rev_data = USERMODIFY[2]
#     #         return JsonResponse(rev_data)
#     #
#     #     user = d2UserModel.objects(GuserTelephone=Ztelephone, GuserPassword= Zoldpassword).first()
#     #     if user is None:
#     #         rev_data = USERMODIFY[5]
#     #         return JsonResponse(rev_data)
#     #     print(Ztelephone)
#     #     # 判断有关信息是否需要修改
#     #     Znewpassword = get_data.get('newpassword')
#     #     # 必须要修改初始化的密码，不能和账号一样
#     #     if Znewpassword is None:
#     #         if Zoldpassword == Ztelephone:
#     #             rev_data = USERMODIFY[3]
#     #             return JsonResponse(rev_data)
#     #
#     #     if Znewpassword == Ztelephone:
#     #         rev_data = USERMODIFY[3]
#     #         return JsonResponse(rev_data)
#     #
#     #     # 如果有输入其他信息，有则修改，没有则算了
#     #     if Znewpassword is not None:
#     #         user.GuserPassword = Znewpassword
#     #
#     #     Zusername = get_data.get('username')
#     #     if Zusername is not None:
#     #         user.GuserUsername = Zusername
#     #
#     #     Zcompany = get_data.get('company')
#     #     if Zcompany is not None:
#     #         user.GuserCompany = Zcompany
#     #
#     #     Zemail = get_data.get('email')
#     #     if Zemail is not None:
#     #         user.GuserEmail = Zemail
#     #
#     #     Zregion = get_data.get('region')
#     #     if Zregion is not None:
#     #         user.GuserRegion = Zregion
#     #
#     #     try:
#     #         user.save()
#     #     except ValidationError as err:
#     #         rev_data = USERMODIFY[4]
#     #         return JsonResponse(rev_data)
#     #     except Exception as err:
#     #         print(err)
#     #         return HttpResponseServerError()
#     #     else:
#     #         rev_data = USERMODIFY[0]
#     #         return JsonResponse(rev_data)
#     #
#     # except Exception as err:
#     #     print(err)
#     #     return HttpResponseServerError()

