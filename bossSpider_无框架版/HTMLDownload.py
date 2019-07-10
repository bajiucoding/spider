#coding=utf-8
'''
*************************
file:       allproject HTMLDownload
author:     gongyi
date:       2019/7/9 21:20
****************************
change activity:
            2019/7/9 21:20
'''
#根据url下载html页面
import requests,chardet
from log import Bosslogger

logger = Bosslogger('HTMLDownload')
class HTMLDownload():
    '''
    html页面下载类
    '''

    def download(self,url):
        '''
        根据url下载html页面
        :param url: 待爬取url
        :return: 下载的html页面
        '''
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        headers = {'User-Agent':user_agent}
        res = requests.get(url,headers=headers)
        if res.status_code==200:
            logger.info('下载html成功，对应url：'+url)
            res.encoding = chardet.detect(res.content)
            return res.text
        logger.info('下载url失败,url是'+url)
        return None

