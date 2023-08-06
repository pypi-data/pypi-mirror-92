import zmail
from qm_spider import *


class Send_Mail:
    def __init__(self, subject, mail_text, file_path, send_user, send_userpwd, receivers=('ctrlf4@yeah.net'), cc=()):
        self.subject = subject
        self.mail_text = mail_text
        self.file_path = file_path
        self.receivers = receivers
        self.send_user = send_user
        self.send_userpwd = send_userpwd
        self.cc = cc

    def send_qm_mail(self):
        self.mail_content = {
            'Subject': self.subject,  # 邮件标题
            'From': self.subject, # 来自XX
            'Content_text': self.mail_text,  # 邮件正文
            'Attachments': self.file_path  # 邮件附件
        }

        if '@qimai.cn' in self.send_user:
            server = zmail.server(self.send_user, self.send_userpwd, smtp_host='smtp.exmail.qq.com', smtp_port=465)
        else:
            server = zmail.server(self.send_user, self.send_userpwd)

        if len(self.cc) > 0:
            server.send_mail(self.receivers, self.mail_content, cc=self.cc)
        else:
            server.send_mail(self.receivers, self.mail_content)
        return '%s-发送成功' %(self.subject)