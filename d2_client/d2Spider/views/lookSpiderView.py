from django_redis import get_redis_connection
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import simplejson
from d2Spider.models import d2SpiderModel
from configuration import OUT_TIME

def ZlookSpider(request):
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
        spider_list = []
        res = d2SpiderModel.objects(GspiderDeleted=0)
        total = res.count()
        for obj in res.skip((currentPage-1)*pageSize).limit(pageSize):
            spider_list.append({
                'number': obj['GspiderId'],
                'source': obj['GspiderDomain'],
                'web_name': obj['GspiderName'],
                'web_classification': obj['GspiderClassification'],
                'web_region': obj['GspiderRegion']
                # 'forbidRemove': False,     ## 是否禁止删除
                # 'showRemoveButton': True   ## 是否显示删除按钮
            })
        rev_data = {
            'code': 0,
            'msg':'查询成功',
            'data': {
                'list': spider_list,
                'total': total
            }
        }
        conn.expire(Ztoken, OUT_TIME)
        return JsonResponse(rev_data)

    except Exception as err:
        return HttpResponseServerError() 
