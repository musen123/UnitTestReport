# 

关于把测试结果推送到钉钉群，unittestreport里面进行了封装。执行完用例之后，调用TestRunner对象的dingtalk_notice方法即可。

#### 1、参数介绍

关于dingtalk_notice这个方法的参数如下，大家可以根据使用需求来进行选择。

- **url: 钉钉机器人的Webhook地址**

- **key: （非必传：str类型）如果钉钉机器人安全设置了关键字，则需要传入对应的关键字**

- **secret:（非必传:str类型）如果钉钉机器人安全设置了签名，则需要传入对应的密钥**

- **atMobiles: （非必传，list类型）发送通知钉钉中要@人的手机号列表，如：[137xxx,188xxx]**

- **isatall: 是否@所有人，默认为False,设为True则会@所有人**

- **except_info:是否发送未通过用例的详细信息，默认为False，设为True则会发送失败用例的详细信息**

#### 2、案例代码：

```python
import unittest
from unittestreport import TestRunner

# 收集用例到套件
suite = unittest.defaultTestLoader.discover(CASE_DIR)
runner = TestRunner(suite)
# 执行用例
runner.run()

url = "https://oapi.dingtalk.com/robot/send?access_token=6e2a63c2b9d870ee878335b5ce6d5d10bb1218b8e64a4e2b55f96a6d116aaf50"
# 发送钉钉通知  
runner.dingtalk_notice(url=url, key='钉钉安全设置的关键字',secret='钉钉安全设置签名的秘钥')

# 备注：关于钉钉群机器人的创建大家可以去看钉钉开放平台上的教程，关键字和秘钥，根据创建钉钉机器人时设置的去添加，没有设置就不需要传这个参数。
```

### 