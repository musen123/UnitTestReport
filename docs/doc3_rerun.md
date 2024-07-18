# 
### 失败重运行
​	关于unittest重运行机制，unittestreport最新得版本中做了优化，直接使用TestRunner.run（之前的版本是TestRunner.rerun_run方法），传入相关的参数即可实现重运行，具体的使用如下

**案例**

运行时加上参数，即可实现用例失败重运行

```python
import unittestreport
# 1、加载测试用例到套件中
suite = unittest.defaultTestLoader.discover(r'C:\project\open_class\Py0507\testcase')
runner = TestRunner(suite=suite)
runner.run(count=3, interval=2)
```

**参数说明：**

- count：用来指定用例失败重运行的次数
- interval：指定每次重运行的时间间隔

### **自定义用例执行顺序**
此方式可以实现自定义用例执行顺序，可以根据需求自己编排要执行的用例，也可以对某一条/或多条用例进行重复执行，具体使用如下：
###### 参数说明：
- run_case：用来指定要执行的用例，格式为：{自定义用例名称：用例方法}
- cls：测试类
- 注意点：unittest是按照ascii码顺序来执行的，所以自定义用例名称要注意ascii码顺序，否则会出现执行顺序混乱的情况


```python
from unittestreport import TestRunner
# 编写执行的测试用例顺序
run_cases = [
    {
        "cls": TestDemo,
        "run_case": {
            'test_rerun_1_login_out': TestDemo.test_login_out,
            'test_rerun_2_phone_login': TestDemo.test_phone_login,
            'test_rerun_3_login_out': TestDemo.test_login_out,
            'test_rerun_4_test_email_login': TestDemo.test_email_login
        }
    }, {
        "cls": TestDemo2,
        "run_case": {
            'test_demo2_01_email_login': TestDemo2.test_demo2_email_login,
            'test_demo2_02_login_out': TestDemo2.test_demo2_login_out,
            'test_demo2_03_email_login': TestDemo2.test_demo2_email_login,
            'test_demo2_04_login_out': TestDemo2.test_demo2_login_out,
            'test_demo2_05_email_login': TestDemo2.test_demo2_email_login,
        }
    }
]
# 执行用例
suite = TestRunner.customize_run_case(run_cases)
runner = TestRunner(suite, title="测试报告", report_dir="./report", templates=2)
runner.run()
```


