from django.http import JsonResponse,  HttpResponseServerError
import simplejson
from django_redis import get_redis_connection
from d2Emotional.models import d2EmotionalModel
from rest_framework.views import APIView
from check_data.check_field import CheckField
import logging
logger = logging.getLogger('django')

class AddWordView(APIView):

    def __init__(self):
        self.check_field = CheckField()
        super().__init__()

    def check_format(self, request):
        emotional_name = request.data.get('keyword')
        emotional_classification = request.data.get('classification')
        emotional_attribute = request.data.get('attribute')
        try:
            emotional_name = self.check_field.is_str(emotional_name)
            emotional_classification = self.check_field.is_str(emotional_classification)
            emotional_attribute = self.check_field.is_attribute(emotional_attribute)
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 1, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            return {
                'keyword': emotional_name,
                'classification': emotional_classification,
                'attribute': emotional_attribute
            }

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            emotional_name = get_data['keyword']
            emotional_classification = get_data['classification']
            emotional_attribute = get_data['attribute']

            temp = d2EmotionalModel.objects(GemotionalName=emotional_name,
                                            GemotionalClassification=emotional_classification).first()

            if temp is not None and temp['GemotionalDeleted'] == 0:
                rev_data = {'code': 3, 'msg': "此敏感词已经存在", "data": {}}
                return JsonResponse(rev_data)

            if temp is not None and temp['GemotionalDeleted'] == 1:
                temp['GemotionalDeleted'] = 0

            new_emotional = d2EmotionalModel(
                GemotionalId=d2EmotionalModel.objects.count(),
                GemotionalName=emotional_name,
                GemotionalClassification=emotional_classification,
                GemotionalAttribute=emotional_attribute
            )
            try:
                if temp is not None:
                    temp.save()
                else:
                    new_emotional.save()
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError()
            else:
                rev_data = {'code': 0, 'msg': "添加成功", 'data': "{}，添加成功".format(emotional_name)}
                return JsonResponse(rev_data)
