from django.http import JsonResponse, HttpResponseServerError
from d2Spider.models import d2SpiderModel
from rest_framework.views import APIView
from check_data.check_field import CheckField
import logging
logger = logging.getLogger('django')


class LookSpiderView(APIView):
    def __init__(self):
        self.check_file = CheckField()
        super().__init__()

    def check_format(self, request):
        current_page = request.data.get('currentPage')  # 当前页
        page_size = request.data.get('pageSize')  # 页面大小
        total = request.data.get('total')
        try:
            current_page = self.check_file.is_int_str(current_page)
            page_size = self.check_file.is_int_str(page_size)
            total = self.check_file.is_int_str(total)
        except (ValueError, TypeError) as err:
            return JsonResponse({'code': 2, 'msg': str(err), 'data':{}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        else:
            return {
                'currentPage': current_page,
                'pageSize': page_size,
                'total': total
            }

    def post(self, request, *args, **kwargs):
        get_data = self.check_format(request)
        if isinstance(get_data, (JsonResponse, HttpResponseServerError)):
            return get_data
        else:
            current_page = get_data['currentPage']  # 当前页
            page_size = get_data['pageSize']  # 页面大小
            total = get_data['total']  # 一共多少条
            spider_list = []
            res = d2SpiderModel.objects(GspiderDeleted=0)
            total = res.count()
            for obj in res.skip((current_page - 1) * page_size).limit(page_size):
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
                'msg': '查询成功',
                'data': {
                    'list': spider_list,
                    'total': total
                }
            }
            return JsonResponse(rev_data)

# def ZlookSpider(request):
#     try:
#
#             # 验证
#         conn = get_redis_connection()
#         get_data = simplejson.loads(request.body)
#         Ztoken = request.META.get('HTTP_X_TOKEN')
#         if Ztoken is None:
#             rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
#             return JsonResponse(rev_data)
#         Ztelephone = conn.get(Ztoken)
#
#         if Ztelephone is not None:
#             Ztelephone = Ztelephone.decode('UTF-8')
#         else:
#             rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
#             return JsonResponse(rev_data)
#
#         currentPage = get_data['currentPage']       # 当前页
#         pageSize = get_data['pageSize']             # 页面大小
#         total = get_data['total']                   # 一共多少条
#
#         # 关键信息不存在
#         if currentPage is None or pageSize is None or total is None:
#             rev_data = {'code':1, 'msg': "关键信息不存在", 'data':{}}
#             return JsonResponse(rev_data)
#         spider_list = []
#         res = d2SpiderModel.objects(GspiderDeleted=0)
#         total = res.count()
#         for obj in res.skip((currentPage-1)*pageSize).limit(pageSize):
#             spider_list.append({
#                 'number': obj['GspiderId'],
#                 'source': obj['GspiderDomain'],
#                 'web_name': obj['GspiderName'],
#                 'web_classification': obj['GspiderClassification'],
#                 'web_region': obj['GspiderRegion']
#                 # 'forbidRemove': False,     ## 是否禁止删除
#                 # 'showRemoveButton': True   ## 是否显示删除按钮
#             })
#         rev_data = {
#             'code': 0,
#             'msg':'查询成功',
#             'data': {
#                 'list': spider_list,
#                 'total': total
#             }
#         }
#         conn.expire(Ztoken, OUT_TIME)
#         return JsonResponse(rev_data)
#
#     except Exception as err:
#         return HttpResponseServerError()
