from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Zinitialization(request):
    try:
        if request.method == "POST":
            rev_data = {
                'code': 0,
                'msg': "成功",
                'data': {
                    'attribute': {
                        'total': 100,
                        'positive': 20,
                        'negative': 50,
                        'neutral': 30
                    },
                    'source': {
                        "isAll":1,
                        "total" : 100,
                        "count": 4,
                        "list": [
                            {
                                "name": "搜索引擎",
                                "total" : 40,
                            },
                            {
                                "name": "报纸",
                                "total" : 30
                            },
                            {
                                "name": "贴吧",
                                "total": 20,
                            },
                            {
                                "name": "论坛",
                                "total": 10
                            }
                        ]
                    },
                    'word':{
                        'isAll': 0,
                        'count': 2,
                        'list': ['天平洋集团', '严介和']
                    }
                }
            }
            return JsonResponse(rev_data)
        else:
            return HttpResponseBadRequest()
    except Exception as err:
        print(err)
        return HttpResponseBadRequest()