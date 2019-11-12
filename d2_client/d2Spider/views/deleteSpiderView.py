from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import simplejson
from django_redis import get_redis_connection
from d2Spider.models import d2SpiderModle

def ZdeleteSpider(request):
    
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

            ZspiderId = get_data.get('number')
            deleteSpider = d2SpiderModle.objects(GspiderId=ZspiderId).first()
            deleteSpider['GSpiderdeleted'] = 1
            try:
                deleteSpider.save()
            except Exception as err:
                print(err)
                return HttpResponseServerError
            else:
                rev_data = {'code': 0, 'msg': "删除成功", 'data': {}}
                return JsonResponse(rev_data)
        else:
            return HttpResponseServerError()
    except Exception as err:
        return HttpResponseServerError()