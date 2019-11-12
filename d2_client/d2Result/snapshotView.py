from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Znapshot(request):
    try:
        if request.method == "POST":
            rev_data = {
                "code": 0,
                "msg": "成功",
                "data": {
                    "title": "XXXXXX",
                    "releaseTime": "2019-10-10",
                    "attribute": "XXXX",
                    "keyword": "XXXXX",
                    "source": "XXXXX",
                    "channel": "xxxxx",
                    "content": "xxxxxxx",
                    "url": "XXXXXXXXX"
                }
            }
            return JsonResponse(rev_data)
        else:
            return HttpResponseBadRequest()
    except Exception as err:
        return HttpResponseServerError()