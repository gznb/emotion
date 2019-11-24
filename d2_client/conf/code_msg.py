
# code, msg
CODE_MSG_DICT = {
    # 电话号码
    '100': "合法手机号码",
    '101': "手机号码不能为空",
    '102': "手机号码应该是11位！",
    '103': "该手机号码不在三大运营商之内，如果确实存在，请联系我们！！！",
    '104': "手机号码应该为数字字符串",
    # 用户名
    '120': "合法用户名",
    '121': "用户名不能为空",
    '122': "用户名必须为字符串",
    '123': "用户名长度必须大于2位并且小于16位!!!",
    # 邮箱
    '140': "合法邮箱",
    '141': "邮箱不能为空",
    '142': "邮箱必须为字符串",
    "143": "非法邮箱",

    # 上传数据格式问题
    # 订单id
    '160': "订单ID",
    '161': "订单编号不能为空",
    '162': "订单编号必须为数字",
    '163': "订单编号必须>=0",

    # 时间周期
    '180': "合法时间周期",
    '181': "时间周期缺失",
    '182': "时间周期必须为数字",
    '183': "时间周期必须>=1",

    # 时间检查
    '200': "合法时间",
    '201': "时间不能为空",
    '202': "时间必须为字符串类型",
    '203': "时间必须为'%Y-%m-%d %H:%M:%S'格式例如'2011-11-11 11:11:11'",
    '204': "开始时间和结束时间差与给定时间周期不吻合",

    # 来源检测
    '220': "合法来源",
    '221': "{}中关键参数不能为空",
    '222': "{}中参数类型错误",
    '223': "关键参数缺失",
    '224': "关键参数类型错误"
}
