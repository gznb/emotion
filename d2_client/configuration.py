
# 配置文件专场

MSGLIST = {
    0 : "成功",
    1 : "", 
}

# redis 配置区
REDISSERVER = '127.0.0.1'
REDISPORT = 6379
REDISNAME = ''
REDISPASSWORD = ''


# mongo配置区
MONGOSERVER = '127.0.0.1'
MONGOPORT = 27017
MONGONAME = ''
MONGOPASSWORD = ''

# 短信配置区
SECRETID = ''
SECRETKEY = ''

# 用户登陆
USERLOGINMSG = [
    {
        'code': 0,
        'msg': "登陆成功",
        'data': {}
    },
    {
        'code': 1,
        'msg': "账号或密码错误",
        'data': {}
    },
    {
        'code': 2,
        'msg': "请修改初始密码，不修改将无法使用",
        'data': {}
    },
    {
        'code': 3,
        'msg': "含有异常字段",
        'data': {}
    },
]

# 用户注册
USERREGISTER = [
    {
        'code': 0,
        'msg': "注册成功，密码默认为电话号码，请及时修改，否则将无法使用",
        'data':{}
    },
    {
        'code': 1,
        'msg': "带*号是关键信息一定要填",
        'data':{}
    },
    {
        'code': 2,
        'msg': "该手机号码以及注册过了，请登陆，或者使用新号码注册",
        'data':{}
    },
    {
        'code': 3,
        'msg': "数据库异常，请联系管理员",
        'data':{}
    },
    {
        'code': 4,
        'msg': "",
        'data': {}
    },
]

# 初始化时长
TRIALDURATION = 30

# 初始化级别
INITIALLEVEL = '普通用户'

# 初始化延长时间
EXTENSIONOFTIME = 0

USERMODIFY = [
    {
        'code': 0,
        'msg': "修改成功",
        'data': {}
    },
    {
        'code': 1,
        'msg': "请重新登录",
        'data': {}
    },
    {
        'code': 2,
        'msg': "请输入旧密码",
        'data': {}
    },
    {
        'code': 3,
        'msg': "密码不能和账号一样",
        'data': {}
    },
    {
        'code': 4,
        'msg': "输入信息不合法，请确认，不想修改信息可以不填写",
        'data': {}
    },
    {
        'code': 5,
        'msg': "原密码输入错误",
        'data': {}
    }
]


# token
OUT_TIME = 600

# admin
ADMINLOGIN = [
    {
        'code': 0,
        'msg': "登陆成功",
        'data': {}
    },
    {
        'code': 1,
        'msg': "账号或密码不正确",
        "data": {}
    },
]