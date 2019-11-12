from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import simplejson
from django_redis import get_redis_connection
from d2Spider.models import d2SpiderModle
from configuration import OUT_TIME

def ZaddSpider(request):

    try:
        if request.method == "POST":
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
            
            ZspiderName = get_data.get('web_name')
            ZspiderClassification = get_data.get('web_classification')
            ZspiderRegion = get_data.get('web_region')
            ZspiderDomain = get_data.get('source')


            if ZspiderName is None or ZspiderClassification is None or ZspiderRegion is None or ZspiderDomain is None:
                rev_data = {'code':1, 'msg': "缺少关键信息", 'data':{}}
                return JsonResponse(rev_data)
            
            # 排除空格
            ZspiderName = "".join(ZspiderName.split())
            ZspiderClassification = "".join(ZspiderClassification.split())
            ZspiderRegion = "".join(ZspiderRegion.split())
            ZspiderDomain = "".join(ZspiderDomain.split())

            if len(ZspiderName) < 1 or len(ZspiderClassification) < 1 or len(ZspiderRegion) < 1 or len(ZspiderDomain) < 1:
                 rev_data = {'code':1, 'msg': "缺少关键信息", 'data':{}}
                 return JsonResponse(rev_data)
            # 查看是否重复

            temp = d2SpiderModle.objects(GspiderDomain=ZspiderDomain).first()
            

            if temp is not None and temp['GSpiderdeleted'] == 0:
                rev_data = {'code': 1, 'msg': "此网站已经存在", "data":{}}
                return JsonResponse(rev_data)

            if temp is not None and temp['GSpiderdeleted'] == 1:
                temp['GSpiderdeleted'] = 0

            
            newSpider = d2SpiderModle(
                GspiderId = d2SpiderModle.objects.count(),
                GspiderName = ZspiderName,
                GspiderClassification = ZspiderClassification,
                GspiderRegion = ZspiderRegion,
                GspiderDomain = ZspiderDomain 
            )
            try:
                if temp is not None:
                    temp.save()
                else:
                    newSpider.save()
            except Exception as err:
                print(err)
                return HttpResponseServerError()
            else:
                rev_data = {'code': 0, 'msg': "添加成功", 'data': "{}，添加成功".format(ZspiderName)}
                return JsonResponse(rev_data)
        else: 
            return HttpResponseBadRequest()

    except Exception as err:
        print(err)
        return HttpResponseServerError()