# django-resr-framework-mongoengine

## 登陆token 验证

1. 登陆成功后，将token信息存放在 redis中。 token--telephone
2. 验证成功后，得到一个 (telephone,token) 并刷新token失效时间
3. 验证失败返回一个抛出验证失败异常
4. 验证类 存放在 d2_client.rest_framework中
5. 登陆，注册，修改页面无需验证token
6. 然后一个身份信息失效的错误code的时候，不能将整型转变为 int


### token 生成
1. 类地址
    > d2_client.rest_framework.token.TokenHander
    
