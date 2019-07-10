#coding=utf-8
'''
*************************
file:       allproject HTMLAnalysis
author:     gongyi
date:       2019/7/9 21:20
****************************
change activity:
            2019/7/9 21:20
'''
#HTML文本解析类
from bs4 import BeautifulSoup
from abc import ABCMeta,abstractmethod
from urllib.parse import urljoin
import re

from log import Bosslogger

logger = Bosslogger('HTMLAnalysis')
class HTMLAnalysis(metaclass=ABCMeta):
    #HTML文本解析类，不同HTML对应不同的解析方法

    @abstractmethod
    def parse(self,url,html):
        pass

    @abstractmethod
    def getNewUrl(self,url,soup):
        pass

    @abstractmethod
    def getNewData(self,url,soup):
        pass

class JobHTMLAnalysis(HTMLAnalysis):
    '''
    boss直聘职位列表页面html的解析
    '''

    def parse(self,url,html):
        '''
        重写虚类的parse方法，解析html
        :param url: 当前页面的url
        :param html: 当前页面得到的text即html文件
        :return:
        '''
        if not url or not html:
            logger.info('传入参数不完整')
            return None
        logger.info('开始解析职位列表页面')
        soup = BeautifulSoup(html,'html.parser')
        new_url = self.getNewUrl(url,soup)
        new_data = self.getNewData(url,soup)
        logger.info('解析职位列表页面html成功')
        return new_url,new_data

    def getNewUrl(self,url,soup):
        '''
        职位页面获取新url
        :param url:
        :param soup:
        :return: 详情url
        '''
        logger.info('开始从职位列表页面解析新的url，即职位详情')
        new_urls = set()
        jobs = soup.find_all('div','job-primary')
        hrefs = []
        for job in jobs:
            href = job.find('div','info-primary').find('a')['href']
            new_url = urljoin(url,href)
            logger.info('解析到新的详情界面url'+new_url)
            new_urls.add(new_url)
        logger.info('getNewURL方法执行完毕')
        return new_urls

    def getNewData(self,url,soup):
        '''
        职位页面获取职位相关数据
        :param url:
        :param soup:
        :return:
        '''
        result = []
        jobs = soup.find_all('div','job-primary')
        for job in jobs:
            result.append(job.find('div','job-title').string)     #获取职位名
            result.append(job.find('span', 'red').string)          #获取工资
            result.append(job.find('div', 'company-text').find('a').string)   #获取公司名称
            # 获取公司地址、经验、学历要求。在一个p标签内还有e标签，先找到p标签，再找到其子标签
            response1 = job.find('div', 'info-primary').find('p').contents
            result.append(response1[0])                         #获取工作地点
            result.append(response1[2])                         #获取工作经验要求
            result.append(response1[4])                         #获取学历要求

            # 获取公司行业、规模、融资情况
            response2 = job.find('div', 'company-text').find('p').contents
            result.append(response2[0])                         #获取公司行业
            if len(response2) < 5:
                result.append('无融资信息')                         #公司融资情况
                result.append(response2[2])                             #公司规模
            else:
                result.append(response2[2])
                result.append(response2[4])
        print(result)
        return result
class DetailHTMLAnalysis(HTMLAnalysis):
    '''
    职位详情界面HTML解析
    '''

    def parse(self,url,html):
        if not url or not html:
            logger.info('传入参数不完整')
            return None
        logger.info('开始解析职位详情页面')
        soup = BeautifulSoup(html,'html.parser')
        new_url = self.getNewUrl(url,soup)
        new_data = self.getNewData(url,soup)
        logger.info('解析职位详情页面html成功')
        return new_url,new_data

    def getNewUrl(self,url,soup):
        return None

    def getNewData(self,url,soup):
        '''
        职位详情页面解析。目前就解析出工作年限和全部的工作要求
        :param url:
        :param soup:
        :return:
        '''
        result = []
        detail = soup.find('div', 'detail-content').find('div', 'text').contents
        for i in range(len(detail)):
            if i % 2 != 0:
                continue
            if '年' in detail[i].strip():
                if re.match(r'[1-9]', detail[i].strip()) and '经验' in detail[i].strip():
                    result.append(detail[i].strip())
        return result