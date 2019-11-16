from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import simplejson
from django_redis import get_redis_connection
from d2Emotional.models import d2EmotionalModel
from configuration import OUT_TIME

def ZaddWord(request):

    try:

        conn = get_redis_connection()
        get_data = simplejson.loads(request.body)
        
        Ztoken = request.META.get('HTTP_X_TOKEN')
        # print(Ztoken)
        if Ztoken is None:
            rev_data = {'code': 1, 'msg': "身份信息失效，请重新登陆", 'data': {}}
            return JsonResponse(rev_data)
        
        Ztelephone = conn.get(Ztoken)

        if Ztelephone is not None:
            Ztelephone = Ztelephone.decode('UTF-8')
        else:
            rev_data = {'code': 1, 'msg': "身份信息失效，请重新登陆", 'data': {}}
            return JsonResponse(rev_data)

        ZemotionalName = get_data.get('keyword')
        ZemotionalClassification = get_data.get('classification')
        ZemotionalAttribute = get_data.get('attribute')

        if ZemotionalClassification is None or ZemotionalAttribute is None or ZemotionalName is None:
            rev_data = {'code':2, 'msg': "缺少关键信息", 'data':{}}
            return JsonResponse(rev_data)
        
        # 排除空格
        ZemotionalName = "".join(ZemotionalName.split())
        ZemotionalClassification = "".join(ZemotionalClassification.split())
        ZemotionalAttribute = "".join(ZemotionalAttribute.split())
        if len(ZemotionalAttribute) < 1 or len(ZemotionalName) < 1 or len(ZemotionalClassification) < 1:
                rev_data = {'code':2, 'msg': "缺少关键信息", 'data':{}}
                return JsonResponse(rev_data)
        # 查看是否重复
        temp = d2EmotionalModel.objects(GemotionalName=ZemotionalName, GemotionalClassification=ZemotionalClassification).first()
        

        if temp is not None and temp['GemotionalDeleted'] == 0:
            rev_data = {'code': 3, 'msg': "此敏感词已经存在", "data":{}}
            return JsonResponse(rev_data)

        if temp is not None and temp['GemotionalDeleted'] == 1:
            temp['GemotionalDeleted'] = 0

        
        newEmotional = d2EmotionalModel(
            GemotionalId = d2EmotionalModel.objects.count(),
            GemotionalName = ZemotionalName,
            GemotionalClassification = ZemotionalClassification,
            GemotionalAttribute = ZemotionalAttribute
        )
        try:
            if temp is not None:
                temp.save()
            else:
                newEmotional.save()
        except Exception as err:
            print(err)
            return HttpResponseServerError()
        else:
            rev_data = {'code': 0, 'msg': "添加成功", 'data': "{}，添加成功".format(ZemotionalName)}
            return JsonResponse(rev_data)


    except Exception as err:
        print(err)
        return HttpResponseServerError()