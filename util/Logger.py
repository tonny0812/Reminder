# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Reminder
   Description :
   Author :       guodongqing
   date：          2019/11/12
-------------------------------------------------
"""
import Config
import logging
from logging import handlers

level_relations = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'crit': logging.CRITICAL
}  # 日志级别关系映射

FMT = '%(asctime)s - %(levelname)s: %(message)s'


class Logger():

    def __init__(self):
        self.logger = logging.getLogger(Config.LOG_FILE_PATH)
        format_str = logging.Formatter(FMT)  # 设置日志格式
        self.logger.setLevel(level_relations.get(Config.LOG_LEVEL))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        # 实例化TimedRotatingFileHandler
        th = handlers.TimedRotatingFileHandler(filename=Config.LOG_FILE_PATH,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)

    def debug(self, msg):
        if msg:
            self.logger.debug(msg.encode('utf-8'))

    def warning(self, msg):
        if msg:
            self.logger.warning(msg.encode('utf-8'))
        else:
            pass

    def info(self, msg):
        if msg:
            self.logger.info(msg.encode('utf-8'))
        else:
            pass

    def error(self, msg):
        if msg:
            self.logger.error(msg.encode('utf-8'))
        else:
            pass

    def critical(self, msg):
        if msg:
            self.logger.critical(msg.encode('utf-8'))
        else:
            pass


if __name__ == '__main__':
    logger = Logger()
    logger.debug('debug')
    logger.info('info')
    logger.warning('警告')
    logger.error('报错')
    logger.critical('严重')
