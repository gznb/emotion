from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Zupdate(request):
    try:
        if request.method == "POST":
            rev_data = {
                'code': 0,
                'msg': "修改成功",
                'data': {
                    'total': 2
                }
            }
            return JsonResponse(rev_data)
        else:
            return HttpResponseBadRequest()
    except Exception as err:
        print(err)
        return HttpResponseServerError()