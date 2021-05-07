"""
============================
Author:柠檬班-木森
Time:2020/11/25  14:14
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import hmac
import hashlib
import base64
import urllib.parse
import requests
import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


class SendEmail:
    """发送邮件"""

    def __init__(self, host, user, password, port=465):
        """
        初始化设置
        :param host: smtp服务器地址（qq邮箱：smtp.qq.com，163邮箱：smtp.163.com"）
        :param port: smtp服务器端口：
        :param user: 邮箱账号
        :param password: 邮箱的smtp服务授权码
        """
        if port == 465 or port == 587:
            self.smtp = smtplib.SMTP_SSL(host=host, port=port)
        else:
            self.smtp = smtplib.SMTP(host=host, port=port)
        self.smtp.login(user=user, password=password)
        self.user = user

    def send_email(self, subject="测试报告", content=None, filename=None, to_addrs=None):
        """
        发送邮件
        :param subject: 邮件主题
        :param content: 邮件内容
        :param filename: 报告文件的完整路径
        :param to_addrs: 收件人地址
        :type to_addrs: str or list
        :return:
        """
        print("--------准备发送测试报告---------")
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.user
        if isinstance(to_addrs, str):
            msg["To"] = to_addrs
        elif to_addrs and isinstance(to_addrs, list):
            msg["To"] = to_addrs[0]
        if not content:
            content = time.strftime("%Y-%m-%d-%H_%M_%S") + ":测试报告"
        # 构建邮件的文本内容
        text = MIMEText(content, _subtype="html", _charset="utf8")
        msg.attach(text)
        # 判断是否要发送附件
        if filename and os.path.isfile(filename):
            with open(filename, "rb") as f:
                content = f.read()
            try:
                report = MIMEApplication(content, _subtype=None)
            except:
                report = MIMEApplication(content)
            name = os.path.split(filename)[1]
            report.add_header('content-disposition', 'attachment', filename=name)
            msg.attach(report)
        # 第三步：发送邮件
        try:
            self.smtp.send_message(msg, from_addr=self.user, to_addrs=to_addrs)
        except Exception as e:
            print("--------测试报告发送失败------")
            raise e
        else:
            print("--------测试报告发送完毕------")


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


class WeiXin:
    """
    企业微信群通知
    """
    base_url = "https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token="

    def __init__(self, access_token=None, corpid=None, corpsecret=None):
        """
        :param corpid:企业ID，
        :param corpsecret:应用的凭证密钥
        """
        self.corpid = corpid
        self.corpsecret = corpsecret
        if access_token:
            self.access_token = access_token
        elif corpid and corpsecret:
            self.access_token = self.get_access_token()
        else:
            raise ValueError("access_token和【corpid,corpsecret】不能都为空，至少要传入一种")

    def get_access_token(self):
        """获取access_token"""
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.corpid,
            "corpsecret": self.corpsecret
        }
        result = requests.get(url=url, params=params).json()
        if result.json()['errcode'] != 0:
            raise ValueError(result["errmsg"])
        return result["access_token"]

    def send_info(self, data):
        """发送消息"""
        url = self.base_url + self.access_token
        response = requests.post(url=url, data=data)
        return response


if __name__ == '__main__':
    url = "https://oapi.dingtalk.com/robot/send?access_token=690900b5ce6d5d10bb1218b8e64a4e2b55f96a6d116aaf50"
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "自动化测试报告",
            "text": open('python31.md', 'r', encoding='utf-8').read()
        },
        "at": {
            "atMobiles": [],
            "isAtAll": False
        }
    }
    ding = DingTalk(url=url, data=data)
    res = ding.send_info()
    print(res)
