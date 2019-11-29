from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from rest_framework.views import APIView
from check_data.check_field import CheckField
from d2Order.models import d2OrderModel

import logging
logger = logging.getLogger('django')


class FindAllOrderView(APIView):

    def __init__(self):
        self.check_field = CheckField()
        super().__init__()

    def check_format(self, request):
        telephone = request.data.get('telephone')
        try:
            telephone = self.check_field.is_telephon(telephone)
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 2, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            return {
                'telephone': telephone
            }

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            telephone = get_data.get('telephone')
            order_list = d2OrderModel.objects(GuserTelephone=telephone)
            rev_order_list = list()
            # print(order_list)
            for order in order_list:

                d = {
                    'orderId': order.GorderId,
                    'name': order.GorderName,
                    'word': {
                        'count': len(order.GorderKeywordList),
                        'list': order.GorderKeywordList
                    },
                    'negative': {
                        'count': len(order.GorderNegativeList),
                        'list': order.GorderNegativeList
                    }
                }
                rev_order_list.append(d)
            return JsonResponse({'code': 0, 'msg': '成功', 'data': {'count':len(rev_order_list), 'list':rev_order_list}})

