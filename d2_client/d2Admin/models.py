from django.db import models
import mongoengine


class d2AdminModel(mongoengine.DynamicDocument):
    '''
    1. 为区分 和 系统默认的 关键字重复， 定义字段 统一 添加前缀 G
    2. 目前使用 动态文档，方便扩展
    '''
    GadminTelephone           =   mongoengine.StringField(max_length=13, unique=True)         # 电话号码，为主键
    GadminPassword            =   mongoengine.StringField(min_length=8, max_length=16)        # 密码为 8 ~ 16 位之间， 暂时无特殊要求
    GadminUsername            =   mongoengine.StringField(max_length=16)                      # 用户名

