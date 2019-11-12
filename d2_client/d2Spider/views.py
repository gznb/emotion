# from django.shortcuts import render, HttpResponse
# import json
# from tools.authentication_module import authenticate
# from .models import websiteModel
# from tools.change_string import change_string

# def ZlookWebs(request):
#     if request.method == 'GET':
#         admin = authenticate(request)
#         if admin is None:
#             rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
#             return HttpResponse(json.dumps(rev_data, ensure_ascii=False))

#     get_data = json.loads(request.body)
#     currentPage = get_data['currentPage']       # 当前页
#     pageSize = get_data['pageSize']             # 页面大小
#     total = get_data['total']   

#     web_list = []
#     i = 1
#     total = websiteModel.objects.count()
#     for obj in websiteModel.objects.skip((currentPage-1)*pageSize).limit(pageSize):
#         web_list.append({
#             'number': i + (currentPage-1)*pageSize,
#             'source': obj['Gsource'],
#             'web_name': obj['GwebName'],
#             'web_classification': obj['GwebClassification'],
#             'web_region': obj['GwebRegion']
#         })
#         i += 1

#     rev_data = {
#         'code': 0,
#         'msg':'查询成功',
#         'data': {
#             'list': web_list,
#             'total': total
#         }
#     }
#     return HttpResponse(json.dumps(rev_data, ensure_ascii=False))

# def ZuploadAction(request):
#     if request.method == 'POST':
#         admin = authenticate(request)
#         if admin is None:
#             rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
#             return HttpResponse(json.dumps(rev_data, ensure_ascii=False))
        
#         file_obj = request.FILES.get('file', None)
#         get_text = file_obj.read()
#         web_list = get_text.decode('utf-8').split('\n')
#         sums = 0
#         for web in web_list:
#             web = web.split(' ')
#             if len(web) != 4:
#                 continue
#             print(web)
#             # print(change_string(web[0]), change_string(web[1]), change_string(web[2]), change_string(web[3]))
#             #  这里有点不太一样
#             if websiteModel.objects(Gsource = change_string(web[0])).first() is None:
#                 website = websiteModel(
#                     Gsource = change_string(web[0]),
#                     GwebName = change_string(web[1]),
#                     GwebClassification = change_string(web[2]),
#                     GwebRegion = change_string(web[3])
#                 )
#                 website.save()
#                 sums += 1
            

#         rev_data = {'code': 0, 'msg': "上传成功", 'data':"新加入 {} 个词".format(sums)}
        
#         return HttpResponse(json.dumps(rev_data, ensure_ascii=False))

# def ZaddOneWeb(request):
#     if request.method == 'POST':
#         admin = authenticate(request)
#         if admin is None:
#             rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
#             return HttpResponse(json.dumps(rev_data, ensure_ascii=False))
#         get_data = json.loads(request.body)
#         # print(get_data)
#         temp = websiteModel.objects(Gsource = get_data['source']).first()

#         if temp is not None:
#             rev_data = {'code': 1, 'msg': "此网址已经存在", 'data': {} }
#             return HttpResponse(json.dumps(rev_data, ensure_ascii=False))

        
#         website = websiteModel(
#             Gsource = get_data['source'],
#             GwebName = get_data['web_name'],
#             GwebClassification = get_data['web_classification'],
#             GwebRegion = get_data['web_region']
#         )
       
#         try:
#             website.save()
#             rev_data = {'code': 0, 'msg': "添加成功", 'data': get_data['source'] + " 添加成功"}
#             return HttpResponse(json.dumps(rev_data, ensure_ascii=False))
#         except:
#             rev_data = {'code': 1, 'msg': "数据库未知错误，请联系管理员", 'data': {}}
#             return HttpResponse(json.dumps(rev_data, ensure_ascii=False))

# def ZdeleteOneWebsite(request):
#     if request.method == 'POST':
#         admin = authenticate(request)
#         if admin is None:
#             rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
#             return HttpResponse(json.dumps(rev_data, ensure_ascii=False))
#         get_data = json.loads(request.body)
#         try:
#             well_be_deleted = websiteModel.objects(Gsource = get_data['source']).first()
#             well_be_deleted.delete()
#             rev_data = {'code': 0, 'msg': "删除成功", 'data': {}}
#             return HttpResponse(json.dumps(rev_data, ensure_ascii=False))
#         except Exception as err:
#             print(err)
#             rev_data = {'code': 1, 'msg': "删除失败，系统内部错误", 'data': {}}
#             return HttpResponse(json.dumps(rev_data, ensure_ascii=False))

# def ZupdateOne(request):
#     if request.method == 'POST':
#         admin = authenticate(request)
#         if admin is None:
#             rev_data = {'code': 1, 'msg': "token无效，请重新登陆", 'data': {}}
#             return HttpResponse(json.dumps(rev_data, ensure_ascii=False))

#         get_data = json.loads(request.body)
#         try:
#             websiteModel.objects(Gsource = get_data['source']).update_one(GwebName=get_data['web_name'], GwebClassification=get_data['web_classification'], GwebRegion=get_data['web_region'])
#             rev_data = {'code': 0, 'msg': "更新成功", 'data': {}}
#             return HttpResponse(json.dumps(rev_data, ensure_ascii=False))
#         except Exception as err:
#             print(err)
#             rev_data = {'code': 1, 'msg': "删除失败，系统内部错误", 'data': {}}
#             return HttpResponse(json.dumps(rev_data, ensure_ascii=False))
    