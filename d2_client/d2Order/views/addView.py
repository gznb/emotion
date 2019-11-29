from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import simplejson
from d2Order.models import d2OrderModel
import datetime
from rest_framework.views import APIView
from check_data.check_field import CheckField
from django_redis import get_redis_connection
import logging
logger = logging.getLogger('django')

class AddOrderView(APIView):
    def __init__(self):
        self.check_field = CheckField()
        self.conn = get_redis_connection()
        super().__init__()

    def check_format(self, request):
        telephone = request.data.get('telephone')
        data = request.data.get('data')
        if data is None:
            return JsonResponse({'code': 2, 'msg': '关键信息缺失', 'data': {}})

        order_name = data.get('orderName')
        word = data.get('word')
        if word is None:
            return JsonResponse({'code': 2, 'msg': '关键信息缺失', 'data': {}})
        word_list = word.get('list')
        negative = data.get('negative')
        if negative is None:
            return JsonResponse({'code': 2, 'msg': '关键信息缺失', 'data': {}})
        negative_list = negative.get('list')
        try:
            telephone = self.check_field.is_telephon(telephone)
            order_name = self.check_field.is_str(order_name)
            if not word_list:
                word_list = [w for w in word_list if self.check_field.is_str(w)]
            if not negative_list:
                negative_list = [n for n in negative_list if self.check_field.is_str(n)]
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 2, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            return {
                'telephone': telephone,
                'data': {
                    'orderName': order_name,
                    'word': {
                        'count': len(word_list),
                        'list': word_list
                    },
                    'negative': {
                        'count': len(negative_list),
                        'list': negative_list
                    }
                }
            }

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            telephone = get_data['telephone']
            data = get_data['data']
            order_name = data['orderName']
            word = data['word']
            word_list = word['list']
            negative = data['negative']
            negative_list = negative['list']
            old_order_list = d2OrderModel.objects(GuserTelephone=telephone)
            # 如果新建的订单的关键词列表是以前的一个关键词列表的子集，就不能被创建
            for old_order in old_order_list:
                old_word_list = old_order.GorderKeywordList
                flag = [False for c in word_list if c not in old_word_list]
                if not flag:
                    return JsonResponse({'code': 2, 'msg': '订单可能重复，请检查', 'data': {}})
            init_last_time = datetime.datetime.strptime('1981-11-11 11:11:11', '%Y-%m-%d %H:%M:%S')
            counts = d2OrderModel.objects().count()
            order = d2OrderModel(
                GorderId=counts,
                GorderName=order_name,
                GorderKeywordList=word_list,
                GorderLastTime=init_last_time,
                GuserTelephone=telephone,
                GorderSpiderList='1' * 100,
                GorderCreateTime=datetime.datetime.now(),
                GorderNegativeList=negative_list
            )
            try:
                order.save()
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError()
            else:
                """
                {
                    'orderId': 2, 
                    'orderName': '负面测试', 
                    'userTelephone': '15200697520', 
                    'orderCreateTime': '2019-11-17 23:08:12', 
                    'orderRemainingTimes': 1000000, 
                    'orderLastTime': '1981-11-11 11:11:11', 
                    'orderSpiderList': '1111111111', 
                    'word': {
                        'count': 3, 
                        'list': ['内幕', '违法项目', '违法盈利']
                        }, 
                    'negative': {
                        'count': 0, 
                        'list': []
                    }
                }
                """
                rev_data = {
                    'code': 0,
                    'msg': "添加成功",
                    'data': {}
                }
                self.conn.set('ORDER_LIST_FLAG', 0)
                return JsonResponse(rev_data)
