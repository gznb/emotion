from django.http import JsonResponse, HttpResponseServerError
from d2Emotional.models import d2EmotionalModel
from rest_framework.views import APIView
from check_data.check_field import CheckField
import logging
logger = logging.getLogger('django')


class DeleteWordView(APIView):

    def __init__(self):
        self.check_field = CheckField()
        super().__init__()

    def check_format(self, request):
        number = request.data.get('number')
        try:
            number = self.check_field.is_int_str(number)
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 1, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            return {
                'number': number
            }

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            emotional_id = get_data.get('number')
            delete_this_word = d2EmotionalModel.objects(GemotionalId=emotional_id).first()
            delete_this_word['GemotionalDeleted'] = 1
            try:
                delete_this_word.save()
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError()
            else:
                rev_data = {'code': 0, 'msg': "删除成功", 'data': {}}
                return JsonResponse(rev_data)
