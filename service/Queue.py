# encoding:utf-8
'''
Created on 2018年8月1日

@author: guodongqing
'''

import threading

class Queue():

    def __init__(self, capacity):
        self.queue = [None] * capacity
        self.capacity = capacity
        self.front = 0
        self.rear = 0
        self._lock = threading.Lock()

    def enQueue(self, element):
        with self._lock:
            if self.full():
                print('队满')
                return
            self.queue[self.rear] = element
            self.rear = (self.rear + 1) % self.capacity

    def deQueue(self):
        with self._lock:
            if self.empty():
                print('队列是空的')
                return
            temp = self.queue[self.front]
            self.queue[self.front] = None
            self.front = (self.front + 1) % self.capacity
            return temp

    def full(self):
        return (self.rear + 1) % self.capacity == self.front

    def empty(self):
        return self.front == self.rear

    def fetchQueue(self):
        temp = self.front
        list = []
        while temp != self.rear:
            list.append(self.queue[temp])
            temp = (temp + 1) % self.capacity
        return list

    def clear(self):
        temp = self.front
        while temp != self.rear:
            self.queue[temp] = None
            temp = (temp + 1) % self.capacity
        self.rear = self.front

    def getHead(self):
        with self._lock:
            if self.empty():
                print('队空')
                return
            h = self.queue[self.front]
            return h

    def length(self):
        return (self.rear - self.front + self.capacity) % self.capacity
