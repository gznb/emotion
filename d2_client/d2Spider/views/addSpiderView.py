from django.http import JsonResponse, HttpResponseServerError
import simplejson
from d2Spider.models import d2SpiderModel
from rest_framework.views import APIView
from check_data.check_field import CheckField
import logging
logger = logging.getLogger('django')


class AddSpiderView(APIView):

    def __init__(self):
        self.check_field = CheckField()
        super().__init__()

    def check_format(self, request):
        spider_name = request.data.get('web_name')
        spider_classification = request.data.get('web_classification')
        spider_region = request.data.get('web_region')
        spider_domain = request.data.get('source')
        try:
            spider_name = self.check_field.is_str(spider_name)
            spider_classification = self.check_field.is_str(spider_classification)
            spider_region = self.check_field.is_str(spider_region)
            spider_domain = self.check_field.is_url(spider_domain)
        except (ValueError, TypeError) as err:
            return JsonResponse({'code': 2, 'msg': str(err), 'data':{}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            return {
                'web_name': spider_name,
                'web_classification': spider_classification,
                'web_region': spider_region,
                'source': spider_domain
            }

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            spider_name = get_data.get('web_name')
            spider_classification = get_data.get('web_classification')
            spider_region = get_data.get('web_region')
            spider_domain = get_data.get('source')

            temp = d2SpiderModel.objects(GspiderDomain=spider_domain).first()

            if temp is not None and temp['GspiderDeleted'] == 0:
                rev_data = {'code': 1, 'msg': "此网站已经存在", "data": {}}
                return JsonResponse(rev_data)

            if temp is not None and temp['GspiderDeleted'] == 1:
                temp['GspiderDeleted'] = 0

            new_spider = d2SpiderModel(
                GspiderId=d2SpiderModel.objects.count(),
                GspiderName=spider_name,
                GspiderClassification=spider_classification,
                GspiderRegion=spider_region,
                GspiderDomain=spider_domain
            )
            try:
                if temp is not None:
                    temp.save()
                else:
                    new_spider.save()
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError()
            else:
                rev_data = {'code': 0, 'msg': "添加成功", 'data': "{}，添加成功".format(spider_name)}
                return JsonResponse(rev_data)
