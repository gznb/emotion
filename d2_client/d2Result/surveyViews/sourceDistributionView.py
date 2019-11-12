from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def ZsourceDistribution(request):
    try:
        if request.method == "POST":
            rev_data = {
                'code': 0,
                'msg': "请求成功",
                'data': {
                    'channel': {
                        'count': 5,
                        'list': [
                            {
                                'name': '百度搜索',
                                'classification': '搜索引擎',
                                'total': 70,
                                'positive': 10,
                                'negative': 20,
                                'neutral': 40
                            },
                            {
                                'name': '360搜索',
                                'classification': '搜索引擎',
                                'total': 70,
                                'positive': 10,
                                'negative': 20,
                                'neutral': 40
                            },
                            {
                                'name': '搜狗搜索',
                                'classification': '搜索引擎',
                                'total': 70,
                                'positive': 10,
                                'negative': 20,
                                'neutral': 40
                            },
                            {
                                'name': '百度贴吧',
                                'classification': '贴吧',
                                'total': 70,
                                'positive': 10,
                                'negative': 20,
                                'neutral': 40
                            },
                            {
                                'name': '天涯论坛',
                                'classification': '论坛',
                                'total': 70,
                                'positive': 10,
                                'negative': 20,
                                'neutral': 40
                            },
                        ]
                    }
                }
            }
            return JsonResponse(rev_data)
        else:
            return HttpResponseBadRequest()
    except Exception as err:
        print(err)
        return HttpResponseServerError()