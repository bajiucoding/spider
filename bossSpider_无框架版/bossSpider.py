#coding=utf-8
'''
*************************
file:       allproject bossSpider
author:     gongyi
date:       2019/7/9 21:20
****************************
change activity:
            2019/7/9 21:20
'''
#爬虫程序主体，调度各个模块
from URLManager import URLManager
from HTMLDownload import HTMLDownload
from HTMLAnalysis import JobHTMLAnalysis,DetailHTMLAnalysis
from DataClass import DataClass
from log import Bosslogger
import time

logger = Bosslogger('bossSpider')

class Spider():
    #爬虫管理调度器
    def __init__(self):
        '''
        初始化爬虫调度器
        '''
        self.URLManager = URLManager()
        self.HTMLDownload = HTMLDownload()
        self.JobHTMLAnalysis = JobHTMLAnalysis()
        self.DetailHTMLAnalysis = DetailHTMLAnalysis()
        self.DataClass = DataClass()

    def crawl(self,root_url):
        '''
        爬虫调度程序
        :param root_url:
        :return:
        '''
        #添加需要爬取的url即根url
        self.URLManager.addNewUrl(root_url)
        logger.info('添加根url成功，即将从根url开始爬取')

        while(self.URLManager.hasNewUrl()):
            logger.info('开始爬取了')
            #为了防止被封ip，每隔10s爬一个链接
            time.sleep(10)
            new_url = self.URLManager.getNewUrl()
            logger.info('即将开始下载'+new_url+'的内容')
            html = self.HTMLDownload.download(new_url)
            if 'job_detail' not in new_url:
                #不是详情页面
                new_urls,data = self.JobHTMLAnalysis.parse(new_url,html)
            else:
                #说明是详情页面
                new_urls,data = self.DetailHTMLAnalysis.parse(new_url,html)

            self.URLManager.addNewUrl(new_urls)
            self.DataClass.WriteTxt(data)
            logger.info('已经爬取了'+str(self.URLManager.oldUrlsSize())+'个链接')

if __name__=='__main__':
    spider = Spider()
    spider.crawl('https://www.zhipin.com/c101280600/?query=python&page=1&ka=page-1')