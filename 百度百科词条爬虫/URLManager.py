#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-08 16:18:19
# @Author  : gongyi

#url管理器
import requests
import pickle
import hashlib

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
        m = hashlib.md5()
        m.update(url.encode())
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            print(url)
            self.new_urls.add(url)

    def add_new_urls(self,urls):
        '''添加url列表'''
        if len(urls)==0:
            return None
        for url in urls:
            self.add_new_url(url)

    def get_new_url(self):
        '''
        获取一个未爬取的url
        '''
        new_url = self.new_urls.pop()
        #此时要对已爬取过的url做md5处理，减少url长度，便于存储
        m = hashlib.md5()
        m.update(new_url.encode())
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url

    def new_url_size(self):
        '''
        获取未爬取url集合的大小
        '''
        return len(self.new_urls)

    def old_url_size(self):
        #获取已爬取url集合的大小
        return len(self.old_urls)


    def store(self,path,data):
        '''
        保存url的爬取进度
        :in param path:文件路径
        :in param data:待存储数据，这里是url集合
        '''
        with open(path,'ab') as f:
            pickle.dump(data,f)

    def load(self,path):
        '''
        从文件中加载进度
        :in param path:文件路径
        :return:返回set集合
        '''
        print('[+]从文件加载进度：%s'%path)
        try:
            with open(path,'rb') as f:
                data = pickle.load(f)
                return data
        except:
            print('[!]无进度文件，请检查%s'%path)
        return set()
