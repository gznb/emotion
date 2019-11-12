from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def Ztrend(request):
    try:
        if request.method == "POST":
            rev_data = {
                'code':0,
                'msg': "成功",
                'data': {
                    'count': 4,
                    'list': [
                        {
                            'time': '15:20',   
                            'thisInfoCounts': 10,   
                            'thisNegativeCounts': 5,  
                            'lastInfoCounts':8,
                            'lastNegativeCounts':3	 
                        },
                        {
                            'time': '16:20',
                            'thisInfoCounts': 10,
                            'thisNegativeCounts': 5,
                            'lastInfoCounts':8,
                            'lastNegativeCounts':3
                        },
                        {
                            'time': '16:20',
                            'thisInfoCounts': 10,
                            'thisNegativeCounts': 5,
                            'lastInfoCounts':8,
                            'lastNegativeCounts':3
                        },
                        {
                            'time': '16:20',
                            'thisInfoCounts': 10,
                            'thisNegativeCounts': 5,
                            'lastInfoCounts':8,
                            'lastNegativeCounts':3
                        }
                    ]
                }
            }
            return JsonResponse(rev_data)
        else:
            return HttpResponseBadRequest()
    except Exception as err:
        print(err)
        return HttpResponseServerError()