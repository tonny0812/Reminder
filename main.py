#encoding:utf-8
'''
Created on 2018年8月1日

@author: guodongqing
'''
from util.Logger import Logger
import web

if __name__ == '__main__':
    Logger.instance().info("---------服务启动-----------")
    web.start_web_server()