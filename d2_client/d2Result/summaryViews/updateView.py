from django.http import JsonResponse, HttpResponseServerError
from rest_framework.views import APIView
from d2Result.models import d2ResultModel
from d2Order.models import d2OrderModel
from d2Result.utils.check_get_data import CheckReceiveFormat

import logging
logger = logging.getLogger('django')

class UpdateView(APIView):

    def check_format(self, request):
        order_id = request.data.get('orderId')
        data = request.data.get('data')
        result = data.get('result')
        check = CheckReceiveFormat()
        try:
            order_id = check.check_order_id({'orderId': order_id})
            attribute, u_count, u_list = check.check_result(result)
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 2, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            get_data = {
                'orderId': order_id,
                'data': {
                    'result': {
                        'attribute': attribute,
                        'count': u_count,
                        'list': u_list
                    }
                }
            }
            return get_data


    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            url_list = get_data['data']['result']['list']
            attribute = get_data['data']['result']['attribute']
            try:
                count = d2ResultModel.objects(GresultRealUrl__in=url_list, GresultDeleted=0).update(GresultAttribute=attribute)
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError()
        return JsonResponse({'code':0, 'msg':'成功更新{}条'.format(count), 'data':{}})
