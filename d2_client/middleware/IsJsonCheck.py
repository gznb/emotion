from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseBadRequest
from simplejson import loads
from simplejson.errors import JSONDecodeError


class ZisJsonCheckMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        if request.method != "POST":
            return HttpResponseBadRequest('请使用 "POST" 请求')

        filename = request.FILES.get('filename')
        if filename is None:
            try:
                loads(request.body)
            except TypeError as err:
                return HttpResponseBadRequest('请携带json格式数据')
            except JSONDecodeError as err:
                return HttpResponseBadRequest('json 编码格式错误')

    def process_response(self,request,response):
        return response
