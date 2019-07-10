#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-08 16:47:05
# @Author  : gongyi
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from log import logger

logger = logger('AnalysisHTML')
class AnalysisHTML():
    #HTML解析

    def parser(self,page_url,html):
        #解析网页内容，提取url和数据
        logger.info('开始调用parser方法，提取url和数据'+page_url)
        if not page_url or not html:
            logger.info('parser方法缺少参数'+str(page_url)+str(html))
            return None
        soup = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
        # print(soup)
        new_urls = self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url,soup)
        logger.info('调用parser方法成功，提取到了url：'+str(len(new_urls)))
        return new_urls,new_data

    def _get_new_urls(self,page_url,soup):
        '''
        提取新的url集合
        ：param page_url:下载页面的url
        :param soup:soup
        '''
        logger.info('_get_new_urls方法开始执行，即将获取新的url'+page_url)
        new_urls = set()
        links = soup.find_all('a',href=re.compile(r'/item/[a-zA-Z0-9\%]+/\d+'))
        logger.info(str(len(links)))
        for link in links:
            #提取href属性
            new_href = link['href']
            logger.info("得到的新href："+new_href)
            #拼接成完整网址
            new_url = urljoin(page_url,new_href)
            logger.info("得到的新url地址："+new_url)
            new_urls.add(new_url)
        logger.info('获取新url成功，即将返回'+str(len(new_urls)))
        return new_urls

    def _get_new_data(self,page_url,soup):
        '''
        提取有效数据
        :param page_url:下载页面的url
        :param soup:
        :return :返回有效数据
        '''
        logger.info('_get_new_data方法开始执行，即将获取新的data')
        data = {}
        data['url'] = page_url
        title = soup.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title.get_text()
        summary = soup.find('div',class_='lemma-summary')
        data['summary'] = summary.get_text()
        logger.info('获取新url成功，即将返回'+str(len(data)))
        return data
