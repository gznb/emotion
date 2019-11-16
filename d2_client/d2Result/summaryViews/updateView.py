from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Zupdate(request):
    try:

        rev_data = {
            'code': 0,
            'msg': "修改成功",
            'data': {
                'total': 2
            }
        }
        return JsonResponse(rev_data)

    except Exception as err:
        print(err)
        return HttpResponseServerError()