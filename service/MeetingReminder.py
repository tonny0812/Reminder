# encoding:utf-8
'''
Created on 2018年8月1日

@author: guodongqing
'''

import schedule
from util import EmailUtil, SMSUtil, DateUtil
from util.DateUtil import getCurrentDate, isWorkDay
from util.Logger import Logger

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MeetingReminder(object):
    _logger = Logger()

    def __init__(self, queue):
        self.userQueue = queue

    def job(self):
        if isWorkDay(getCurrentDate()):
            self.sendMessage()
        else:
            print(getCurrentDate() + '是假日！')

    def sendMessage(self):
        try:
            user = self.userQueue.deQueue()
            _r = '--------order:' + str(
                user.order) + '---' + user.name + '(' + user.account + ')负责今天(' + DateUtil.getCurrentDate() + ')早会------------'
            _r2 = '--------order:%s---%s(%s)负责今天(%s)早会------------' % (str(user.order),user.name,user.account,DateUtil.getCurrentDate())
            self._logger.info(_r2)
            eReceivers = []
            tReceivers = []
            if user:
                eReceivers.append(user.email)
                tReceivers.append(user.tel)
                try:
                    content = user.name + '(' + user.account + ')' + '负责今天(' + getCurrentDate() + ')早会';
                    EmailUtil.sendEmail(eReceivers, u'主持早会', content.encode("utf-8"))
                except Exception as e:
                    self._logger.error("邮件失败，" + str(e))
                try:
                    msg = "【主持早会】" + user.name + '(' + user.account + ')' + '负责今天(' + getCurrentDate() + ')早会';
                    SMSUtil.sendSMS(tReceivers, msg.encode("utf-8"))
                except Exception as e:
                    self._logger.error("短信失败，" + str(e))
        except Exception as e:
            print(e)
        self.userQueue.enQueue(user)

    def setSchdeule(self, job):
        # schedule.every().day.at("7:00").do(job)
        schedule.every(3).seconds.do(job)

    def scheduleCheck(self):
        schedule.run_pending()
