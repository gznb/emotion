from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import simplejson
from django_redis import get_redis_connection
from d2Emotional.models import d2EmotionalModel
from configuration import OUT_TIME

def ZupdateWord(request):
    
    try:

        conn = get_redis_connection()
        get_data = simplejson.loads(request.body)
        
        Ztoken = request.META.get('HTTP_X_TOKEN')
        # print(Ztoken)
        if Ztoken is None:
            rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
            return JsonResponse(rev_data)
        
        Ztelephone = conn.get(Ztoken)

        if Ztelephone is not None:
            Ztelephone = Ztelephone.decode('UTF-8')
        else:
            rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
            return JsonResponse(rev_data)

        ZemotionalId = get_data.get('number')
        ZemotionalClassification = get_data.get('classification')
        ZemotionalAttribute = get_data.get('attribute')

        if ZemotionalId is None or ZemotionalAttribute is None or ZemotionalClassification is None:
            rev_data = {'code':1, 'msg': "缺少关键信息", 'data':{}}
            return JsonResponse(rev_data)

            # 排除空格
        ZemotionalClassification = "".join(ZemotionalClassification.split(' '))
        ZemotionalAttribute = "".join(ZemotionalAttribute.split(' '))

        if len(ZemotionalAttribute) < 1 or len(ZemotionalClassification) < 1:
                rev_data = {'code':1, 'msg': "缺少关键信息", 'data':{}}
                return JsonResponse(rev_data)
        updateWord = d2EmotionalModel.objects(GemotionalId=ZemotionalId).first()
        if updateWord is None:
            rev_data = {'code': 1, 'msg': "更新失败", 'data': "改词不存在，或者已经被删除"}
            return JsonResponse(rev_data)

        if ZemotionalClassification is not None:
            updateWord['GemotionalClassification'] = ZemotionalClassification
        
        if ZemotionalAttribute is not None:
            deleteWord['GemotionalAttribute'] = ZemotionalAttribute

        try:
            updateWord.save()
        except Exception as err:
            print(err)
            return HttpResponseServerError
        else:
            rev_data = {'code': 0, 'msg': "更新成功", 'data': {}}
            return JsonResponse(rev_data)

    except Exception as err:
        return HttpResponseServerError()