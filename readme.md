# UniTesTReportV1.0.9

#### 备注：

- ##### 开发者：柠檬班—木森

- ##### E-mail:musen_nmb@qq.com

- ##### 大家在使用过程中发现bug,可以联系我，以便优化解决！

- ##### 安装命令 

    ```
    pip install unittestreport
    ```

## 一、本模在unittest上扩展的几个功能的问题

- ##### 功能一： unittest 生成多种风格的测试html报告

- ##### 功能二： unittest 用例多线程执行机制

- ##### 功能三： unittest 用例失败重运行机制（1.0.9版本新增）

- ##### 后续会持续，更新请关注项目github： https://github.com/musen123/UnitTestReport 

## 二、unittest生成测试HTML报告

- ##### 关于测试报告

    - 本模块可以生成3个风格的测试报告
    （ps:一种自己编写的，另一种风格由的BeautifulReport的报告模板稍加修改而来）
    - 另外为了方便大家使用，本模块还集成了HTMLTestRunnerNew这个生成报告的模块
    - 模块自带报告截图
    - ![1594961041386](http://testingpai.com/upload/file/2020/ef9be15f-79fc-4a5d-8861-9ea7f62989c8.png)

    

- ##### 关于TestRunner类初始化，以及允许方法的参数说明

    ```python
    class TestRunner():
        """unittest运行程序"""

        def __init__(self, suite: unittest.TestSuite,
                     filename="report.html",
                     report_dir=".",
                     title='测试报告',
                     tester='木森',
                     desc="木森执行测试生产的报告",
                     templates=1
                     ):
            """
            初始化用例运行程序
            :param suites: 测试套件
            :param filename: 报告文件名
            :param report_dir:报告文件的路径
            :param title:测试套件标题
            :param templates: 可以通过参数值1或者2，指定报告的样式模板，目前只有两个模板
            :param tester:
            """
    ```

- #### 使用案例

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
    # 运行测试
    runner.run()
    ```

    



## 三、关于多线程执行

- 因为考虑到测试用例执行的顺序问题，本模块提供了多线程执行用例的方法式
- TestRunner.run：可以通过参数来设置启动执行线程的数量，和线程中最小的用例执行单元，
    thread_count:线程数量，默认位1
    exec_unit: case ro class
        case: 以测试用例为单位开启多线程运行，不能保证用例执行的顺序问题
        class:以用例类为单位开启多线程运行，可以保证用例类中的用例执行的顺序问题

```python
    def run(self, thread_count=1, exec_unit="class"):
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



## 四、unittest用例重运行

​		关于unittest重运行机制，unittestreport中提供了两种方式，第一种局部生效的，可以自己去标记失败需要重运行的测试用例，第二种是全局的，所有的测试用例，只要运行失败都会重运行。那么接下来一个一个给大家介绍。

#### 1、单个用例重运行

- 如果像标记单个测试用例失败重运行，库用直接使用unittestreport中的rerun来标记测试用例，rerun接收两个参数count,和interval。
    - count：用来指定用例失败重运行的次数
    - interval：指定每次重运行的时间间隔

- 下面有三个测试用例，其中有一个test_case_01使用了rerun进行了标记，设置的失败重运行次数为4次，每次间隔的时间2秒。

```python
import unittest
from unittestreport import rerun

class TestClass(unittest.TestCase):
    @rerun(count=4, interval=2)
    def test_case_01(self):
        a = 100
        b = 99
        assert a == b
        
    def test_case_02(self):
        a = 100
        b = 101
        assert a == b
        
```

- 运行上述用例

    ```python
    import unittest
    from unittestreport import TestRunner
    from testcase import TestClass  # 导入上面写的测试用例类
    # 加载测试套件
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestClass)
    # 执行测试用例
    runner = TestRunner(suite=suite)
    runner.run()
    ```


#### 2、全部用例失败重跑机制

- 关于所有的测试用例失败重跑，unittestreport中提供了一个更为简单的使用入口，直接使用unittestreport中TestRunner对象的rerun_run方法即可实现所有的用例失败重运行，rerun_run同样有两个参数，count和interval。

    - count：用来指定用例失败重运行的次数
    - interval：指定每次重运行的时间间隔

- 测试用例如下：

    ```python
    import unittest
    from unittestreport import rerun
    
    class TestClass(unittest.TestCase):
        def test_case_01(self):
            a = 100
            b = 99
            assert a == b 
       def test_case_02(self):
            a = 100
            b = 101
            assert a == b
    ```

- 使用unittestreport的重运行机制，运行上述用例

    ```python
    import unittest
    from unittestreport import TestRunner
    from testcase import TestClass  # 导入测试用例类
    
    # 测试套件
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestClass)
    # 创建执行对象
    runner = TestRunner(suite=suite)
    # 执行测试用例，失败重运行设置为3次，间隔时间为2秒
    runner.rerun_run(count=3, interval=2)
    ```

- 执行测试可以看到失败的用例，都重复运行了三次：
