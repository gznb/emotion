from django.db import models
import mongoengine

class d2OrderModel(mongoengine.DynamicDocument):
    '''
    
    '''
    GorderId = mongoengine.IntField()                           # id
    GorderName = mongoengine.StringField()                      # 名字
    GorderKeywordList = mongoengine.ListField()                 # 关键词列表
    GorderRemainingTimes = mongoengine.IntField()               # 剩余次数
    GorderLastTime = mongoengine.DateTimeField()                # 上一次爬取时间
    GuserTelephone = mongoengine.StringField(max_length=13)     # 客户电话
    GorderSpiderList = mongoengine.StringField()                # 爬虫列表
    GorderCreateTime = mongoengine.DateTimeField()              # 创建时间
    GorderNegativeList = mongoengine.ListField(default=[])      # 负面词列表
    GorderDeleted = mongoengine.IntField(default=0)             # 伪删除

