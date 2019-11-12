from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Zdelete(request):
    try:
        if request.method == 'POST':
            rev_data = {
                'code': 0,
                'msg': "删除成功",
                'data': {}
            }
            return JsonResponse(rev_data)
        else:
            return HttpResponseBadRequest()
    except Exception as err:
        print(err)
        return HttpResponseServerError()
