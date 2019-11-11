#encoding:utf-8
'''
Created on 2018年8月1日

@author: guodongqing
'''

import schedule
from util.DateUtil import getCurrentDate, isWorkDay
from util import EmailUtil, SMSUtil, DateUtil

class MeetingReminder():
    def __init__(self,queue):
        self.userQueue = queue
        
    def job(self):
        if isWorkDay(getCurrentDate()):
            self.sendMessage();
        else:
            print(getCurrentDate() + '是假日！');
    
    def sendMessage(self):
        user = self.userQueue.deQueue();
        eReceivers = [];
        tReceivers = [];
        if user:
            eReceivers.append(user['email']);
            tReceivers.append(user['tel']);
            content = user['name'] +'(' + user['account'] +')' + '负责今天('+ getCurrentDate() +')早会';
            EmailUtil.sendEmail(eReceivers, '主持早会', content)
            msg = "【主持早会】" + user['name'] +'(' + user['account'] +')' + '负责今天('+ getCurrentDate() +')早会';
            SMSUtil.sendSMS(tReceivers, msg)
            r = '--------order:' + str(user['order']) + ' ' + user['name'] +'(' + user['account'] +')' + '负责今天('+ DateUtil.getCurrentDate() +')早会。。。'
            print(r)
        self.userQueue.enQueue(user);
    
    def setSchdeule(self, job):
#         schedule.every().day.at("7:00").do(job);
        schedule.every(10).seconds.do(job);
    
    def scheduleCheck(self):
        schedule.run_pending();
    