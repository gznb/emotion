from django.db import models
import mongoengine
# Create your models here.

class d2SpiderModle(mongoengine.DynamicDocument):
    '''
    爬虫类
    '''
    GspiderId = mongoengine.IntField(unique=True)                  # id
    GspiderName = mongoengine.StringField()             # 名称
    GspiderRegion = mongoengine.StringField()           # 地区
    GspiderClassification = mongoengine.StringField()   # 分类
    GspiderDomain = mongoengine.StringField(unique=True)           # 域名
    
    GSpiderdeleted = mongoengine.IntField(default=0)          # 伪删除