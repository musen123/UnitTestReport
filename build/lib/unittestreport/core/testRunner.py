# encoding=utf-8
"""
============================
Author:柠檬班-木森
Time:2020/7/7   14:47
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import json
import os
import unittest
import time
from concurrent.futures.thread import ThreadPoolExecutor
from ..core.testResult import TestResult, ReRunResult
from ..core.resultPush import DingTalk, WeiXin, SendEmail

from jinja2 import Environment, FileSystemLoader
import copy

Load = unittest.defaultTestLoader


class TestRunner():

    def __init__(self, suite: unittest.TestSuite,
                 filename="report.html",
                 report_dir="./reports",
                 title='测试报告',
                 tester='测试员',
                 desc="XX项目测试生成的报告",
                 templates=1
                 ):
        """
        :param suites: test suite
        :param filename: Report file name
        :param report_dir:The path to the report file
        :param title:Test suite title
        :param templates: You can specify the style template for the report by parameter value 1 or 2. Currently, there are only two templates
        :param tester:Tester
        """
        if not isinstance(suite, unittest.TestSuite):
            raise TypeError("Parameter suite is not a test suite")
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

    def __classification_suite(self):
        suites_list = []

        def wrapper(suite):
            for item in suite:
                if isinstance(item, unittest.TestCase):
                    suites_list.append(suite)
                    break
                else:
                    wrapper(item)

        wrapper(copy.deepcopy(self.suite))
        return suites_list

    def __get_reports(self):
        print("所有用例执行完毕，正在生成测试报告中......")
        test_result = {
            "success": 0,
            "all": 0,
            "fail": 0,
            "skip": 0,
            "error": 0,
            "results": [],
            "testClass": [],
        }
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
        # 判断是否要生产测试报告
        if os.path.isdir(self.report_dir):
            pass
        else:
            os.mkdir(self.report_dir)
        # 获取历史执行数据
        test_result['history'] = self.__handle_history_data(test_result)

        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        env = Environment(loader=FileSystemLoader(template_path))
        if self.templates == 2:
            template = env.get_template('templates2.html')
        elif self.templates == 3:
            template = env.get_template('templates3.html')
        else:
            template = env.get_template('templates.html')
        file_path = os.path.join(self.report_dir, self.filename)
        res = template.render(test_result)
        with open(file_path, 'wb') as f:
            f.write(res.encode('utf8'))
        print("测试报告已经生成，报告路径为:{}".format(file_path))
        self.email_conent = {"file": os.path.abspath(file_path),
                             "content": env.get_template('templates03.html').render(test_result)
                             }
        self.test_result = test_result
        return test_result

    def __handle_history_data(self, test_result):
        """
        处理历史数据
        :return:
        """
        try:
            with open(os.path.join(self.report_dir, 'history.json'), 'r', encoding='utf-8') as f:
                history = json.load(f)
        except FileNotFoundError as e:
            history = []
        history.append({'success': test_result['success'],
                        'all': test_result['all'],
                        'fail': test_result['fail'],
                        'skip': test_result['skip'],
                        'error': test_result['error'],
                        'runtime': test_result['runtime'],
                        'begin_time': test_result['begin_time'],
                        'pass_rate': test_result['pass_rate'],
                        })

        with open(os.path.join(self.report_dir, 'history.json'), 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=True)
        return history

    def __get_notice_content(self):
        """获取通知的内容"""
        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        env = Environment(loader=FileSystemLoader(template_path))
        res_text = env.get_template('dingtalk.md').render(self.test_result)
        return res_text

    def run(self, thread_count=1, count=0, interval=2):
        """
        The entrance to running tests
        Note: if multiple test classes share a global variable, errors may occur due to resource competition
        :param thread_count:Number of threads. default 1
        :param count: Rerun times,  default 0
        :param interval: Rerun interval, default 2
        :return: Test run results
        """
        suites = self.__classification_suite()

        if thread_count>1:
            with ThreadPoolExecutor(max_workers=thread_count) as ts:
                for i in suites:
                    res = ReRunResult(count=count, interval=interval)
                    self.result.append(res)
                    ts.submit(i.run, result=res).add_done_callback(res.stopTestRun)
        else:
            res = ReRunResult(count=count, interval=interval)
            self.result.append(res)
            self.suite.run(res)
            res.stopTestRun()
        result = self.__get_reports()
        return result

    def rerun_run(self, count=0, interval=2):
        """
        Test case failure and error rerun mechanism
        :param count: Rerun times,  default 0
        :param interval: Rerun interval, default 2
        :return: Test run results
        """
        res = ReRunResult(count=count, interval=interval)
        self.result.append(res)
        suites = self.__classification_suite()
        for case_ in suites:
            case_.run(res)
        res.stopTestRun()
        res = self.__get_reports()
        return res

    def send_email(self, host: str, port: int, user: str, password: str, to_addrs, is_file=True):
        """
        The occurrence report is attached to the mailbox
        :param host: SMTP server address
        :param port: SMTP server port
        :param user: Email account number
        :param password: SMTP service authorization code of mailbox
        :param to_addrs: Addressee's address str or list
        :return:
        """
        sm = SendEmail(host=host, port=port, user=user, password=password)
        if is_file:
            filename = self.email_conent["file"]
        else:
            filename = None
        content = self.email_conent["content"]

        sm.send_email(subject=self.title, content=content, filename=filename, to_addrs=to_addrs)

    def get_except_info(self):
        """Get error reporting information for error cases and failure cases"""
        except_info = []
        num = 0
        for i in self.result:
            for texts in i.failures:
                t, content = texts
                num += 1
                except_info.append("*{}、用例【{}】执行失败*，\n失败信息如下：".format(num, t._testMethodDoc))
                except_info.append(content)
            for texts in i.errors:
                num += 1
                t, content = texts
                except_info.append("*{}、用例【{}】执行错误*，\n错误信息如下：".format(num, t._testMethodDoc))
                except_info.append(content)
        except_str = "\n".join(except_info)
        return except_str

    def dingtalk_notice(self, url, key=None, secret=None, atMobiles=None, isatall=False, except_info=False):
        """
        :param url: 钉钉机器人的Webhook地址
        :param key: （非必传：str类型）如果钉钉机器人安全设置了关键字，则需要传入对应的关键字
        :param secret:（非必传:str类型）如果钉钉机器人安全设置了签名，则需要传入对应的密钥
        :param atMobiles: （非必传，list类型）发送通知钉钉中要@人的手机号列表，如：[137xxx,188xxx]
        :param isatall: 是否@所有人，默认为False,设为True则会@所有人
        :param except_info:是否发送未通过用例的详细信息，默认为False，设为True则会发送失败用例的详细信息
        :return:  发送成功返回 {"errcode":0,"errmsg":"ok"}  发送失败返回 {"errcode":错误码,"errmsg":"失败原因"}
        """

        res_text = self.__get_notice_content()
        if except_info:
            res_text += '\n ### 未通过用例详情：\n'
            res_text += self.get_except_info()
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": '{}({})'.format(self.title, key),
                "text": res_text
            },
            "at": {
                "atMobiles": atMobiles,
                "isAtAll": isatall
            }
        }
        ding = DingTalk(url=url, data=data, secret=secret)
        response = ding.send_info()
        return response.json()

    def weixin_notice(self, chatid, access_token=None, corpid=None, corpsecret=None):
        """
        测试结果推送到企业微信群，【access_token】和【corpid，corpsecret】至少要传一种
        可以传入access_token ,也可以传入（corpid，corpsecret）来代替access_token
        :param chatid: 企业微信群ID
        :param access_token: 调用企业微信API接口的凭证
        :param corpid: 企业ID
        :param corpsecret:应用的凭证密钥
        :return:
        """
        # 获取通知结果
        res_text = self.__get_notice_content()
        data = {
            "chatid": chatid,
            "msgtype": "markdown",
            "markdown": {
                "content": res_text
            }
        }
        wx = WeiXin(access_token=access_token, corpid=corpid, corpsecret=corpsecret)
        response = wx.send_info(data=data)
        return response
