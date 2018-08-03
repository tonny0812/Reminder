#encoding:utf-8
'''
Created on 2018年8月1日

@author: guodongqing
'''
import time
from config.UserInfo import MISUsers, MeetingUsers
from service.MISReminder import MISReminder
from service.MeetingReminder import MeetingReminder
from service.Queue import Queue

def sortMISUser(firstOrder):
    size = len(MISUsers);
    for user in MISUsers:
        order = ((user['order'] - firstOrder) + size) % size; 
        user['neworder'] = order + 1;
    MISUsers.sort(cmp=None, key=lambda x:x['neworder'], reverse=False)

def sortMeetingUser(firstOrder):
    size = len(MeetingUsers);
    for user in MeetingUsers:
        order = ((user['order'] - firstOrder) + size) % size; 
        user['neworder'] = order + 1;
    MeetingUsers.sort(cmp=None, key=lambda x:x['neworder'], reverse=False)

if __name__ == '__main__':
    sortMISUser(3)
    misUserQueue = Queue(len(MISUsers)+1);
    for user in MISUsers:
        misUserQueue.enQueue(user);
    sortMeetingUser(5)
    meetinUserQueue = Queue(len(MeetingUsers)+1);
    for user in MeetingUsers:
        meetinUserQueue.enQueue(user);    
    
    misReminder = MISReminder(misUserQueue);
    meetingReminder = MeetingReminder(meetinUserQueue);
    misReminder.setSchdeule(misReminder.job);
    meetingReminder.setSchdeule(meetingReminder.job)    
    while True:
        misReminder.scheduleCheck();
        meetingReminder.scheduleCheck();
        time.sleep(1)