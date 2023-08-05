#!/usr/bin/env python3
# file: mail.py
# author: walker

"""
Changelogs

2018.06.29: init
2020.04.18: 支援io.BytesIO附件 

"""

import os
import sys
import smtplib
import traceback
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class Mail(object):

    def __init__(self, host, port, user='', pwd=''):
        """
        :param host(str): 邮件服务器主机
        :param port(int): Port
        :param user(str): 登入帐号
        :param pwd(str): 密码
        """
        self.mail = smtplib.SMTP(host, port)
        try:
            self.mail.starttls()
        except smtplib.SMTPNotSupportedError:
            pass
        if user and pwd:
            self.mail.login(user, pwd)
        
    def send(self, subject, content, _from, _to, _cc=[], _bcc=[], _file=[], _img=[]):
        """
        :param subject(str): 标题
        :param content(str): 邮件内容
        :param _from(str): 发件人
        :param _to(list): 收件人
        :param _cc(list): 抄送
        :param _bcc(list): 密本抄送
        :param _file(list): 附件, [文件名]或是[[文件名, io.BytesIO]]
        :param _img(str): 邮件内容有嵌图片时使用
        """

        if isinstance(_to, str):
            _to = [_to]
        if _cc and isinstance(_cc, str):
            _cc = [_cc]
        if _bcc and isinstance(_bcc, str):
            _bcc = [_bcc]

        msg = MIMEMultipart()
        msg['to'] = ','.join(_to)
        msg['cc'] = ','.join(_cc)
        msg['from'] = _from
        msg['subject'] = subject

        # HTML Content 
        content = MIMEText(content, 'html', 'utf-8')
        msg.attach(content)

        # with Picture
        if _img:
            for n in _img:
                with open(n, 'rb') as f: img = f.read()
                msg_image = MIMEImage(img)
                msg_image.add_header('Content-ID', filename)
                msg.attach(msg_image)

        # Attachment
        for n in _file:
            if isinstance(n, str):
                filename = n
                attach = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
                attach.add_header('Content-Type', 'application/octet-stream')
                attach.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(attach)
            elif isinstance(n, list):
                filename, cache = n
                attach = MIMEText(cache.read(), 'base64', 'utf-8')
                attach.add_header('Content-Type', 'application/octet-stream')
                attach.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(attach)

        _From = _from
        _To = _to + _cc + _bcc

        self.mail.sendmail(_From, _To, msg.as_string())

    def close(self):
        self.mail.quit()

if __name__ == '__main__':

    os.chdir(sys.path[0])

    _from = 'XXXX'
    _to = 'YYYY'

    ## Local
    #mail = Mail(host='127.0.0.1', port=25)
    ## Gmail
    #mail = Mail(host='smtp.gmail.com', port=587, user='XXXX', pwd='XXXXX')

    subject = 'Python Test %s'%(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    content = 'This is a Test!!!'

    mail.send(subject, content, _from, _to)

