# 

项目中的setting.py文件，是整个项目的配置文件，接下来相信介绍一下项目的配置选项。

### 1、debug模式运行

项目创建之后，默认运行是开启了debug模式，运行过程中会输出详细的debug级别日志。如果不像看运行日志，则将settings中的DEBUG设置为Flase即可。

```python
# 是否开启debug模式：True为debug模式，False为关闭debug模式
DEBUG = False
```



### 2、ENV全局的变量

将settings.py中的ENV可以设置项目全局配置，

**1、全局的域名**

推荐在`ENV`中设置全局的`host,`不建议在每一个测试用例中去设置`host`,切换测试环境切换也更方便(如果用例数据中没有自己定义`host`，会自动引用全局的host地址)

```python
ENV = {
    "host":"http://WWW.XXX.com/",
}
```

**2、全局的请求头**

如果项目接口有必传的请求头数据，也可以直接在`ENV`中设置(如果用例数据中没有定义时，也会自动引用全局的`headers`)。

```python
ENV = {
    "host":"http://WWW.XXX.com/",
    "headers": {"UserAgent": "apin-test01"}
}
```

**3、全局的测试数据**

如果用例中需要引用事先准备好的一些测试数据，如测试账号、密码之类的

如：定义一个测试账号、测试密码、用户id

```python
ENV = {
    "host":"http://WWW.XXX.com/",
    "headers": {"UserAgent": "apin-test01"},
    "user":"musen@qq.com",
    "pwd":"lemon123",
    "user_id":111
}
```

测试用例中直接使用`${{ name}}`即可引用，

```python
# 引用user和pwd
{
 'title': "登录",
 'interface': "member/register",
 "method": "post",
 'json': {"mobile_phone": "${{user}}", "pwd": "${{pwd}}"},
}
```

- **注意点：如果局部环境和全局变量重名，优先引用局部变量。**



### 3、测试报告

​	通过`setting.py`中的`TEST_RESULT`，可以配置测试报告的输出信息。

```python
TEST_RESULT = {
    # 测试报告文件名
    "filename": "report.html",
    # 测试人员
    "tester": "测试员",
    # 报告标题
    "title": "测试报告",
    # 报告样式 ：有1，2，三个样式
    "templates": 1,
    # 报告描述信息
    "desc": "XX项目测试生成的报告"
}
```



### 4、邮件推送测试结果

如果要将测试结果发送到指定的邮箱中，则在`settings.py`添加`EMAIL`配置即可

```python
EMAIL = {
    # smtp服务器地址
    "host": 'smtp.qq.com',
    # smtp服务器端口
    "port": 465,
    # 邮箱账号
    "user": "xxxx@qq.com",
    # smtps授权码
    "password": "xxxx",
    # 收件人列表
    "to_addrs": ['xxx@qq.com','xxx@qq.com'],
    # 是否发送附件
    "is_file": True
}
```



### 5、测试结果推送到钉钉群

如果要将测试结果推送到钉钉群，则在`settings.py`添加`DINGTALK`配置即可。

```python
DINGTALK = {
    #  钉钉机器人的Webhook地址
    "url": "",
    # 如果钉钉机器人安全设置了关键字，则需要传入对应的关键字
    "key": None,
    # 如果钉钉机器人安全设置了签名，则需要传入对应的密钥
    "secret": None,
    # 钉钉群中要@人的手机号列表，如：[137xxx,188xxx]
    "atMobiles": [],
    # 是否@所有人
    "isatall": False
}
```



### 6、测试结果推送企业微信群

如果要将测试结果推送到企业微信群，则在`settings.py`添加`WECHAT`配置即可。

```python
WECHAT = {
    # 企业微信群ID
    "chatid": "",
    # 调用企业微信API接口的凭证
    "access_token": ""
}
```

