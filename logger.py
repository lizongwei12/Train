# -*- coding: utf-8 -*-
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from settings import CATEGORY_LOG
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_name = datetime.now().strftime('%Y-%m-%d')
def create_conf(backupCount,level):
    # price log configure
    root_logger = logging.getLogger()
    if len(root_logger.handlers)==0:
        root_logger.setLevel(logging.INFO)    # Log等级总开关
        category_path = '../log/%s-log-%s.txt' % (CATEGORY_LOG,file_name)
        category_handler = RotatingFileHandler(category_path, maxBytes=1024*1024*1024,backupCount=backupCount,mode='w')
        category_handler.setLevel(level)
        category_handler.setFormatter(formatter)
        root_logger.addHandler(category_handler)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        root_logger.addHandler(ch)
create_conf(10,logging.INFO)
# 日志等级   debug 、info 、warning 、error 、critical
