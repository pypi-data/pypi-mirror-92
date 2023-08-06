#!/usr/bin/env python
# -*-coding:utf-8-*-

import mimetypes
import os
import smtplib
import time
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from os.path import getsize


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


class EmailClient:
    def __init__(self, **kwargs):
        """
        constructor
        :param kwargs:Variable paramete
        """
        self.kwargs = kwargs
        self.MAX_FILE_SIZE = 100 * 1024 * 1024

    def __get_cfg(self, key, throw=True):

        """
        get the configuration file based on the key
        :param key:
        :param throw:
        :return:
        """
        cfg = self.kwargs.get(key)
        if throw and (cfg is None or cfg == ''):
            raise Exception("The configuration can't be empty", 'utf-8')
        return cfg

    def __init_cfg(self):
        self.smtp_server = self.__get_cfg('smtp_server')
        self.msg_from = self.__get_cfg('msg_from')
        self.password = self.__get_cfg('password')
        self.msg_from_format = self.__get_cfg('msg_from_format')
        self.msg_to = ','.join(self.__get_cfg('msg_to'))
        self.msg_subject = self.__get_cfg('msg_subject')
        self.msg_content = self.__get_cfg('msg_content')
        self.msg_date = self.__get_cfg('msg_date')

        self.attach_files = self.__get_cfg('attach_files', throw=False)

    def login_server(self):

        """
        login server
        :return:
        """
        server = smtplib.SMTP_SSL(self.smtp_server, 465)
        server.set_debuglevel(1)
        server.login(self.msg_from, self.password)
        return server

    def get_main_msg(self):
        """
        suject content
        :return:
        """
        msg = MIMEMultipart()
        # message content
        msg.attach(MIMEText(self.msg_content, 'plain', 'utf-8'))
        msg['From'] = _format_addr(self.msg_from_format % self.msg_from)
        msg['To'] = self.msg_to
        msg['Subject'] = Header(self.msg_subject, 'utf-8')
        msg['Date'] = self.msg_date

        # attachment content
        if self.attach_files is not None and self.attach_files != '':
            for attach_file in self.attach_files:
                attach_file_result = self.get_attach_file(attach_file)
                if attach_file_result is not None:
                    msg.attach(attach_file_result)
        return msg

    def get_attach_file(self, attach_file):
        """
        generate mail attachment content
        :param attach_file:     附件地址
        :return:
        """
        if attach_file is not None and attach_file != '':
            try:
                if getsize(attach_file) > self.MAX_FILE_SIZE:
                    raise Exception('The attachment is too large and the upload failed!!')
                with open(attach_file, 'rb') as file:
                    ctype, encoding = mimetypes.guess_type(attach_file)
                    if ctype is None or encoding is not None:
                        ctype = 'application/octet-stream'
                    maintype, subtype = ctype.split('/', 1)
                    mime = MIMEBase(maintype, subtype)
                    mime.set_payload(file.read())
                    # set header
                    mime.add_header('Content-Disposition', 'attachment',
                                    filename=os.path.basename(attach_file))
                    mime.add_header('Content-ID', '<0>')
                    mime.add_header('X-Attachment-Id', '0')

                    # set the attachment encoding rules
                    encoders.encode_base64(mime)
                    return mime

            except Exception as e:
                print('%s......' % e)
                return None
        else:
            return None

    def send(self):
        try:
            # initialize the configuration file
            self.__init_cfg()
            # log on to the SMTP server and verify authorization
            server = self.login_server()
            # mail content
            msg = self.get_main_msg()
            # send mail
            server.sendmail(self.msg_from, self.__get_cfg('msg_to'), msg.as_string())
            server.quit()
            print("Send succeed!!")

        except smtplib.SMTPException:
            print("Error:Can't send this email!!")


if __name__ == "__main__":
    mail_cfgs = {
        # smtp发送邮件服务器
        'smtp_server': 'your smtp_server',
        # 发件人邮箱
        'msg_from': 'your email',
        # 发件人授权码(不是密码)
        'password': 'your email password',
        # 发件人格式化显示文案   效果：DataWorks对账系统 <your email>
        'msg_from_format': 'DataWorks对账系统 <%s>',
        # 收件人邮箱列表
        'msg_to': ['receiver email 1', 'receiver email 2'],
        # 邮件主题
        'msg_subject': 'DataWorks对账系统警报邮件',
        # 邮件内容
        'msg_content': 'DataWorks对账系统警报:\n \t 日收入对账异常，日对账差异明细详情请查看附件。',
        # 邮件附件
        'attach_files': ['xxx.xlsx'],
        # 邮件发送时间
        'msg_date': time.ctime()
    }

    manager = EmailClient(**mail_cfgs)
    manager.send()
