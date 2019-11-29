from django_redis import get_redis_connection
from django.http import JsonResponse, HttpResponseServerError
import simplejson
from d2Emotional.models import d2EmotionalModel
from rest_framework.views import APIView
from configuration import OUT_TIME
from check_data.check_field import CheckField
import logging
logger = logging.getLogger('django')

class LookWordView(APIView):
    # {
    #     "currentPage": "XXXXX",
    #     "pageSize": "XXXXX"
    # }

    def __init__(self):
        self.check_field = CheckField()
        super().__init__()

    def check_format(self, request):
        current_page = request.data.get('currentPage')
        page_size = request.data.get('pageSize')
        total = request.data.get('total')
        try:
            current_page = self.check_field.is_int_str(current_page)
            page_size = self.check_field.is_int_str(page_size)
            total = self.check_field.is_int_str(total)
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 1, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            return {
                'currentPage': current_page,
                'pageSize': page_size,
                'total': total
            }

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            current_page = get_data.get('currentPage')
            page_size = get_data.get('pageSize')
            total = get_data.get('total')
            word_list = []
            res = d2EmotionalModel.objects(GemotionalDeleted=0)
            total = res.count()
            for obj in res.skip((current_page - 1) * page_size).limit(page_size):
                word_list.append({
                    'number': obj['GemotionalId'],
                    'keyword': obj['GemotionalName'],
                    'classification': obj['GemotionalClassification'],
                    'attribute': obj['GemotionalAttribute'],
                    # 'forbidRemove': False,     ## 是否禁止删除
                    # 'showRemoveButton': True   ## 是否显示删除按钮
                })
            rev_data = {
                'code': 0,
                'msg': '查询成功',
                'data': {
                    'list': word_list,
                    'total': total
                }
            }
            return JsonResponse(rev_data)
