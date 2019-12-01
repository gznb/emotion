from django.http import JsonResponse, HttpResponseServerError
from d2Result.utils.check_get_data import CheckReceiveFormat
from rest_framework.views import APIView
from d2Spider.models import d2SpiderModel
from d2Result.models import d2ResultModel
from conf.time_conf import DATETIME_FORMAT_STR
import logging
logger = logging.getLogger('django')

class SnapshotView(APIView):

    def check_format(self, request):
        order_id = request.data.get('orderId')
        url = request.data.get('url')
        check = CheckReceiveFormat()
        try:
            order_id = check.check_order_id({'orderId':order_id})
            url = check.check_url({'url':url})
        except (TypeError, ValueError) as err:
            return JsonResponse({'code':2, 'msg': str(err), 'data':{}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError
        else:
            return {
                'orderId': order_id,
                'url': url
            }


    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (HttpResponseServerError, JsonResponse)):
            return get_data
        else:
            res = d2ResultModel.objects(GorderId=get_data['orderId'], GresultRealUrl=get_data['url']).first()
            if res is None:
                return JsonResponse({'code': 0, 'msg': '该订单下url快照不存在', 'data':{}})
            else:
                spider = d2SpiderModel.objects(GspiderId=res.GspiderId).first()
                data = {
                    'title': res['GresultTitle'].strip(),
                    'releaseTime': res['GresultReleaseTime'].strftime(DATETIME_FORMAT_STR),
                    'attribute': res['GresultAttribute'],
                    'keyword': res['GresultKeyword'],
                    'source': spider['GspiderClassification'],
                    'channel': spider['GspiderName'],
                    'content': res['GresultDetailedInformating'].strip() if res['GresultDetailedInformating'] else "此渠道不包括正文",
                    'url': 'GresultRealUrl'
                }
                return JsonResponse({'code':0, 'msg':'成功', 'data': data})