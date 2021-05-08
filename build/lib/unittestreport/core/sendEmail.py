"""
============================
Author:柠檬班-木森
Time:2020/8/31   14:48
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


class EmailConf:
    EmailQQ = {"host": "smtp.qq.com", "port": 465}
    Email163 = {"host": "smtp.163.com", "port": 465}


class SendEmail:
    """发送邮件"""

    def __init__(self, host, user, password, port=465):
        """
        初始化设置
        :param host: smtp服务器地址（qq邮箱：smtp.qq.com，163邮箱：smtp.163.com"）
        :param port: smtp服务器端口：465
        :param user: 邮箱账号
        :param password: 邮箱的smtp服务授权码
        """
        self.smtp = smtplib.SMTP_SSL(host=host, port=port)
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
            report = MIMEApplication(content, _subtype=None)
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
