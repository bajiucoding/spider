#coding=utf-8
'''
*************************
file:       allproject URLManager
author:     gongyi
date:       2019/7/9 21:19
****************************
change activity:
            2019/7/9 21:19
'''
#URL管理器，管理爬虫需要爬取的url
from log import Bosslogger

logger = Bosslogger('URLManager')
class URLManager():
    '''
    url管理
    '''

    def __init__(self):
        '''
        初始化，带爬取url集合和已爬取url集合
        '''
        self.old_urls = set()
        self.new_urls = set()

    def addNewUrl(self,urls):
        '''
        添加待爬取url
        :param urls:单个url或者url列表/集合
        :return:
        '''
        logger.info('开始添加待爬取url')
        if type(urls)==set:
            for url in urls:
                if not self.existOldUrls(url):
                    self.new_urls.add(url)
        elif not urls:
            pass
        else:
            if not self.existOldUrls(urls):
                self.new_urls.add(urls)

    def addOldUrls(self,url):
        '''
        将已爬取url加入到已爬取url列表中
        :param url:
        :return:
        '''
        self.old_urls.add(url)

    def getNewUrl(self):
        '''
        获取一个待爬取链接
        :return:
        '''
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def oldUrlsSize(self):
        '''
        获取已爬取url数量
        :return:
        '''
        return len(self.old_urls)

    def hasNewUrl(self):
        '''
        判断是否还有待爬取链接
        :return:
        '''
        return len(self.new_urls) > 0

    def existOldUrls(self,url):
        '''
        判断url是否存在于已爬取url集合中
        :param url:
        :return:
        '''
        return url in self.old_urls

