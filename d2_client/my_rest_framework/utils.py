from rest_framework.response import Response
# 导入源码中的exception_handler函数,因为重名,所以定义别名
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from rest_framework import exceptions
# 名字和源码中的一样(exception_handler)


def exception_handler(exc, context):
    # 根据源码，可以在这里单独的列出 用户信息失效错误
    if isinstance(exc, exceptions.APIException):
        return Response(data={'code': 1000, 'msg': '用户信息失效', 'data': {}}, status=status.HTTP_200_OK)
    # 通过源码我们知道drf_exception_handler处理服务端报错的时候返回值是空
    response = drf_exception_handler(exc, context)
    if response is None:
        # 如果这个为空, 就说明是服务器的500错误
        # 这个错误是drf不做处理的
        # 我们把错误信息保存到日志文件中
        # data： 传递的数据
        # status：响应状态码
        response = Response(data={'status': 1, 'msg': '上传数据格式可能错误哦', 'exc': f'{exc}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
    # 上线后注释或删除掉'error', 'exc': f'{exc}'
    response = Response(data={'code': 500, '服务器错误': 'error', 'exc': f'{exc}'})
    return response
