#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-08 16:43:26
# @Author  : gongyi
import requests
class GetHTML():
    #HTML下载器
    def download(self,url):
        #下载对应的HTML
        if not url:
            return None
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        headers = {'User-Agent':user_agent}
        r = requests.get(url,headers=headers)
        if r.status_code==200:
            r.encoding='utf-8'
            return r.text
        return '下载失败%s'%r.status_code
