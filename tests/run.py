"""
============================
Author:柠檬班-木森
Time:2020/8/19   17:48
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import unittest

from unittestreport import TestRunner

suite = unittest.defaultTestLoader.discover(r'C:\project\MSUnitTestReport\UnitTestReport\tests')
runner = TestRunner(suite=suite,
                    title="接口自动化测试报告",
                    templates=1)

runner.run()

# error_info = runner.get_except_info()

# 推送测试结果到企业微信
# runner.weixin_notice(chatid="群id", access_token="调用企业微信API接口的凭证")

# 发送右击
# runner.send_email(host="smtp.qq.com",
#                   port=465,
#                   user="musen_nmb@qq.com",
#                   password="algmmzptupjccbab",
#                   to_addrs="3247119728@qq.com")
# 钉钉机器人webhork地址
# url = "https://oapi.dingtalk.com/robot/send?access_token=6e2a63c2b9d870ee878335b5ce6d5d10bb1218b8e64a4e2b55f96a6d116aaf50"
# # 发生钉钉通知
# runner.dingtalk_notice(url=url, except_info=True)


# 推送测试结果到企业微信
# runner.weixin_notice(chatid="群id", access_token="调用企业微信API接口的凭证")
