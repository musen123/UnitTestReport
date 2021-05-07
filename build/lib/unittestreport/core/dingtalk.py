"""
============================
Author:柠檬班-木森
Time:2020/11/25  14:14
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests


class DingTalk:
    """发生钉钉群通知"""

    def __init__(self, url, data, secret=None):
        """
        初始化机器人对象
        :param url:钉钉机器人webhook地址
        :param data:发送的消息（参照钉钉官方的消息类型）
        :param secret: (非必填)如果机器人安全设置了加签，则需要传入加签的秘钥
        """
        self.url = url
        self.data = data
        self.secret = secret

    def get_stamp(self):
        """加签"""
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return {"sign": sign, "timestamp": timestamp}

    def send_info(self):
        """发送消息"""
        # 判断是否需要加签
        if self.secret:
            params = self.get_stamp()
        else:
            params = None
        # 发送请求
        response = requests.post(url=self.url, json=self.data, params=params)
        return response


if __name__ == '__main__':
    url = "https://oapi.dingtalk.com/robot/send?access_token=6e2a63c2b9d870ee878335b5ce6d5d10bb1218b8e64a4e2b55f96a6d116aaf50"
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "自动化测试报告",
            "text": '测试'
        },
        "at": {
            "atMobiles": [],
            "isAtAll": False
        }
    }
    ding = DingTalk(url=url, data=data)
    res = ding.send_info()
    print(res.text)