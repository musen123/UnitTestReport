# 

unittestreport内部实现了推送测试结果到邮箱的方法，执行完测试用例之后调用发送测试报告的方法即可。发邮件的方法介绍：TestRunner类中实现了send_email方法，可以方便用户，快速发送邮件。

#### 1、使用案例

```python
suite = unittest.defaultTestLoader.discover(r'C:\project\open_class\Py0507\testcase')
runner = TestRunner(suite)
runner.run()
runner.send_email(host="smtp.qq.com",
                  port=465,
                  user="musen_nmb@qq.com",
                  password="alg123412bab",
                  to_addrs="324666668@qq.com")
```

#### 2、参数介绍

- **host： smtp服务器地址**

- **port：端口**

- **user：邮箱账号**

- **password：smtp服务授权码**

- **to_addrs：收件人邮箱地址（一个收件人传字符串，多个收件人传列表）**

    

> **注意：目前发送邮件只支持465和25端口**



#### 3、收到的邮件样式

![image](C:\课件\images\1598866521882-8470de3c-1620456241096.png )

