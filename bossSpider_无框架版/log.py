#coding=utf-8
'''
*************************
file:       allproject log
author:     gongyi
date:       2019/7/9 21:55
****************************
change activity:
            2019/7/9 21:55
'''
#日志模块
import logging

def Bosslogger(log_type):

    #设定输出日志级别
    LOGLEVEL = logging.INFO

    #创建日志
    my_logger = logging.getLogger(log_type)
    my_logger.setLevel(LOGLEVEL)

    #创建终端输出日志
    ch = logging.StreamHandler()
    ch.setLevel(LOGLEVEL)

    #创建文件日志句柄
    log_file = 'BossSpider.log'
    fh = logging.FileHandler(log_file)
    fh.setLevel(LOGLEVEL)

    #设定日志格式
    formatter = logging.Formatter('%(asctime)s[%(name)s:%(lineno)d][%(module)s:%(funcName)s][%(levelname)s-%(message)s]')

    #应用日志格式
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    my_logger.addHandler(ch)
    my_logger.addHandler(fh)

    return my_logger