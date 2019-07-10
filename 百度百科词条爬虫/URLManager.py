#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-08 16:18:19
# @Author  : gongyi

#url管理器
import requests

class URLManager():

    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        '''
        判断是否有待爬取的url
        '''
        return self.new_url_size()!=0

    def add_new_url(self,url):
        '''
        添加新的url到未爬取集合中
        '''
        if not url:
            return None
        if url not in self.new_urls and url not in self.old_urls:
            print(url)
            self.new_urls.add(url)

    def add_new_urls(self,urls):
        '''添加url列表'''
        if len(urls)==0:
            return None
        for url in urls:
            if url not in self.new_urls and url not in self.old_urls:
                self.new_urls.add(url)

    def get_new_url(self):
        '''
        获取一个未爬取的url
        '''
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def new_url_size(self):
        '''
        获取未爬取url集合的大小
        '''
        return len(self.new_urls)

    def old_url_size(self):
        #获取已爬取url集合的大小
        return len(self.old_urls)

