"""
============================
Author:柠檬班-木森
Time:2020/8/19   17:46
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
# from unittestreport import ddt, data
import time
import unittest
#
# from unittestreport.core.dataDriver import ddt, list_data, json_data, yaml_data
#
# @ddt
# class TestClass(unittest.TestCase):
#     apitest = [{'case_id': 1, 'title': '用例1', 'data': '用例参数', 'expected': '预期结果'},
#              {'case_id': 2, 'title': '用例2', 'data': '用例参数', 'expected': '预期结果'},
#              {'case_id': 3, 'title': '用例3', 'data': '用例参数', 'expected': '预期结果'}]
#
#     @list_data(range(501))
#     def test_case(self, data):
#         print(data)
#         time.sleep(2)
#
#
#
# # @yaml_data("apitest.yaml")
# # def test_case02(self, data):
# #     pass
# #
#
# from parameterized import parameterized
#
#
# class TestClass2(unittest.TestCase):
#
#     @parameterized.expand([
#         {"case_id": "11", "case_data": 22, "expected": '99'},
#         {"case_id": "11", "case_data": 22, "expected": '99'},
#         {"case_id": "11", "case_data": 22, "expected": '99'},
#     ])
#     def test_case_01(self, case_id, case_data, expected):
#         a = 100
#         b = 99
#         assert a == 100
#
#     def test_case_02(self):
#         a = 100
#         b = 100
#         assert a == b
#
#
