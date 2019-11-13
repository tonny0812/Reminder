# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Reminder
   Description :
   Author :       guodongqing
   date：          2019/11/12
-------------------------------------------------
"""
import multiprocessing
import sys
import threading
import traceback

import Config
import logging

level_relations = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'crit': logging.CRITICAL
}  # 日志级别关系映射


# ============================================================================
# Define Log Handler
# ============================================================================
class CustomLogHandler(logging.Handler):
    """multiprocessing log handler

    This handler makes it possible for several processes
    to log to the same file by using a queue.

    """

    def __init__(self, fname):
        logging.Handler.__init__(self)

        self._handler = logging.FileHandler(fname)
        self.queue = multiprocessing.Queue(-1)

        thrd = threading.Thread(target=self.receive)
        thrd.daemon = True
        thrd.start()

    def setFormatter(self, fmt):
        logging.Handler.setFormatter(self, fmt)
        self._handler.setFormatter(fmt)

    def receive(self):
        while True:
            try:
                record = self.queue.get()
                self._handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)

    def send(self, s):
        self.queue.put_nowait(s)

    def _format_record(self, record):
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            dummy = self.format(record)
            record.exc_info = None

        return record

    def emit(self, record):
        try:
            s = self._format_record(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        self._handler.close()
        logging.Handler.close(self)

class Logger():
    _instance_lock = threading.Lock()

    def __init__(self):
        self.logger = logging.getLogger(Config.LOGGER_NAME)
        format_str = logging.Formatter(Config.FMT)  # 设置日志格式
        self.logger.setLevel(level_relations.get(Config.LOG_LEVEL))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        custromHandler = CustomLogHandler(Config.LOG_FILE_PATH)
        custromHandler.setFormatter(format_str)
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(custromHandler)

    @classmethod
    def instance(cls, *args, **kwargs):
        with Logger._instance_lock:
            if not hasattr(Logger, "_instance"):
                Logger._instance = Logger(*args, **kwargs)
        return Logger._instance

    def debug(self, msg):
        if msg:
            try:
                msg = unicode(msg, 'utf-8')
            except Exception as e:
                msg.encode('utf-8')
            self.logger.debug(msg)

    def warning(self, msg):
        if msg:
            try:
                msg = unicode(msg, 'utf-8')
            except Exception as e:
                msg.encode('utf-8')
            self.logger.warning(msg)
        else:
            pass

    def info(self, msg):
        if msg:
            try:
                msg = unicode(msg, 'utf-8')
            except Exception as e:
                msg.encode('utf-8')
            self.logger.info(msg)
        else:
            pass

    def error(self, msg):
        if msg:
            try:
                msg = unicode(msg, 'utf-8')
            except Exception as e:
                msg.encode('utf-8')
            self.logger.error(msg)
        else:
            pass

    def critical(self, msg):
        if msg:
            try:
                msg = unicode(msg, 'utf-8')
            except Exception as e:
                msg.encode('utf-8')
            self.logger.critical(msg)
        else:
            pass


def _output(name):
    logger = Logger.instance()
    print(logger)
    logger.info('info_output' + name)
    logger.warning('警告_output' + name)
    logger.error(u'报错_output' + name)

def _output2(name):
    logger = Logger.instance()
    print(logger)
    logger.info('info_output' + name)
    logger.warning('警告_output' + name)
    logger.error(u'报错_output' + name)


if __name__ == '__main__':


    p1 = threading.Thread(target=_output, args=('p1',))
    p2 = threading.Thread(target=_output2, args=('p2',))

    p1.start()
    p2.start()

    logger = Logger.instance()
    print(logger)
    logger.info('info')
    logger.warning('警告%s' % 'test_ss')
    logger.error(u'报错%d' % 100)
    logger.critical(u'严重')
