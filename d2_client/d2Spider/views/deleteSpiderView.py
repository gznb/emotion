from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import simplejson
from django_redis import get_redis_connection
from d2Spider.models import d2SpiderModel
from rest_framework.views import APIView
from check_data.check_field import CheckField

import logging
logger = logging.getLogger('django')

class DeleteSpiderView(APIView):

    def __init__(self):
        self.check_field = CheckField()
        super().__init__()

    def check_format(self, request):
        order_id = request.data.get('number')
        try:
            order_id = self.check_field.is_order_id(order_id)
        except (TypeError, ValueError) as err:
            return JsonResponse({'code':2, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError
        else:
            return {
                'number': order_id
            }

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            order_id = get_data.get('number')
            delete_spider = d2SpiderModel.objects(GspiderId=order_id).first()
            delete_spider['GspiderDeleted'] = 1
            try:
                delete_spider.save()
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError()
            else:
                rev_data = {'code': 0, 'msg': "删除成功", 'data': {}}
                return JsonResponse(rev_data)
