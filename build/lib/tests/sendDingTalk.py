"""
============================
Author:柠檬班-木森
Time:2020/9/1   11:41
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import requests


class SendDingTalk:
    """发送测试结果到钉钉群"""

    def __init__(self, access_token, chat_id, ):
        """初始化消息"""
        self.url = "https://oapi.dingtalk.com/chat/send?access_token={}".format(access_token)
        self.chat_id = chat_id

    def send_info(self, msg):
        requests.post(url=self.url)
