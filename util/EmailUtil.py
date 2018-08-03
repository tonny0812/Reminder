#encoding:utf-8
'''
Created on 2018年8月1日

@author: guodongqing
'''
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

senderInfo = {
    'host':'smtp.exmail.qq.com',
    'port':25,
    'address':'',
    'password':''
}

def sendEmail(receivers, subject, content): 
    try:
        if receivers is not None and subject is not None and content is not None: 
            msg = MIMEMultipart();
            msg['From'] = senderInfo['address'];
            msg['To'] = ','.join(receivers);
            msg['Subject'] = subject;
            msg.attach(MIMEText(content, 'plain', 'utf-8'));
            
            server = smtplib.SMTP(senderInfo['host'], senderInfo['port']);
            server.starttls();
            server.login(senderInfo['address'], senderInfo['password']);
            text = msg.as_string();
            server.sendmail(senderInfo['address'], receivers, text);
            server.quit();
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
