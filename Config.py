# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Config
   Description :
   Author :       guodongqing
   date：          2019/11/12
-------------------------------------------------
"""
import os

BASE_PATH = os.path.dirname(__file__) + "\\"

LOG_DIR_PATH = BASE_PATH + "\\log\\"
LOG_FILE_PATH = LOG_DIR_PATH + "remind.log"

# 'debug','info','warning','error','crit'
LOG_LEVEL = 'info'
LOGGER_NAME = 'reminderLogger'
FMT = '%(asctime)s - %(levelname)s: %(message)s'

