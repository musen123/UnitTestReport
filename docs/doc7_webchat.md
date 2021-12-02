# 

​	目前也有不少的公司使用企业微信办公，自动化跑完之后，测试结果需要推送到企业微信群，所以把这个功能做了一下集成（其实大家自己去写也没多少代码)。执行完用例之后，调用TestRunner对象的weixin_notice方法即可将测试结果推送到企业微信群。

#### 1、参数介绍

- **chatid： 企业微信群id**
- **access_token：调用企业微信API接口的凭证**
- **corpid：企业ID**
- **corpsecret：应用的凭证密钥**



#### 2、案例代码

```python
import unittest
from tests.test_case import TestClass
from unittestreport import TestRunner
# 加载用例
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestClass)
runner = TestRunner(suite=suite)
# 运行用例
runner.run()

# 推送测试结果到企业微信
# 方式一：
runner.weixin_notice(chatid="企业微信群id", access_token="调用企业微信API接口的凭证")
# 方式二：
runner.weixin_notice(chatid="企业微信群id",corpid='企业ID', corpsecret='应用的凭证密钥')
```

