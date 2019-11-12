from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Zinitialization(request):
    try:
        if request.method == "POST":
            rev_data = {
                'code': 0,
                'msg': "查询成功",
                'data': {
                    'infoCounts': 100,  # 整体信息量
                    'negativeCounts': 70, # 负面信息量
                    'mainsource': {			# 负面主要来源
                        'name': "百度搜索", # 来源名字
                        'count': 40			# 来源条数
                    },
                    "source": {
                        "isAll": 1,
                        "count": 4,
                        "list": ["搜索引擎", "报纸", "贴吧", "论坛"]
                    },
                    'word': {
                        'count': 2,
                        'list': ['太平洋集团', '严介和']
                    },
                    'data': {
                        'timeInterval': 1,   #  1天，开始时间和结束时间间隔一天，同时，周期的间隔时间也是一天，默认为1天
                        
                        'thisPeriod': {      # 当前周期
                            'beginTime': '2019-11-8 15:21',  # 开始的时间
                            'endTime':  '2019-11-9  15:21'  # 结束的时间
                        }
                    }
                    
                }
            }
            return JsonResponse(rev_data)
        else:
            return HttpResponseBadRequest()
    except Exception as err:
        print(err)
        return HttpResponseBadRequest()