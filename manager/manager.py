# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     manager
   Description :
   Author :       guodongqing
   date：          2019/11/11
-------------------------------------------------
"""
import sys
import threading
import time

from db.sqlitecli import SqliteUserDB
from service.MISReminder import MISReminder
from service.MeetingReminder import MeetingReminder
from service.Queue import Queue
from util.Logger import Logger

reload(sys)
sys.setdefaultencoding('utf-8')


class Manager(object):
    __meetingReminderThread = None
    __meetingReminderFlag = True
    __misReminderThread = None
    __misReminderFlag = True
    __userdb = SqliteUserDB()
    _logger = Logger.instance()
    _meetingUserQueue = None

    def startMeetingReminder(self, account):
        _firstUser = self.__userdb.query_meetinguser_by_account(account)[0]
        if _firstUser is None:
            return False, u"用户%s不存在！" % account
        if _firstUser.isValid == 0:
            return False, u"用户%s不可用！" % account

        _meetingUsers = self.__userdb.get_meetinguser_all_valid()
        _meetingUsers = self.__rSortUsers(_firstUser, _meetingUsers)
        self._meetingUserQueue = self.__getUserQueue(_meetingUsers)
        if self.__meetingReminderThread is None or self.__meetingReminderThread.is_alive() == False:
            self.__meetingReminderThread = None
            self.__meetingReminderThread = threading.Thread(name="meeting-thread",
                                                            target=self._startMeetingReminderServer,
                                                            args=(self._meetingUserQueue,))
            self.__meetingReminderThread.start()
            return True, u"Meeting Reminder Start"
        else:
            return False, u"Meeting Reminder is running"

    def startMisReminder(self, account):
        _firstUser = self.__userdb.query_misuser_by_account(account)[0]
        if _firstUser is None:
            return False, u"用户%s不存在！" % account
        if _firstUser.isValid == 0:
            return False, u"用户%s不可用！" % account

        _misUsers = self.__userdb.get_misuser_all_valid()
        _misUsers = self.__rSortUsers(_firstUser, _misUsers)
        _misUserQueue = self.__getUserQueue(_misUsers)
        if self.__misReminderThread is None or self.__misReminderThread.is_alive() == False:
            self.__misReminderThread = None
            self.__misReminderThread = threading.Thread(name="mis-thread", target=self._startMisReminderServer, args=(_misUserQueue,))
            self.__misReminderThread.start()
            return True, u"Mis Reminder Start"
        else:
            return False, u"Mis Reminder is running"

    def _startMeetingReminderServer(self, meetinUserQueue):
        self._logger.info("开始Meeting通知...")
        meetingReminder = MeetingReminder(meetinUserQueue)
        meetingReminder.setSchdeule(meetingReminder.job)
        self.__meetingReminderFlag = True
        while self.__meetingReminderFlag:
            meetingReminder.scheduleCheck()
            time.sleep(1)
        self._logger.info("Meeting通知结束...")
        return

    def _startMisReminderServer(self, misUserQueue):
        self._logger.info("开始Mis通知...")
        misReminder = MISReminder(misUserQueue)
        misReminder.setSchdeule(misReminder.job)
        self.__misReminderFlag = True
        while self.__misReminderFlag:
            misReminder.scheduleCheck()
            time.sleep(1)
        self._logger.info("Mis通知结束...")
        return

    def stopMeetingReminder(self):
        if self.__meetingReminderThread and self.__meetingReminderThread.is_alive():
            self._logger.info("停止Meeting通知...")
            self.__meetingReminderFlag = False
            return True, u"Meeting Reminder is stopped"
        else:
            return False, u"Meeting Reminder has stopped"

    def stopMisReminder(self):
        if self.__misReminderThread and self.__misReminderThread.is_alive():
            self._logger.info("停止Mis通知...")
            self.__misReminderFlag = False
            return True, u"Mis Reminder is stopped"
        else:
            return False, u"Mis Reminder has stopped"

    def getAllMeetingUsers(self):
        return self.__userdb.get_meetinguser_all()

    def getAllMisUsers(self):
        return self.__userdb.get_misuser_all()

    def getAllActiveMeetingUsers(self):
        return self.__userdb.get_meetinguser_all_valid()

    def getAllActiveMisUsers(self):
        return self.__userdb.get_misuser_all_valid()

    def updateMeetingUsers(self, accout, active=True):
        print(accout, active, (1 if active == True else 0))
        if accout:
            _user = self.__userdb.query_meetinguser_by_account(accout)[0]
            if _user:
                _user.isValid = (1 if active == True else 0)
                self.__userdb.update_meetinguser(_user)
        else:
            print("更新失败！")

    def updateMisUsers(self, accout, active=True):
        print(accout, active, (1 if active == True else 0))
        if accout:
            _user = self.__userdb.query_misuser_by_account(accout)[0]
            if _user:
                _user.isValid = (1 if active == True else 0)
                self.__userdb.update_misuser(_user)
        else:
            print("更新失败！")

    @classmethod
    def __rSortUsers(self, firstOrderUser, users):
        firstOrder = firstOrderUser.order
        size = len(users)
        for user in users:
            _order = ((user.order - firstOrder) + size) % size
            user.order = _order + 1;
        users.sort(cmp=None, key=lambda x: x.order, reverse=False)
        return users

    @classmethod
    def __getUserQueue(self, users):
        _queue = Queue(len(users) + 1);
        for user in users:
            _queue.enQueue(user);
        return _queue


if __name__ == '__main__':
    sysManager = Manager()
    sysManager.startMeetingReminder('guodongqing')
    sysManager.startMisReminder('guodongqing')
