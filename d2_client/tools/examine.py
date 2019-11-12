#encoding:utf-8

import re

def examineTelephone(telephone):
        #号码前缀，如果运营商启用新的号段，只需要在此列表将新的号段加上即可。
        phoneprefix=['130','131','132','133','134','135','136','137','138','139','150','151','152','153','156','158','159','170','183','182','185','186','188','189']
        #检测号码是否长度是否合法。
        if len(telephone) != 11:
                return 0, "The length of phonenum is 11."
        else:
                #检测输入的号码是否全部是数字。
                if  telephone.isdigit():
                        #检测前缀是否是正确。
                        if telephone[:3] in phoneprefix:
                                return 1, "OK"
                        else:
                                return 0, "The phone num is invalid."
                else:
                        return 0, "The phone num is made up of digits."

    
def examineUsername(username):
    if username is None:
        return 0, "用户名不能为空"

    if len(username) > 20:
        return 0, "用户名长度不能大于20个字符"
    
    for i in username:
        if i == ' ':
            return 0, "用户名不能有空格"

    return 1, "OK"
 

def examineEmail(email): 
    if email is None:
        return 0, "邮箱不能为空"

    email_rule = r'^[0-9a-zA-Z\_\-]+(\.[0-9a-zA-Z\_\-]+)*@[0-9a-zA-Z]+(\.[0-9a-zA-Z]+){1,}$'
    if not re.match(email_rule, email):
        return 0, "邮箱不合法"

    return 1, "OK"


