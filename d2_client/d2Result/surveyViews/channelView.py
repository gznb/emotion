from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Zchannel(request):
    try:

        rev_data = {
            'code': 0,
            'msg': '成功',
            'data': {
                'channel': {
                    'count': 5,
                    'list': [
                        {
                            'name': '百度搜索',
                            'total': 20,
                            'positive': 2,
                            'negative': 10,
                            'neutral': 8,
                        },
                        {
                            'name': '360搜索',
                            'total': 30,
                            'positive': 2,
                            'negative': 10,
                            'neutral': 18,
                        },
                        {
                            'name': '搜狗搜索',
                            'total': 40,
                            'positive': 2,
                            'negative': 10,
                            'neutral': 28,
                        },
                        {
                            'name': '百度贴吧',
                            'total': 50,
                            'positive': 2,
                            'negative': 10,
                            'neutral': 38,
                        },
                        {
                            'name': '天涯论坛',
                            'total': 60,
                            'positive': 2,
                            'negative': 10,
                            'neutral': 48,
                        },
                    ]
                }
            }
        }
        return JsonResponse(rev_data)

    except Exception as err:
        print(err)
        return HttpResponseServerError()