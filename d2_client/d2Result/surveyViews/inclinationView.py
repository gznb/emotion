from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Zinclination(request):
    try:
        if request.method == "POST":
            rev_data = {
                'code': 0,
                'msg': '成功',
                'data': {
                    'thisPeriod': {
                        'positive': 10,
                        'negative': 20,
                        'neutral': 40
                    },
                    'lastPeriod': {
                        'positive': 2,
                        'negative': 3,
                        'neutral': 6
                    }
                
                }
            }
            return JsonResponse(rev_data)
        else:
            return HttpResponseBadRequest()
    except Exception as err:
        print(err)
        return HttpResponseServerError()