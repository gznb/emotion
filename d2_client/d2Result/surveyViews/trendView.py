from django.http import JsonResponse,  HttpResponseServerError, HttpResponseNotFound
from d2Result.check_receive_format import CheckReceiveFormat
from simplejson import loads
from d2Result.models import d2ResultModel

def trend(request):
    check_data = CheckReceiveFormat()
    # 检查输入 数据格式和参数是否正确
    get_data = check_data.is_survey_trend(loads(request.body))
    if get_data[0]:
        get_data = get_data[1]
    else:
        return HttpResponseNotFound()

    if get_data['data']['source']['isAll'] == 1:
        pass
    else:
        pass
    if get_data['data']['word']['isAll'] == 1:
        pass
    else:
        pass


    queury_list = d2ResultModel.objects(GorderId=get_data['orderId'])


    try:

        rev_data = {
            'code': 0,
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
    except Exception as err:
        print(err)
        return HttpResponseServerError()