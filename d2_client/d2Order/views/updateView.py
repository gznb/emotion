from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Zupdate(request):
    try:
        if request.method == 'POST':
            rev_data = {
                'code': 0,
                'msg': "更新成功",
                'data': {}
            }
            return JsonResponse(rev_data)
        else:
            return HttpResponseBadRequest()
    except Exception as err:
        print(err)
        return HttpResponseServerError()
