"""
============================
Author:柠檬班-木森
Time:2021/2/4 17:23
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
=======
"""
from unittestreport.apitest.request import CaseData
from unittestreport.apitest.tasecase import HttpCase


class TestLogin(HttpCase):
    host = "http://api.lemonban.com/futureloan/"
    headers = {
        "X-Lemonban-Media-Type": "lemonban.v1"
    }
    method = 'post'
    interface = "member/login"
    Cases = [
        {'title': "登录成功",
         'host': "http://api.lemonban.com/futureloan/",
         "interface": "member/login",
         "method": "post",
         'json': {
             "mobile_phone": "13367877876",
             "pwd": "lemonban"
         },

         },
        {'title': "登录成功",
         'json': {
             "mobile_phone": "13367877876",
             "pwd": "lemonban"
         },
         }
    ]


class TestLogin2(HttpCase):
    host = "http://api.lemonban.com/futureloan/"
    headers = {
        "X-Lemonban-Media-Type": "lemonban.v1"
    }
    method = 'post'

    Cases = [
        CaseData(
            host="http://api.lemonban.com/futureloan/",
            headers={
                "X-Lemonban-Media-Type": "lemonban.v1"
            },
            method='post',
            title="登录成功",
            interface="member/login",
            json={
                "mobile_phone": "13367877876",
                "pwd": "lemonban"
            },
        ),
        CaseData(
            title="登录成功",
            interface="member/login",
            json={
                "mobile_phone": "13367877876",
                "pwd": "lemonban"
            },
        )
    ]

# class TestLogin2(HttpCase):
#     class Data:
#         case_id = "login-01",
#         title = "登录成功",
#         host = "http://api.lemonban.com/futureloan/"
#         interface = "member/register"
#         request_data = {
#             "method": "post",
#             'json': {
#                 "mobile_phone": "13367877876",
#                 "pwd": "lemonban"
#             },
#             "headers": {
#                 "X-Lemonban-Media-Type": "lemonban.v1"
#             }
#         }
#         verification = {
#
#         }
