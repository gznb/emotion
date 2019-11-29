from django.http import JsonResponse,  HttpResponseServerError
from d2Spider.models import d2SpiderModel
from rest_framework.views import APIView
from mongoengine.errors import NotUniqueError
from check_data.check_field import CheckField
import logging
logger = logging.getLogger('django')


class UpdateSpiderView(APIView):
    def __init__(self):
        self.check_field = CheckField()
        super().__init__()

    def check_format(self, request):
        spider_id = request.data.get('number')
        spider_name = request.data.get('web_name')
        spider_region = request.data.get('web_region')
        spider_classification = request.data.get('web_classification')
        spider_domain = request.data.get('source')
        try:
            spider_id = self.check_field.is_int_str(spider_id)
            spider_name = self.check_field.is_str(spider_name)
            spider_region = self.check_field.is_str(spider_region)
            spider_classification = self.check_field.is_str(spider_classification)
            spider_domain = self.check_field.is_url(spider_domain)
        except (TypeError, ValueError) as err:
            return JsonResponse({'code':2, 'msg': str(err), 'data':{}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            return {
                'number' : spider_id,
                'web_name': spider_name,
                'web_region': spider_region,
                'web_classification': spider_classification,
                'source': spider_domain
            }

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            spider_id = get_data.get('number')
            spider_name = get_data.get('web_name')
            spider_region = get_data.get('web_region')
            spider_classification = get_data.get('web_classification')
            spider_domain = get_data.get('source')

            updateSpider = d2SpiderModel.objects(GspiderId=spider_id).first()

            if updateSpider is None:
                rev_data = {'code': 1, 'msg': "更新失败", 'data': "改词不存在，或者已经被删除"}
                return JsonResponse(rev_data)

            if spider_name is not None:
                updateSpider['GspiderName'] = spider_name

            if spider_region is not None:
                updateSpider['GspiderRegion'] = spider_region

            if spider_classification is not None:
                updateSpider['GspiderClassification'] = spider_classification

            if spider_domain is not None:
                updateSpider['GspiderDomain'] = spider_domain

            try:
                updateSpider.save()
            except NotUniqueError as err:
                rev_data = {'code': 1, 'msg': "域名冲突，域名应该唯一", 'data': {}}
                return JsonResponse(rev_data)
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError
            else:
                rev_data = {'code': 0, 'msg': "更新成功", 'data': {}}
                return JsonResponse(rev_data)
