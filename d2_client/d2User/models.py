
import mongoengine
from django.db import models


class d2UserModel(mongoengine.DynamicDocument):
    '''
    1. 为了避免 字段名 和 系统有关 变量名冲突，前面添加前缀 'G'
    2. 方便扩充，暂时为 动态文档
    '''
    # 用户基本信息
    GuserTelephone = mongoengine.StringField(required=True, max_length=46, unique = True)      # 电话 唯一标识
    GuserPassword = mongoengine.StringField(min_length=8, max_length=16)        # 密码
    GuserUsername = mongoengine.StringField(min_length=2, max_length=16)                      # 姓名
    GuserCompany = mongoengine.StringField(max_length=64)                       # 公司
    GuserEmail = mongoengine.EmailField()                                       # 邮箱
    GuserRegion = mongoengine.StringField(max_length=128)                       # 地区
    GuserPosition = mongoengine.StringField(max_length=64)                      # 级别
    # 购买时长
    '''
    1.  当前时间 < 购买日期 + 可用时长                                          ## 账号正常使用
    2.  购买日期 + 可用时长 < 当前时间 < 购买日期 + 可用时长 + 延长时长           ## 账号处于延长期内
    3.  购买日期 + 可用时长 + 延长时长 < 当前时间                                ## 账号停用，相应爬虫全部暂停 
    4.  时间计算为 秒 级，因此不考虑 时间相等的情况
    '''
    GuserRegistrationDate = mongoengine.DateTimeField()        # 注册日期  年/月/日/时/分/秒
    GuserPurchaseDate = mongoengine.DateTimeField()                             # 购买日期  年/月/日/时/分/秒
    GuserAvailableTime = mongoengine.IntField()                                 # 可用时长  单位：天
    GuserExtendedDate = mongoengine.IntField(default=0)                         # 延长时长  单位:  天

    # 用户活跃度
    GuserUseCounts = mongoengine.IntField(default=0)                            # 使用次数
    GuserLastLogin = mongoengine.DateTimeField()                   # 上次登陆时间  年/月/日/时/分/秒
    GuserMoneyCounts = mongoengine.IntField(default=0)                          # 消费总额
    GuserArticleContent = mongoengine.IntField(default=0)                       # 总数据条数


    Gdeleted = mongoengine.IntField(default=0)                              # 伪删除

    