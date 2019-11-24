from django.http import JsonResponse,  HttpResponseServerError
import simplejson
from django_redis import get_redis_connection
from d2Emotional.models import d2EmotionalModel


def update_word(request):
    # noinspection PyBroadException
    try:
        conn = get_redis_connection()
        get_data = simplejson.loads(request.body)
        
        token = request.META.get('HTTP_X_TOKEN')
        # print(token)
        if token is None:
            rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
            return JsonResponse(rev_data)
        
        telephone = conn.get(token)

        if telephone is not None:
            telephone = telephone.decode('UTF-8')
        else:
            rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
            return JsonResponse(rev_data)

        emotional_id = get_data.get('number')
        emotional_classification = get_data.get('classification')
        emotional_attribute = get_data.get('attribute')

        if emotional_id is None or emotional_attribute is None or emotional_classification is None:
            rev_data = {'code':1, 'msg': "缺少关键信息", 'data':{}}
            return JsonResponse(rev_data)

            # 排除空格
        emotional_classification = "".join(emotional_classification.split(' '))
        emotional_attribute = "".join(emotional_attribute.split(' '))

        if len(emotional_attribute) < 1 or len(emotional_classification) < 1:
            rev_data = {'code': 1, 'msg': "缺少关键信息", 'data': {}}
            return JsonResponse(rev_data)
        update_this_word = d2EmotionalModel.objects(GemotionalId=emotional_id).first()
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
            print(err)
            return HttpResponseServerError
        else:
            rev_data = {'code': 0, 'msg': "更新成功", 'data': {}}
            return JsonResponse(rev_data)
    except Exception as err:
        return HttpResponseServerError()