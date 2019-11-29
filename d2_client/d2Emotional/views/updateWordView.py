from django.http import JsonResponse,  HttpResponseServerError
import simplejson
from django_redis import get_redis_connection
from d2Emotional.models import d2EmotionalModel
from rest_framework.views import APIView
from check_data.check_field import CheckField
import logging
logger = logging.getLogger('django')


class UpdateWordView(APIView):

    def __init__(self):
        self.check_field = CheckField()
        super().__init__()

    def check_format(self, request):
        emotional_id = request.data.get('number')
        emotional_classification = request.data.get('classification')
        emotional_attribute = request.data.get('attribute')
        try:
            emotional_name = self.check_field.is_int_str(emotional_id)
            emotional_classification = self.check_field.is_str(emotional_classification)
            emotional_attribute = self.check_field.is_attribute(emotional_attribute)
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 1, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            return {
                'number': emotional_name,
                'classification': emotional_classification,
                'attribute': emotional_attribute
            }

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            emotional_id = get_data.get('number')
            emotional_classification = get_data.get('classification')
            emotional_attribute = get_data.get('attribute')
            update_this_word = d2EmotionalModel.objects(GemotionalId=emotional_id, GemotionalDeleted=0).first()
            if update_this_word is None:
                rev_data = {'code': 1, 'msg': "更新失败", 'data': "改词不存在，或者已经被删除"}
                return JsonResponse(rev_data)

            if emotional_classification is not None:
                update_this_word['GemotionalClassification'] = emotional_classification

            if emotional_attribute is not None:
                update_this_word['GemotionalAttribute'] = emotional_attribute

            try:
                update_this_word.save()
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError
            else:
                rev_data = {'code': 0, 'msg': "更新成功", 'data': {}}
                return JsonResponse(rev_data)