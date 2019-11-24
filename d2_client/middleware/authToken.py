from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from d2_client.settings import NOT_AUTH_URL
from django_redis import get_redis_connection


class ZauthTokenMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        res_url = request.path
        if res_url not in NOT_AUTH_URL:
            token = request.META.get('HTTP_X_TOKEN')
        
            # 没有发送token 
            if token is None:
                return JsonResponse({'code': 1, 'msg': '身份信息失效', 'data': ""})
            else:
                # token  在 redis中不存在
                conn = get_redis_connection()
                if conn.get(token) is None:
                    return JsonResponse({'code': 1, 'msg': '身份信息失效', 'data': ""})

    def process_response(self, request, response):
        return response
