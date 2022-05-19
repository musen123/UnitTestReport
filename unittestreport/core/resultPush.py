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
    """Send mail"""

    def __init__(self, host, user, password, port=465):
        """
        :param host: smtp server address
        :param port: smtp server report
        :param user: Email account number
        :param password: SMTP service authorization code of mailbox
        """
        if port == 465 or port == 587:
            self.smtp = smtplib.SMTP_SSL(host=host, port=port)
        else:
            self.smtp = smtplib.SMTP(host=host, port=port)
        self.smtp.ehlo()

        self.smtp.login(user=user, password=password)
        self.user = user

    def send_email(self, subject="test report", content=None, filename=None, to_addrs=None):
        """
        :param subject:Email subject
        :param content: Email content
        :param filename: Attachment document
        :param to_addrs: Addressee's address
        :type to_addrs: str or list
        :return:
        """
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.user
        if isinstance(to_addrs, str):
            msg["To"] = to_addrs
        elif to_addrs and isinstance(to_addrs, list):
            msg["To"] = to_addrs[0]
        if not content:
            content = time.strftime("%Y-%m-%d-%H_%M_%S") + ":测试报告"
        text = MIMEText(content, _subtype="html", _charset="utf8")
        msg.attach(text)
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
        try:
            self.smtp.send_message(msg, from_addr=self.user, to_addrs=to_addrs)
        except Exception as e:
            print("Failed to send test report")
            raise e
        else:
            print("The test report has been sent")


class DingTalk:
    """Nail group notification occurred"""

    def __init__(self, url, data, secret=None):
        """
        :param url: Dingtalk robot webhook address
        :param data:Message sent (refer to the official message type)
        :param secret: (not required) if the robot has set the signature security, it needs to pass in the signature key
        """
        self.url = url
        self.data = data
        self.secret = secret

    def get_stamp(self):
        """Countersign"""
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return {"sign": sign, "timestamp": timestamp}

    def send_info(self):
        """send info"""
        if self.secret:
            params = self.get_stamp()
        else:
            params = None
        response = requests.post(url=self.url, json=self.data, params=params)
        return response


class WeiXin:
    """
    Enterprise wechat group notice
    """
    base_url = "https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token="

    def __init__(self, access_token=None, corpid=None, corpsecret=None):
        """
        :param corpid:wechat corpid
        :param corpsecret:Applied credential key
        """
        self.corpid = corpid
        self.corpsecret = corpsecret
        if access_token:
            self.access_token = access_token
        elif corpid and corpsecret:
            self.access_token = self.get_access_token()
        else:
            raise ValueError("access_token and [corpid, corpsecret] cannot both be empty. At least one of them must be passed in")

    def get_access_token(self):
        """get access_token"""
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.corpid,
            "corpsecret": self.corpsecret
        }
        result = requests.get(url=url, params=params).json()
        if result['errcode'] != 0:
            raise ValueError(result["errmsg"])
        return result["access_token"]

    def send_info(self, data):
        """send info"""
        url = self.base_url + self.access_token
        response = requests.post(url=url, json=data)
        return response



