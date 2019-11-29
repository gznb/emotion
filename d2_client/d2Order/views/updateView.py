from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import logging
from d2Order.models import d2OrderModel
from check_data.check_field import CheckField
from django_redis import get_redis_connection
from rest_framework.views import APIView
logger = logging.getLogger('django')

class UpdateOrderView(APIView):
    def __init__(self):
        self.check_field = CheckField()
        self.conn = get_redis_connection()
        super().__init__()

    def check_format(self, request):
        telephone = request.data.get('telephone')
        order_id = request.data.get('orderId')
        order_name = ''
        word_list = []
        negative_list = []
        try:
            telephone = self.check_field.is_telephon(telephone)
            order_id = self.check_field.is_order_id(order_id)
            data = request.data.get('data')
            if data:
                order_name = data.get('orderName')
                if order_name:
                    order_name = self.check_field.is_str(order_name)
                word = data.get('word')
                if word:
                    count = word.get('count')
                    word_list = word.get('list')
                    if word_list:
                        word_list = [w for w in word_list if self.check_field.is_str(w)]
                negative = data.get('negative')
                if negative:
                    count = negative.get('negative')
                    negative_list = negative.get('list')
                    if negative_list:
                        negative_list = [n for n in negative_list if self.check_field.is_str(n)]
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 2, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            return {
                'telephone': telephone,
                'orderId': order_id,
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
            telephone = get_data.get('telephone')
            order_id = get_data.get('orderId')
            new_order = d2OrderModel.objects(GuserTelephone=telephone, GorderId=order_id).first()
            if new_order:
                data = get_data.get('data')
                if data:
                    order_name = data.get('orderName')
                    if order_name:
                        new_order.GorderName = order_name
                    word = data.get('word')
                    if word:
                        word_list = word.get('list')
                        if word_list:
                            old_order_list = d2OrderModel.objects(GuserTelephone=telephone)
                            for old_order in old_order_list:
                                old_word_list = old_order.GorderKeywordList
                                flag = [False for c in word_list if c not in old_word_list]
                                if not flag:
                                    return JsonResponse({'code': 2, 'msg': '订单可能重复，请检查', 'data': {}})
                            new_order.GorderKeywordList = word_list
                    negative = data.get('negative')
                    if negative:
                        negative_list = negative.get('list')
                        if negative_list:
                            new_order.GorderNegativeList = negative_list
                    try:
                        new_order.save()
                    except Exception as err:
                        logger.error(err)
                        return HttpResponseServerError()
                    else:
                        self.conn.set('CRAWLED_URL_SET_FLAG', 0)
                        self.conn.set('ORDER_LIST_FLAG', 0)
                        return JsonResponse({'code': 0, 'msg': '更新成功', 'data': {}})
            else:
                return JsonResponse({'code': 2, 'msg': "该订单不存在", 'data': {}})
