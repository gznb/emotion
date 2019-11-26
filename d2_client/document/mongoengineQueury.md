
1. d2ResultModel.objects(__raw__={'GorderId': 1})
    使用原生的 pymongo 查询，但是不支持，筛选
2. objects.all()   
返回所有的查询结果集。也就是可以遍历所有

3. all_fields()  
返回的是所有字段的集合，仅仅只有字段

4.  as_pymongo()
    直接返回 文档实例，List
5. .exclude('GorderId')  
    排除掉一些字段
6. hint
    明确告诉 使用什么索引
    
    
 7. 使用标题或者正文搜索有点小难度，应该是在里面写 正则表达式