#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-08 21:55:02
# @Author  : gongyi

from URLManager import URLManager
from GetHTML import GetHTML
from AnalysisHTML import AnalysisHTML
from DataClass import DataClass
from log import logger
import pysnooper

logger = logger('spider')

class Spider():
    #爬虫调度管理器
    def __init__(self):
        logger.info('爬虫开始执行了')
        self.manager = URLManager()
        self.downloader = GetHTML()
        self.parser = AnalysisHTML()
        self.DataClass = DataClass()

    # @pysnooper.snoop()
    def crawl(self,root_url):
        #添加初始入口url
        self.manager.add_new_url(root_url)
        logger.info('已经添加了根url：'+root_url)
        #
        while(self.manager.has_new_url() and self.manager.old_url_size()<100):
            logger.info('爬取根url')
            new_url = self.manager.get_new_url()
            html = self.downloader.download(new_url)
            new_urls,data = self.parser.parser(new_url,html)
            self.manager.add_new_urls(new_urls)
            self.DataClass.store_data(data)
            print('已经抓取了%d个链接'%self.manager.old_url_size())
            # try:
            #     logger.info('爬取根url')
            #     new_url = self.manager.get_new_url()
            #     html = self.downloader.download(new_url)
            #     new_urls,data = self.parser.parser(new_url,html)
            #     self.manager.add_new_url(new_urls)
            #     self.DataClass.store_data(data)
            #     print('已经抓取了%d个链接'%self.manager.old_url_size())
            # except Exception as e:
            #     print('抓取失败',e)
        self.DataClass.outputHTML()

if __name__=='__main__':
    spider = Spider()
    spider.crawl('https://baike.baidu.com/item/网络爬虫')
