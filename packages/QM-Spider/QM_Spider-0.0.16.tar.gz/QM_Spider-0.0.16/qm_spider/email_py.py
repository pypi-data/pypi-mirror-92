import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication
from qm_spider import *


class Send_Mail:
    def __init__(self, subject, mail_text, file_path, file_name, send_user, send_userpwd, receivers=('1013373636@qq.com')):
        self.subject = subject
        self.mail_text = mail_text
        self.file_path = file_path
        self.file_name = file_name
        self.receivers = receivers
        self.send_user = send_user
        self.send_userpwd = send_userpwd

    def send_qm_mail(self):
         sender = 'liliucheng@qimai.cn'
         receivers = self.receivers
         # 创建一个带附件的实例
         message = MIMEMultipart()
         message['From'] = Header("七麦-掉词数据周报", 'utf-8')
         message['To'] = Header("商务", 'utf-8')
         username = 'liliucheng@qimai.cn'
         password = 'Ck3+d.Ek3Z>#m4DrV2'
         message['Subject'] = Header(self.subject, 'utf-8')

         # 邮件正文内容
         message.attach(MIMEText(self.mail_text, 'plain', 'utf-8'))

         # 构造附件1，传送当前目录下的 test.txt 文件
         att1 = MIMEApplication(open(self.file_path, 'rb').read())
         # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
         att1.add_header('Content-Disposition', 'attachment', filename=('gbk', '', self.file_name))
         message.attach(att1)

         try:
              smtp = smtplib.SMTP()
              smtp.connect('smtp.exmail.qq.com')
              smtp.login(username, password)
              smtp.sendmail(sender, receivers, message.as_string())
              print("邮件发送成功")

              # 发送成功后推送一条钉钉消息；
              push_title = '商务-掉词数据周报'
              push_status = '推送成功'
              dingding_push_markdown(push_title, push_status, today_time)

              return "邮件发送成功"
         except smtplib.SMTPException:
              return "Error: 无法发送邮件"