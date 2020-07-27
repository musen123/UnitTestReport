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
import copy
import os
import re
import traceback
import unittest
import sys
import time
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import Manager
from io import StringIO

from jinja2 import Environment, FileSystemLoader

origin_stdout = sys.stdout


def output2console(s):
    """将stdout内容输出到console"""
    tmp_stdout = sys.stdout
    sys.stdout = origin_stdout
    print(s, end='')
    sys.stdout = tmp_stdout


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)
        output2console(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


class _TestResult(unittest.TestResult):
    """ 测试报告"""

    def __init__(self):
        super().__init__()

        self.fields = {
            "success": 0,
            "all": 0,
            "fail": 0,
            "skip": 0,
            "error": 0,
            "begin_time": "",
            "results": [],
            "testClass": set()
        }
        self.sys_stdout = None
        self.sys_stderr = None
        self.outputBuffer = None

    def startTest(self, test):
        """
        当测试用例测试即将运行时调用
        :return:
        """
        super().startTest(test)
        self.start_time = time.time()
        self.outputBuffer = StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.sys_stdout = sys.stdout
        self.sys_stderr = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        if self.sys_stdout:
            sys.stdout = self.sys_stdout
            sys.stderr = self.sys_stderr
            self.sys_stdout = None
            self.sys_stderr = None
        return self.outputBuffer.getvalue()

    def stopTest(self, test):
        """
        当测试用力执行完成后进行调用
        :return:
        """

        # 获取用例的执行时间
        test.run_time = '{:.3}s'.format((time.time() - self.start_time))

        # 获取该用例的类名
        test.class_name = test.__class__.__qualname__
        # 获取用例的方法名
        test.method_name = test.__dict__['_testMethodName']
        # 获取用例的描述
        test.method_doc = test.shortDescription()
        # 保存该用例执行的结果
        self.fields['results'].append(test)
        self.fields["testClass"].add(test.class_name)

        self.complete_output()

    def stopTestRun(self, title=None):
        """
        测试用例执行完手动调用统计测试结果的相关数据
        :param title:
        :return:
        """
        # 获取失败的用例数量
        self.fields['fail'] = len(self.failures)
        # 获取错误的用例数量
        self.fields['error'] = len(self.errors)
        # 获取标记跳过用例
        self.fields['skip'] = len(self.skipped)
        # 获取用例总数
        self.fields['all'] = sum(
            [self.fields['fail'], self.fields['error'], self.fields['skip'], self.fields['success']])
        self.fields['testClass'] = list(self.fields['testClass'])

    def addSuccess(self, test):
        """用例执行通过，成功数量+1"""
        self.fields["success"] += 1
        test.state = '成功'
        sys.stdout.write("{}执行——>【通过】\n".format(test))
        logs = []
        output = self.complete_output()
        logs.append(output)
        test.run_info = logs

    def addFailure(self, test, err):
        """
        :param test: 测试用例
        :param err:  错误信息
        :return:
        """
        super().addFailure(test, err)
        logs = []
        test.state = '失败'
        sys.stderr.write("{}执行——>【失败】\n".format(test))
        # 保存错误信息
        output = self.complete_output()
        logs.append(output)
        logs.extend(traceback.format_exception(*err))
        test.run_info = logs

    def addSkip(self, test, reason):
        """
        修改跳过用例的状态
        :param test:测试用例
        :param reason: 相关信息
        :return: None
        """
        super().addSkip(test, reason)
        test.state = '跳过'
        sys.stdout.write("{}执行--【跳过Skip】\n".format(test))
        logs = [reason]
        test.run_info = logs

    def addError(self, test, err):
        """
        修改错误用例的状态
        :param test: 测试用例
        :param err:错误信息
        :return:
        """

        super().addError(test, err)
        test.state = '错误'
        sys.stderr.write("{}执行——>【错误Error】\n".format(test))
        logs = []
        logs.extend(traceback.format_exception(*err))
        test.run_info = logs
        if test.__class__.__qualname__ == '_ErrorHolder':
            test.run_time = 0
            res = re.search(r'(.*)\(.*\.(.*)\)', test.description)
            # 获取该错误的类名
            test.class_name = res.group(2)
            # 获取错误方法名
            test.method_name = res.group(1)
            # 获取用例的描述
            test.method_doc = test.shortDescription()
            # 保存该用例执行的结果
            self.fields['results'].append(test)
            self.fields["testClass"].add(test.class_name)
        else:
            output = self.complete_output()
            logs.append(output)


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
                res = _TestResult()
                self.result.append(res)
                ts.submit(i.run, result=res).add_done_callback(res.stopTestRun)
            ts.shutdown(wait=True)
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
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        env = Environment(loader=FileSystemLoader(template_path))
        if self.templates == 2:
            template = env.get_template('templates02.html')
        else:
            template = env.get_template('templates.html')
        file_path = os.path.join(self.report_dir, self.filename)
        # 渲染报告模板
        res = template.render(test_result)
        # 输出报告到文件
        with open(file_path, 'wb') as f:
            f.write(res.encode('utf8'))

        print("测试报告已经生成，报告路径为:{}".format(file_path))


if __name__ == '__main__':
    suite1 = unittest.defaultTestLoader.discover(r"C:\project\musen\case_test")
    tr = TestRunner(suite1, title='木森的测试报告', filename="musen")
    tr.run()
