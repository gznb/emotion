from django_redis import get_redis_connection
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import simplejson
from d2Emotional.models import d2EmotionalModel
import pprint
from configuration import OUT_TIME
def ZlookWordsView(request):
    try:

        # 验证
        conn = get_redis_connection()
        get_data = simplejson.loads(request.body)
        Ztoken = request.META.get('HTTP_X_TOKEN')
        if Ztoken is None:
            rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
            return JsonResponse(rev_data)  
        Ztelephone = conn.get(Ztoken)

        if Ztelephone is not None:
            Ztelephone = Ztelephone.decode('UTF-8')
        else:
            rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
            return JsonResponse(rev_data)
        currentPage = get_data['currentPage']       # 当前页
        pageSize = get_data['pageSize']             # 页面大小
        total = get_data['total']                   # 一共多少条
    
        # 关键信息不存在
        if currentPage is None or pageSize is None or total is None:
            rev_data = {'code':1, 'msg': "关键信息不存在", 'data':{}}
            return JsonResponse(rev_data)
        word_list = []
        res = d2EmotionalModel.objects(GemotionalDeleted=0)
        total = res.count()
        for obj in res.skip((currentPage-1)*pageSize).limit(pageSize):
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
            'msg':'查询成功',
            'data': {
                'list': word_list,
                'total': total
            }
        }
        conn.expire(Ztoken, OUT_TIME)
        return JsonResponse(rev_data)

    except Exception as err:
        print(err)
        return HttpResponseServerError()