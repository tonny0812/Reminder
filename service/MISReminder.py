#encoding:utf-8
'''
Created on 2018年8月1日

@author: guodongqing
'''

import schedule
from util import EmailUtil, SMSUtil

class MISReminder():
    def __init__(self,queue):
        self.userQueue = queue
        
    def job(self):
        self.sendMessage();
    
    def sendMessage(self):
        user = self.userQueue.deQueue();
        eReceivers = [];
        tReceivers = [];
        if user:
            eReceivers.append(user['email']);
            tReceivers.append(user['tel']);
            content = user['name'] +'(' + user['account'] +')' + '负责这周巡检，访问地址：http://union.vip.58.com/bsp/index';
            EmailUtil.sendEmail(eReceivers, '巡检轮班', content)
            msg = "【巡检轮班】" + user['name'] +'(' + user['account'] +')' + '负责这周巡检';
            SMSUtil.sendSMS(tReceivers, msg)
            print('--------order:' + str(user['order']), user['name'] +'(' + user['account'] +')' + '负责巡检。。。')
        self.userQueue.enQueue(user);
    
    def setSchdeule(self, job):
        schedule.every().monday.at("9:30").do(job);
    
    def scheduleCheck(self):
        schedule.run_pending();