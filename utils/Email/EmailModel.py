# _*_coding:utf-8 _*_
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import parseaddr, formataddr
import smtplib
import os
from loguru import logger

from utils.util_functions import cfg_parse


'''
-------------------------------------------------
   @File Name :     EmailModel
   @Description :   create a class to auto send email
   @Author :        YYP
   @date :          2020/4/26
   @modify :        2020/4/26
-------------------------------------------------
'''


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


class EmailModel:
    def __init__(self):
        self.send_from = None
        self.send_pwd = None
        self.send_to = None
        self.email_server = None
        self._enclosure = []
        self._msg = ''
        self._msg_type = 'plain'
        self._encoding = 'utf-8'
        self._subject = ''
        self.__init()
        self.server = smtplib.SMTP(self.email_server, 25)
        self.server.login(self.send_from, self.send_pwd)
        self.server.set_debuglevel(1)

    @property
    def have_enclosure(self):
        if self._enclosure:
            return True
        else:
            return False

    @property
    def enclosure(self):
        return self._enclosure

    @enclosure.setter
    def enclosure(self, enclosure_):
        assert isinstance(enclosure_, list), '请传入一个列表'
        self._enclosure = enclosure_

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, coding):
        self._encoding = coding

    @property
    def msg_type(self):
        return self._msg_type

    @msg_type.setter
    def msg_type(self, sub_type):
        self._msg_type = sub_type

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, msg_info):
        self._msg = msg_info

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, sub):
        self._subject = Header(sub, 'utf-8').encode()

    def __init(self):
        email_info = cfg_parse(os.path.join('EmailConfig', 'EmailSettings.cfg'))
        self.send_from = email_info.get('Email', 'From')
        self.send_pwd = email_info.get('Email', 'PassWord')
        self.send_to = email_info.get('Email', 'To').split(',')
        self.email_server = email_info.get('Email', 'SmtpServer')

    def sendmail(self):
        if self.have_enclosure == True:
            msg = MIMEMultipart()
            msg.attach(MIMEText(self.msg, self.msg_type, self.encoding))
            for each_enclosure_path in self.enclosure:
                if os.path.splitext(each_enclosure_path)[1] == '.txt':
                    add_enclosure = MIMEText(open(each_enclosure_path, 'rb').read(), 'base64', 'utf-8')
                    add_enclosure["Content-Type"] = 'application/octet-stream'
                    add_enclosure["Content-Disposition"] = 'attachment; filename="{}"'.format(os.path.basename(each_enclosure_path))
                else:
                    add_enclosure = MIMEApplication(open(each_enclosure_path, 'rb').read(), self.encoding)
                    add_enclosure.add_header('Content-Disposition', 'attachment', filename="{}".format(os.path.basename(each_enclosure_path)))
                msg.attach(add_enclosure)
        else:
            msg = MIMEText(self.msg, self.msg_type, self.encoding)

        # 邮件头信息
        msg['From'] = _format_addr('网易邮箱发送<%s>' % self.send_from)
        msg['To'] = _format_addr('腾讯邮箱接收<%s>' % (''.join(self.send_to)))
        msg['Subject'] = self.subject
        try:
            self.server.sendmail(self.send_from, self.send_to, msg.as_string())
        except smtplib.SMTPException as e:
            logger.error('邮件发送失败！！！')
            logger.error('失败原因:{}'.format(str(e)))

    def __del__(self):
        self.server.quit()



if __name__ == "__main__":
    email_model = EmailModel()
    email_model.msg = '这是一个测试邮件'  # 设置发送内容
    email_model.subject = '测试邮件'  # 设置发送主题
    email_model.enclosure = [r'C:\Users\Administrator\Desktop\test.txt']  # 添加待添加附件
    email_model.sendmail()