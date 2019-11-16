from django.utils.deprecation import MiddlewareMixin
from django.shortcuts  import HttpResponse
from django.http import HttpResponseBadRequest
import simplejson

class ZisJsonCheck(MiddlewareMixin):
    
    def process_request(self, request):
        if request.method != "POST":
            return HttpResponseBadRequest('请使用 "POST" 请求')

        try:
            get_data = simplejson.loads(request.body)
        except Exception as err:
            return HttpResponseBadRequest('请携带json格式数据')

    def process_response(self,request,response):
        return response