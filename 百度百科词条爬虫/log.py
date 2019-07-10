#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-08 22:29:12
# @Author  : gongyi

import logging,pysnooper
# @pysnooper.snoop()
def logger(log_type):
    '''
    日志函数
    '''

    logLevel = logging.INFO
    #创建日志
    my_logger = logging.getLogger(log_type)
    my_logger.setLevel(logLevel)

    #创建日志输出
    ch = logging.StreamHandler()
    ch.setLevel(logLevel)

    # #创建文件句柄，设置级别
    # log_file = '%s/log/%s'%(setting.BASE_DIR,setting.LOG_TYPES[log_type])
    # fh  = logging.FileHandler(log_file)
    # fh.setLevel(setting.LOG_LEVEL)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch.setFormatter(formatter)

    my_logger.addHandler(ch)
    return my_logger
