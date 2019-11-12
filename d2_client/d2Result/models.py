from django.db import models
import mongoengine 
# Create your models here.

class d2ResultModel(mongoengine.DynamicDocument):
    '''
    '''
    GresultKeyword = mongoengine.StringField()                        # 搜索关键词
    GresultRealUrl = mongoengine.URLField()                           # 网页url
    GresultTitle = mongoengine.StringField()                          # 网页title
    GresultDetailedInformating = mongoengine.StringField()            # 文本信息   
    
    GresultNowTime = mongoengine.DateTimeField()                      # 爬取时间
    GresultAttribute = mongoengine.StringField()                      # 网页属性   
    GresultReleaseTime = mongoengine.DateTimeField()                  # 网页发布时间   
    GresultScore  = mongoengine.FloatField()                          # 评分
    
    GorderId = mongoengine.StringField()                              # 订单id
    GspiderId = mongoengine.IntField()                                # 爬虫id

    GresultDeleted = mongoengine.IntField(default=0)                  # 伪删除