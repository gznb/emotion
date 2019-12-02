from rest_framework.views import APIView
from check_data.check_field import CheckField
from django.http import JsonResponse, HttpResponseServerError
from d2Result.models import d2ResultModel
from django_redis import get_redis_connection
import logging
logger = logging.getLogger('django')


class DeletedView(APIView):

    def __init__(self):
        self.check_field = CheckField()
        self.conn = get_redis_connection()
        super().__init__()

    def check_format(self, request):
        order_id = request.data.get('orderId')
        url_list = request.data.get('urls')

        try:
            order_id = self.check_field.is_order_id(order_id)
            u_list = []
            for url in url_list:
                r = self.check_field.is_url(url)
                u_list.append(r)
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 2, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            return {
                'orderId': order_id,
                'urls': u_list
            }

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            order_id = get_data.get('orderId')
            url_list = get_data.get('urls')
            try:
                count = d2ResultModel.objects(GorderId=order_id,
                                              GresultDeleted=0,
                                              GresultRealUrl__in=url_list).update(GresultDeleted=1)
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError()
            else:
                self.conn.set('CRAWLED_URL_SET_FLAG', 0)
        return JsonResponse({'code': 0, 'msg': '成功删除{}条'.format(count), 'data': {}})
