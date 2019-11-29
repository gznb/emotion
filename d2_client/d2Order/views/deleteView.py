from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from rest_framework.views import APIView
from django_redis import get_redis_connection
from check_data.check_field import CheckField
from d2Order.models import d2OrderModel
from d2Result.models import d2ResultModel

import logging
logger = logging.getLogger('django')


class DeleteOrderView(APIView):

    def __init__(self):
        self.check_field = CheckField()
        self.conn = get_redis_connection()
        super().__init__()

    def check_format(self, request):
        telephone = request.data.get('telephone')
        order_id = request.data.get('orderId')
        try:
            telephone = self.check_field.is_telephon(telephone)
            order_id = self.check_field.is_order_id(order_id)
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 2, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            return {
                "telephone": telephone,
                "orderId": order_id
            }

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            telephone = get_data.get('telephone')
            order_id = get_data.get('orderId')
            try:
                d2OrderModel.objects(GuserTelephone=telephone, GorderId=order_id).update(GorderDeleted=1)
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError()
            else:
                try:
                    d2ResultModel.objects(GorderId=order_id).update(GresultDeleted=1)
                except Exception as err:
                    logger.error(err)
                    return HttpResponseServerError()
                else:
                    self.conn.set('ORDER_LIST_FLAG', 0)
                    self.conn.set('CRAWLED_URL_SET_FLAG', 0)
                    return JsonResponse({'code': 0, 'msg': '订单删除成功', 'data': {}})

