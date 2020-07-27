# UniTesTReport 

- #### unittest 生成测试报告

- #### unittest测试用例多线程执行
- #### 安装命令 pip install unittestreport

### 一、使用说明

​	本模块专门为unittest执行测试用例生成测试报告而开发，支持多线程执行unittest的测试用例

- ##### 关于测试报告

    - 本模块可以生成3个风格的测试报告
    （ps:一种自己编写的，另一种风格由的BeautifulReport的报告模板稍加修改而来）
    - 另外为了方便大家使用，本模块还集成了HTMLTestRunnerNew这个生成报告的模块
    - 报告截图
    - ![1594961041386](C:\课件\images\1594961041386.png)

- ##### 关于多线程执行

    - 因为考虑到测试用例执行的顺序问题，本模块提供了多线程执行用例的方法式
    - TestRunner.run：可以通过参数来设置启动执行线程的数量，和线程中最小的用例执行单元，
        thread_count:线程数量，默认位1
        exec_unit: case ro class
            case: 以测试用例为单位开启多线程运行，不能保证用例执行的顺序问题
            class:以用例类为单位开启多线程运行，可以保证用例类中的用例执行的顺序问题

- ##### 关于TestRunner类初始化，以及允许方法的参数说明

    ```python
    class TestRunner():
        """unittest运行程序"""

        def __init__(self, suite: unittest.TestSuite,
                     filename="report.html",
                     report_dir=".",
                     title='测试报告',
                     tester='木森',
                     desc="木森执行测试的报告",
                     templates=1
                     ):
            """
            初始化用例运行程序
            :param suites: 测试套件
            :param filename: 报告文件名
            :param report_dir:报告文件的路径
            :param title:测试套件标题
            :param tester:测试者
            :param desc:相关的描述信息
            :param temp:模板风格
            """
       def run(self, thread_count=1):

            """
            支持多线程执行
            注意点：如果多个测试类共用某一个全局变量，由于资源竞争可能回出现错误
            :param thread_count:线程数量，默认位1
            :param exec_unit: case ro class
                    case: 以测试用例为单位开启多线程运行，不能保证用例执行的顺序问题
                    class:以用例类为单位开启多线程运行，可以保证用例类中的用例执行的顺序问题
            :return:
            """
    ```

### 二、使用案例

```python
import unittest
from unittestreport import TestRunner

# 加载测试套件
suite1 = unittest.defaultTestLoader.discover(r"C:\project\musen\case_test")
# 创建运行对象
runner = TestRunner(suite1, 
                    title='木森的测试报告',
                    filename="musen02",
                    templates=1)

runner.run()
```

#### 备注：

- ##### 开发者：柠檬班—木森
- ##### 开发时间：2020-07-16
- ##### E-mail:musen_nmb@qq.com
- ##### 本模块目前是第一个版本，后续还会优化改进，欢迎各位大佬提BUG！




























