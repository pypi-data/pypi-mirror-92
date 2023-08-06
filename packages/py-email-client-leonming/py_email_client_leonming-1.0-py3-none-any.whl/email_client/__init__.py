__all__ = ['email_client']

"""
使用方法：

发送邮件工具类

import email_client

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
                 'attach_file': ['attach_file_1','attach_file_2'],
                 # 邮件发送时间
                 'msg_date': time.ctime()
                 }

    manager = emailclient.create(**mail_cfgs)
    manager.send()
"""
from email_client.email_client import EmailClient


def create(**kwargs):
    """
    创建EmailClient实例
    :param kwargs:
    :param smtp_server: smtp发送邮件服务器
    :param msg_from: 发件人邮箱
    :param password: 发件人授权码
    :param msg_from_format: 发件人格式化显示文案
    :param msg_to: 收件人邮箱列表
    :param msg_subject: 邮件主题
    :param msg_content: 邮件内容
    :param attach_file: 邮件附件
    :param msg_date: 邮件发送时间
    :param kwargs:
    :return:
    """
    return EmailClient(**kwargs)
