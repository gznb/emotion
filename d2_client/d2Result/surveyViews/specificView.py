from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Zspecific(request):
    try:

        rev_data = {
            'code': 0,
            'msg': "成功",
            'data': {
                'count': 3,  # 最多显示10页
                'list': [
                    {
                        'time': "2019-11-8 14:50",
                        'title': "XXXXXXXXXX",
                        'url': "www.XXXXXX.com",
                        'score': 0.5,
                        'source': '搜索引擎'
                    },
                    {
                        'time': "2019-11-8 15:50",
                        'title': "XXXXXXXXXX",
                        'url': "www.XXXXXX.com",
                        'score': 0.5,         # 重要程度排序，越小越靠前
                        'source': '贴吧'
                    },
                    {
                        'time': "2019-11-8 16:50",
                        'title': "XXXXXXXXXX",
                        'url': "www.XXXXXX.com",
                        'score': 0.5,
                        'source': '论坛'
                    }
                ]
            }
        }
        return JsonResponse(rev_data)

    except Exception as err:
        print(err)
        return HttpResponseServerError()