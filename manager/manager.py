# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     manager
   Description :
   Author :       guodongqing
   date：          2019/11/11
-------------------------------------------------
"""
import time
from multiprocessing import Process

from db.sqlitecli import SqliteUserDB
from service.MeetingReminder import MeetingReminder
from service.Queue import Queue


class Manager(object):
    __meetingReminderProcess = None
    __meetringReminderFlag = True
    __userdb = SqliteUserDB()

    def startMeetingReminder(self, account):
        _firstUser = self.__userdb.query_meetinguser_by_account(account)[0]
        if _firstUser is None:
            return False, "用户%s不存在！" % account
        if _firstUser.isValid == 0:
            return False, "用户%s不可用！" % account

        _meetingUsers = self.__userdb.get_meetinguser_all_valid()
        _meetingUsers = self.__rSortUsers(_firstUser, _meetingUsers)
        _meetinUserQueue = self.__getUserQueue(_meetingUsers)
        if self.__meetingReminderProcess is None:
            self.__meetingReminderProcess = Process(target=self.__startMeetingReminderServer, args=(_meetinUserQueue,))
            return True, "Meeting Reminder Start"
        else:
            return False, "Meeting Reminder is running"

    def __startMeetingReminderServer(self, meetinUserQueue):
        meetingReminder = MeetingReminder(meetinUserQueue)
        meetingReminder.setSchdeule(meetingReminder.job)
        self.__meetringReminderFlag = True
        while self.__meetringReminderFlag:
            meetingReminder.scheduleCheck()
            print('##')
            time.sleep(1)

    def stopMeetringReminder(self):
        if self.__meetingReminderProcess and self.__meetingReminderProcess.is_alive():
            print('stop meeting reminder processs!')
            self.__meetringReminderFlag = False
            self.__meetingReminderProcess.terminate()
            self.__meetingReminderProcess.join(10)
            return True, "Meeting Reminder is stopped"
        else:
            return False, "Meeting Reminder has stopped"

    def getAllMeetingUsers(self):
        return self.__userdb.get_meetinguser_all()

    def __rSortUsers(self, firstOrderUser, users):
        firstOrder = firstOrderUser.order
        size = len(users)
        for user in users:
            _order = ((user.order - firstOrder) + size) % size
            user.order = _order + 1;
        users.sort(cmp=None, key=lambda x: x.order, reverse=False)
        return users

    def __getUserQueue(self, meetingUsers):
        queue = Queue(len(meetingUsers) + 1);
        for user in meetingUsers:
            queue.enQueue(user);
        return queue


if __name__ == '__main__':
    sysManager = Manager()
    sysManager.startMeetingReminder('yangfan05')
