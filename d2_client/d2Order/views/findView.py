from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

def ZfindAll(request):
    try:
        if request.method == 'POST':
            rev_data = {
                "code": 0,
                "msg": "查看成功",
                "data": { 
                    "count": 1,     	# 订单数量
                    "list": [			# 具体详情
                        {
                            "orderId": 0,	# 订单 id
                            "name": "XXXX",	# 订单名
                            "word": {		# 检测词
                                "count": 2, # 检测词数量
                                "list": [	# 检测词
                                    "你好",
                                    "没钱"
                                ]
                            },
                            "negative": {    # 自定义敏感词，  现在不用
                                "count": 0,  # 词个数
                                "list": []   # 那些词
                            }
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
