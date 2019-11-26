from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Zupdate(request):
    try:

        rev_data = {
            'code': 0,
            'msg': "更新成功",
            'data': {}
        }
        return JsonResponse(rev_data)

    except Exception as err:
        # print(err)
        return HttpResponseServerError()
