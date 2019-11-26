from django_redis import get_redis_connection
from django.http import JsonResponse, HttpResponseServerError
import simplejson
from d2Emotional.models import d2EmotionalModel

from configuration import OUT_TIME


def look_words(request):
    try:
        # 验证
        conn = get_redis_connection()
        get_data = simplejson.loads(request.body)
        token = request.META.get('HTTP_X_TOKEN')
        if token is None:
            rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
            return JsonResponse(rev_data)  
        telephone = conn.get(token)

        if telephone is not None:
            telephone = telephone.decode('UTF-8')
        else:
            rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
            return JsonResponse(rev_data)
        current_page = get_data['currentPage']       # 当前页
        page_size = get_data['pageSize']             # 页面大小
        total = get_data['total']                   # 一共多少条
    
        # 关键信息不存在
        if current_page is None or page_size is None or total is None:
            rev_data = {'code': 1, 'msg': "关键信息不存在", 'data': {}}
            return JsonResponse(rev_data)
        word_list = []
        res = d2EmotionalModel.objects(GemotionalDeleted=0)
        total = res.count()
        for obj in res.skip((current_page-1)*page_size).limit(page_size):
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
        conn.expire(token, OUT_TIME)
        return JsonResponse(rev_data)

    except Exception as err:
        # print(err)
        return HttpResponseServerError()