"""
============================
Author:柠檬班-木森
Time:2020/7/7   14:47
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================

本模块主要是为了解决多线程运行unittest测试用例的问题
该模块预留了两个入口，

注意点：
使用起来非常简单，只需要调用TestRunner的run方法即可执行测试用例，运行的时候可通过参数指定开启的线程数量

"""
import os
import unittest
import time
from concurrent.futures.thread import ThreadPoolExecutor

from unittestreport.core.sendEmail import SendEmail
from unittestreport.core.testResult import TestResult, ReRunResult
from jinja2 import Environment, FileSystemLoader


class TestRunner():
    """unittest运行程序"""

    def __init__(self, suite: unittest.TestSuite,
                 filename="report.html",
                 report_dir=".",
                 title='测试报告',
                 tester='木森',
                 desc="XX项目测试生产的报告",
                 templates=1
                 ):
        """
        初始化用例运行程序
        :param suites: 测试套件
        :param filename: 报告文件名
        :param report_dir:报告文件的路径
        :param title:测试套件标题
        :param templates: 可以通过参数值1或者2，指定报告的样式模板，目前只有两个模板
        :param tester:测试者
        """
        if not isinstance(suite, unittest.TestSuite):
            raise TypeError("suites 不是测试套件")
        if not isinstance(filename, str):
            raise TypeError("filename is not str")
        if not filename.endswith(".html"):
            filename = filename + ".html"
        self.suite = suite
        self.filename = filename
        self.title = title
        self.tester = tester
        self.desc = desc
        self.templates = templates
        self.report_dir = report_dir
        self.result = []
        self.starttime = time.time()

    def classification_suite(self):
        """
        将测试套件中的用例，根据用例类位单位，拆分成多个测试套件，打包成列表类型
        :return: list-->[suite,suite,suite.....]
        """
        suites_list = []

        def wrapper(suite):
            for item in suite:
                if isinstance(item, unittest.TestCase):
                    suites_list.append(suite)
                    break
                else:
                    wrapper(item)

        wrapper(self.suite)
        return suites_list

    def classification_test_case(self):
        """
        将测试套件中的用例进行拆分，保存到列表中
        :return: list-->[case,case]
        """
        test_list = []

        def wrapper(suite):
            for item in suite:
                if isinstance(item, unittest.TestCase):
                    test_list.append(item)
                else:
                    wrapper(item)

        wrapper(self.suite)
        return test_list

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
        if exec_unit == "case":
            # 将测试套件按照用例进行拆分
            suites = self.classification_test_case()
        else:
            # 将测试套件按照用例类进行拆分
            suites = self.classification_suite()
        with ThreadPoolExecutor(max_workers=thread_count) as ts:
            for i in suites:
                res = TestResult()
                self.result.append(res)
                ts.submit(i.run, result=res).add_done_callback(res.stopTestRun)
            ts.shutdown(wait=True)

        self.get_reports()

    def rerun_run(self, count=0, interval=2):
        """
        测试用例失败、错误重跑机制
        :param count: 重跑次数，默认为0
        :param interval: 重跑时间间隔，默认为2
        :return:
        """
        res = ReRunResult(count=count, interval=interval)
        self.result.append(res)
        suites = self.classification_test_case()
        for case in suites:
            case.run(res)
        res.stopTestRun()
        self.get_reports()

    def get_reports(self):
        """生成报告"""
        print("所有用例执行完毕，正在生成测试报告中......")
        # 汇总测试结果
        test_result = {
            "success": 0,
            "all": 0,
            "fail": 0,
            "skip": 0,
            "error": 0,
            "results": [],
            "testClass": [],
        }
        # 整合测试结果
        for res in self.result:
            for item in test_result:
                test_result[item] += res.fields[item]

        test_result['runtime'] = '{:.2f} S'.format(time.time() - self.starttime)
        test_result["begin_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.starttime))
        test_result["title"] = self.title
        test_result["tester"] = self.tester
        test_result['desc'] = self.desc
        if test_result['all'] != 0:
            test_result['pass_rate'] = '{:.2f}'.format(test_result['success'] / test_result['all'] * 100)
        else:
            test_result['pass_rate'] = 0

        # 获取报告模板
        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        env = Environment(loader=FileSystemLoader(template_path))
        if self.templates == 2:
            template = env.get_template('templates02.html')
        elif self.templates == 3:
            template = env.get_template('templates03.html')
        else:
            template = env.get_template('templates.html')
        file_path = os.path.join(self.report_dir, self.filename)
        # 渲染报告模板
        res = template.render(test_result)
        # 输出报告到文件
        with open(file_path, 'wb') as f:
            f.write(res.encode('utf8'))
        print("测试报告已经生成，报告路径为:{}".format(file_path))
        self.email_conent = {"file": os.path.abspath(file_path),
                             "content": env.get_template('templates03.html').render(test_result)
                             }

    def send_email(self, host, port, user, password, to_addrs, is_file=True):
        """
        发生报告为附件到邮箱
        :param host: str类型，(smtp服务器地址)
        :param port: int类型，(smtp服务器地址端口)
        :param user: str类型，(邮箱账号)
        :param password: str类型（邮箱密码）
        :param to_addrs: str(单个收件人) or list(多个收件人)收件人列表，
        :return:
        """
        sm = SendEmail(host=host, port=port, user=user, password=password)
        if is_file:
            filename = self.email_conent["file"]
        else:
            filename = None
        content = self.email_conent["content"]

        sm.send_email(subject=self.title, content=content, filename=filename, to_addrs=to_addrs)
