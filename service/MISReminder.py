# encoding:utf-8
'''
Created on 2018年8月1日

@author: guodongqing
'''
import datetime
import threading

import schedule
from util import EmailUtil, SMSUtil
from util.DateUtil import isWorkDay, getCurrentDate
from util.Logger import Logger
from service import email_content


class MISReminder():
    _logger = Logger.instance()

    def __init__(self, queue):
        self.userQueue = queue
        self._lock = threading.Lock()

    def job(self):
        if isWorkDay(getCurrentDate()):
            with self._lock:
                user = self.userQueue.getHead();
                self.sendMessage(user);
        else:
            today = datetime.now().weekday();
            if today == 6:
                with self._lock:
                    user = self.userQueue.deQueue();
                    self.userQueue.enQueue(user);
            self._logger.info(getCurrentDate() + '是假日！');

    def sendMessage(self, user):
        _r = '--------order:%s---%s(%s)负责巡检------------' % (str(user.order), user.name, user.account,)
        self._logger.info(_r)
        eReceivers = [];
        tReceivers = [];

        if user:
            _r2 = '--------email:%s---tel:%s------------' % (str(user.email), user.tel)
            self._logger.info(_r2)
            eReceivers.append(user.email);
            eReceivers.append('lijian02@58.com')
            tReceivers.append(user.tel);
            try:
                content = user.name + '(' + user.account + ')' + '负责巡检，访问地址：<a href="http://union.vip.58.com/bsp/index">http://union.vip.58.com/bsp/index</a>,并查看《HBG业绩加和校验结果通知》邮件';
                content += '<br/>'
                content += email_content
                EmailUtil.sendEmail(eReceivers, '巡检轮班', content.encode("utf-8"))
            except Exception as e:
                self._logger.error("邮件失败，" + str(e))
            try:
                msg = "【巡检轮班】" + user.name + '(' + user.account + ')' + '负责这周巡检,并查看《HBG业绩加和校验结果通知》邮件'
                SMSUtil.sendSMS(tReceivers, msg.encode("utf-8"))
            except Exception as e:
                self._logger.error("短信失败，" + str(e))
                pass



    def setSchdeule(self, job):
        schedule.every().day.at("10:00").do(job)
        schedule.every().day.at("14:00").do(job)
        # schedule.every(5).seconds.do(job)

    def scheduleCheck(self):
        schedule.run_pending();
