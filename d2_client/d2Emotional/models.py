from django.db import models
import mongoengine

class d2EmotionalModel(mongoengine.DynamicDocument):
    '''

    '''
    
    GemotionalId = mongoengine.IntField(unique=True)                   # id
    GemotionalName = mongoengine.StringField()              # 敏感词名字
    GemotionalClassification = mongoengine.StringField()  # 分类列表
    GemotionalScore = mongoengine.FloatField(default=0.0)              # 分数
    GemotionalAttribute = mongoengine.StringField()                 # 属性
    GemotionalOwnList = mongoengine.ListField(default=[0])          # 所属列表
    
    GemotionalDeleted = mongoengine.IntField(default=0)              # 伪删除
