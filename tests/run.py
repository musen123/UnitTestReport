"""
============================
Project: UnitTestReport
Author:柠檬班-木森
Time:2021/8/4 15:48
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
Site: http://www.lemonban.com
Forum: http://testingpai.com 
============================
"""
import unittest
from unittestreport import TestRunner

suite = unittest.defaultTestLoader.discover(r'C:\git_project\UnitTestReport\tests\testcases')

runner = TestRunner(suite,templates=2,report_dir='./reports')

runner.run()

runner.send_email(host='smtp.qq.com',
                  port=465,
                  user='musen_nmb@qq.com',
                  password='algmmzptupjccbab',
                  to_addrs='3247119728@qq.com')


# python setup.py sdist bdist_wheel
# twine upload dist/*

"""
pypi-AgEIcHlwaS5vcmcCJGE4ODRmMDM5LTUwMTQtNDZjMy1hY2ZlLTE2M2YzYzg5YTgzMwACFlsxLFsidW5pdHRlc3RyZXBvcnQiXV0AAixbMixbIjIzZmM2ZTYyLWIyMTMtNGIzMC04NjQyLWFlY2VhZTY4MGUzZCJdXQAABiB7heBzh7qrPDT-_y9YJaWXgMACfOMsNWaJ-7YlSgcJ8w

"""