from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Zdetailed(request):
    try:

        rev_data = {
            'code': 0,
            'msg': "成功",
            'data': {
                'page': {
                    'position': 1,
                    'count': 20
                },
                'total': 3,
                'list': [
                    {
                        'url': "www.XXXX.com",
                        'title': "XXXXXX",
                        'attribute': '中性',
                        'channel': '百度搜索',
                        'content': '此渠道不包括正文',
                        'crowTime': '2019-11-8 11:20',
                        'releaseTime': '2019-11-8 11:10',
                        'keyword': '太平洋'
                    },
                    {
                        'url': "www.XXXX.com",
                        'title': "XXXXXX",
                        'attribute': '中性',
                        'channel': '百度搜索',
                        'content': '此渠道不包括正文',
                        'crowTime': '2019-11-8 11:20',
                        'releaseTime': '2019-11-8 11:10',
                        'keyword': '太平洋'
                    },
                    {
                        'url': "www.XXXX.com",
                        'title': "XXXXXX",
                        'attribute': '中性',
                        'channel': '百度搜索',
                        'content': '此渠道不包括正文',
                        'crowTime': '2019-11-8 11:20',
                        'releaseTime': '2019-11-8 11:10',
                        'keyword': '太平洋'
                    }
                ]
            }
        }
        return JsonResponse(rev_data)

    except Exception as err:
        print(err)
        return HttpResponseServerError()