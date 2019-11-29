from django.http import JsonResponse
import pandas as pd
from d2Emotional.models import d2EmotionalModel
from rest_framework.views import APIView
import logging
logger = logging.getLogger('django')

class UploadView(APIView):

    def post(self, request, *args, **kwargs):

        file_obj = request._request.FILES.get('filename')
        if file_obj is None:
            rev_data = {'code': 1, 'msg': "请选择文件", 'data': {}}
            return JsonResponse(rev_data)

        if file_obj.name.split('.')[1] != 'xlsx':
            rev_data = {'code': 1, 'msg': "请上传xlsx文件", 'data': {}}
            return JsonResponse(rev_data)
        print(111)
        df = pd.read_excel(file_obj)
        print(222)
        columns_name = df.columns.values
        print(333)
        if columns_name[0] != 'keyword' and columns_name[1] != 'classification' and columns_name[2] != 'attribute':
            rev_data = {'code': 1, 'msg': '表头数据不对', 'data': {}}
            return JsonResponse(rev_data)
        df.columns = ['GemotionalName', 'GemotionalClassification', 'GemotionalAttribute']

        # 去除含有空行的列
        df.dropna(axis=0, how='any', inplace=True)
        counts = d2EmotionalModel.objects().count()
        for i in df.index.values:  # 获取行号的索引，并对其进行遍历：
            row_data = df.iloc[i].to_dict()  # 根据i来获取每一行指定的数据 并利用to_dict转成字典

            for k, v in row_data.items():
                row_data[k] = v.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
            try:
                row_data['GemotionalId'] = int(counts)
                if d2EmotionalModel.objects(GemotionalName=row_data['GemotionalName'],
                                            GemotionalClassification=row_data[
                                                'GemotionalClassification']).first() is None:
                    d2EmotionalModel(GemotionalId=counts,
                                     GemotionalName=row_data['GemotionalName'],
                                     GemotionalClassification=row_data['GemotionalClassification'],
                                     GemotionalAttribute=row_data['GemotionalAttribute']
                                     ).save()
                    counts += 1
            except Exception as err:
                logger.error(err)
                rev_data = {'code': 2, 'msg': "保存失败", 'data': ""}
                return JsonResponse(rev_data)

        rev_data = {'code': 0, 'msg': "上传成功", 'data': "上传成功"}
        return JsonResponse(rev_data)

# def upload_action(request):
#     token = request.META.get('HTTP_X_TOKEN')
#     if token is None:
#         rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
#         return JsonResponse(rev_data)
#
#
#     file_obj = request.FILES.get('filename')
#
#     if file_obj is None:
#         rev_data = {'code': 1, 'msg': "请选择文件", 'data': {}}
#         return JsonResponse(rev_data)
#
#     if file_obj.name.split('.')[1] != 'xlsx':
#         rev_data = {'code':1, 'msg': "请上传xlsx文件", 'data': {}}
#         return JsonResponse(rev_data)
#
#     df = pd.read_excel(file_obj)
#     columns_name = df.columns.values
#     if columns_name[0] != 'keyword' and columns_name[1] != 'classification' and columns_name[2] != 'attribute':
#         rev_data = {'code': 1, 'msg': '表头数据不对', 'data': {}}
#         return JsonResponse(rev_data)
#     df.columns = ['GemotionalName','GemotionalClassification','GemotionalAttribute']
#
#     # 去除含有空行的列
#     df.dropna(axis=0, how='any', inplace=True)
#     counts = d2EmotionalModel.objects().count()
#     for i in df.index.values:  # 获取行号的索引，并对其进行遍历：
#         row_data = df.iloc[i].to_dict()  # 根据i来获取每一行指定的数据 并利用to_dict转成字典
#
#         for k,v in row_data.items():
#             row_data[k] = v.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
#         try:
#             row_data['GemotionalId'] = int(counts)
#             if d2EmotionalModel.objects(GemotionalName=row_data['GemotionalName'],
#                                         GemotionalClassification=row_data['GemotionalClassification']).first() is None:
#                 d2EmotionalModel(GemotionalId=counts,
#                                  GemotionalName=row_data['GemotionalName'],
#                                  GemotionalClassification=row_data['GemotionalClassification'],
#                                  GemotionalAttribute=row_data['GemotionalAttribute']
#                 ).save()
#                 counts += 1
#         except Exception as err:
#             logger.error(err)
#             rev_data = {'code': 2, 'msg': "保存失败", 'data':""}
#             return JsonResponse(rev_data)
#
#     rev_data = {'code': 0, 'msg': "上传成功", 'data':""}
#     return JsonResponse(rev_data)