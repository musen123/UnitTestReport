import unittest
from unittestreport import TestRunner

suite = unittest.defaultTestLoader.discover(r'D:\githubcode\UnitTestReport\tests\testcases')

runner = TestRunner(suite, templates=2, report_dir='./reports')

runner.run()
#
# runner.send_email(host='smtp.qq.com',
#                   port=465,
#                   user='musen_nmb@qq.com',
#                   password='algmmzptupjccbab',
#                   to_addrs='3247119728@qq.com')


# python setup.py sdist bdist_wheel
# twine upload dist/*
