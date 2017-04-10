# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class SJTU_Mail:
    def __init__(self,username,password):
        self.sender = username+'@sjtu.edu.cn'
        self.receiver = self.sender
        self.smtpserver = 'smtp.sjtu.edu.cn'
        self.username = self.sender
        self.password = password

    def send_mail(self,header,text):
        msg = MIMEText(text,'plain','utf-8')
        msg['Subject'] = Header(header, 'utf-8')
        smtp = smtplib.SMTP()
        smtp.connect(self.smtpserver)
        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, self.receiver, msg.as_string())
        smtp.quit()
