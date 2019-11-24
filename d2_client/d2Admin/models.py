from django.db import models
import mongoengine


class d2AdminModel(mongoengine.DynamicDocument):
    """

    """
    GadminTelephone = mongoengine.StringField(max_length=13, unique=True)         # 电话号码，为主键
    GadminPassword = mongoengine.StringField(min_length=8, max_length=16)        # 密码为 8 ~ 16 位之间， 暂时无特殊要求
    GadminUsername = mongoengine.StringField(max_length=16)                      # 用户名

