
from django.http import JsonResponse, HttpResponseServerError
import simplejson
from django_redis import get_redis_connection
from d2Emotional.models import d2EmotionalModel


def delete_word(request):
    # 关闭 Exception 使用警告
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
        delete_this_word = d2EmotionalModel.objects(GemotionalId=emotional_id).first()
        delete_this_word['GemotionalDeleted'] = 1
        try:
            delete_this_word.save()
        except Exception as err:
            # print(err)
            return HttpResponseServerError
        else:
            rev_data = {'code': 0, 'msg': "删除成功", 'data': {}}
            return JsonResponse(rev_data)
    except Exception as err:
        return HttpResponseServerError()