#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@software: Pycharm
@file: mail.py
@time: 2019/8/1 15:42
@desc:
'''
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
import os.path
import mimetypes


class Mail():
    def __init__(self):
        # 输入SMTP服务器地址:
        self.smtp_server = 'smtp.qq.com'
        self.smtp_port = 587
        # Email地址和口令:
        self.from_addr = '发送者的QQ邮箱'
        self.password = 'QQ邮箱授权码'
        #收件人地址:
        self.to_addr = '收件人QQ邮箱'
        self.msg = MIMEMultipart()
        # 定义邮件信息
        self.msg['From'] = self._format_addr('Maya <%s>' % self.from_addr)
        self.msg['To'] = self._format_addr('Receiver <%s>' % self.to_addr)
        self.msg['Subject'] = Header('测试一下发送邮件的代码……', 'utf-8').encode()

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def withAnnex(self, filePath):
        ctype, encoding = mimetypes.guess_type(filePath)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)

        # 添加附件就是加上一个MIMEBase:
        with open(filePath, 'rb') as f:
            # 设置附件的MIME和文件名,这里通过mimetypes获取
            mime = MIMEBase(maintype, subtype, filename=os.path.basename(filePath))
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filePath))
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            self.msg.attach(mime)

    def sendMail(self):
        # 先创建SSL安全连接，然后再使用SMTP协议发送邮件
        server = smtplib.SMTP(self.smtp_server, self.smtp_port) # SMTP协议默认端口是25
        server.starttls()
        # 邮件正文是MIMEText:
        self.msg.attach(MIMEText('这只是一个测试的邮件', 'plain', 'utf-8'))
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, [self.to_addr], self.msg.as_string())
        server.quit()


if __name__ == '__main__':
    mail = Mail()
    mail.withAnnex('添加文件1')
    mail.withAnnex('添加文件2')
    mail.sendMail()
