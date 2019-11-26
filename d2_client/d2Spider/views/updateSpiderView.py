from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import simplejson
from django_redis import get_redis_connection
from d2Spider.models import d2SpiderModel
from configuration import OUT_TIME
from mongoengine.errors import NotUniqueError
def ZupdateSpider(request):
    
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

        ZspiderId = get_data.get('number')
        ZspiderName = get_data.get('web_name')
        ZspiderRegion = get_data.get('web_region')
        ZspiderClassification = get_data.get('web_classification')
        ZspiderDomain = get_data.get('source')
        if ZspiderName is None or ZspiderDomain is None or ZspiderClassification is None or ZspiderRegion is None:
            rev_data = {'code':1, 'msg': "缺少关键信息", 'data':{}}
            return JsonResponse(rev_data)

            # 排除空格
        ZspiderName = "".join(ZspiderName.split(' '))
        ZspiderRegion = "".join(ZspiderRegion.split(' '))
        ZspiderClassification = "".join(ZspiderClassification.split(' '))
        ZspiderDomain = "".join(ZspiderDomain.split(' '))

        if len(ZspiderName) < 1 or len(ZspiderRegion) < 1 or len(ZspiderClassification) < 1 or len(ZspiderDomain) < 1:
                rev_data = {'code':1, 'msg': "缺少关键信息", 'data':{}}
                return JsonResponse(rev_data)

        updateSpider = d2SpiderModel.objects(GspiderId=ZspiderId).first()

        if updateSpider is None:
            rev_data = {'code': 1, 'msg': "更新失败", 'data': "改词不存在，或者已经被删除"}
            return JsonResponse(rev_data)

        if ZspiderName is not None:
            updateSpider['GspiderName'] = ZspiderName
        
        if ZspiderRegion is not None:
            updateSpider['GspiderRegion'] = ZspiderRegion

        if ZspiderClassification is not None:
            updateSpider['GspiderClassification'] = ZspiderClassification

        if ZspiderDomain is not None:
            updateSpider['GspiderDomain'] = ZspiderDomain

        try:
            updateSpider.save()
        except NotUniqueError as err:
            rev_data = {'code':1, 'msg': "域名冲突，域名应该唯一", 'data':{}}
            return JsonResponse(rev_data)
        except Exception as err:
            # print(err)
            return HttpResponseServerError
        else:
            rev_data = {'code': 0, 'msg': "更新成功", 'data': {}}
            return JsonResponse(rev_data)

    except Exception as err:
        return HttpResponseServerError()