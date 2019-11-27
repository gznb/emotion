from django.http import JsonResponse,  HttpResponseServerError
import simplejson
from django_redis import get_redis_connection
from d2Emotional.models import d2EmotionalModel
from rest_framework.views import APIView
from check_data.check_field import CheckField


class AddWordView(APIView):
    check_field = CheckField()

    def check_format(self, request):
        emotional_name = request.data.get('keyword')
        emotional_classification = request.data.get('classification')
        emotional_attribute = request.data.get('attribute')
        try:
            emotional_attribute = self.check_field.is_attribute(emotional_attribute)
        except Exception as err:
            pass

    def post(self, request, *args, **kwargs):
        pass


def add_word(request):

    try:

        conn = get_redis_connection()
        get_data = simplejson.loads(request.body)
        
        token = request.META.get('HTTP_X_TOKEN')
        # print(Ztoken)
        if token is None:
            rev_data = {'code': 1, 'msg': "身份信息失效，请重新登陆", 'data': {}}
            return JsonResponse(rev_data)
        
        telephone = conn.get(token)

        if telephone is not None:
            telephone = telephone.decode('UTF-8')
        else:
            rev_data = {'code': 1, 'msg': "身份信息失效，请重新登陆", 'data': {}}
            return JsonResponse(rev_data)

        emotional_name = get_data.get('keyword')
        emotional_classification = get_data.get('classification')
        emotional_attribute = get_data.get('attribute')

        if emotional_classification is None or emotional_attribute is None or emotional_name is None:
            rev_data = {'code': 2, 'msg': "缺少关键信息", 'data': {}}
            return JsonResponse(rev_data)
        
        # 排除空格
        emotional_name = "".join(emotional_name.split())
        emotional_classification = "".join(emotional_classification.split())
        emotional_attribute = "".join(emotional_attribute.split())
        if len(emotional_attribute) < 1 or len(emotional_name) < 1 or len(emotional_classification) < 1:
            rev_data = {'code': 2, 'msg': "缺少关键信息", 'data': {}}
            return JsonResponse(rev_data)
        # 查看是否重复
        temp = d2EmotionalModel.objects(GemotionalName=emotional_name, GemotionalClassification=emotional_classification).first()

        if temp is not None and temp['GemotionalDeleted'] == 0:
            rev_data = {'code': 3, 'msg': "此敏感词已经存在", "data":{}}
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
            # print(err)
            return HttpResponseServerError()
        else:
            rev_data = {'code': 0, 'msg': "添加成功", 'data': "{}，添加成功".format(emotional_name)}
            return JsonResponse(rev_data)
    except Exception as err:
        # print(err)
        return HttpResponseServerError()