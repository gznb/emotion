from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Zadd(request):
    try:

        rev_data = {
            'code': 0,
            'msg': "添加成功",
            'data': {}
        }
        return JsonResponse(rev_data)

    except Exception as err:
        print(err)
        return HttpResponseServerError()
