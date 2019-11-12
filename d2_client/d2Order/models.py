from django.db import models
import mongoengine

class d2OrderModel(mongoengine.DynamicDocument):
    '''
    
    '''
    GorderId = mongoengine.IntField()                   # id
    GorderName = mongoengine.StringField()              # 名字
    GorderKeywordList = mongoengine.ListField()              # 关键词列表
    GorderRemainingTimes = mongoengine.IntField()            # 剩余次数
    GorderLastTime = mongoengine.DateTimeField()             # 上一次爬取时间
    GuserTelephone = mongoengine.StringField(max_length=13) # 客户电话
    GorderSpiderList = mongoengine.StringField()             # 爬虫列表
    GorderStartTime = mongoengine.DateTimeField()            # 开始时间

    GorderDeleted = mongoengine.IntField(default=0)          # 伪删除

