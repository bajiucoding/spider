#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-08 20:43:47
# @Author  : gongyi

#数据存储器
import codecs
import time

class DataClass():
    def __init__(self):
        self.filepath = 'baike_%s.html'%(time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime()))
        self.outputHead(self.filepath)
        self.datas = []

    def store_data(self,data):
        if not data:
            return
        self.datas.append(data)
        if len(self.datas)>10:
            self.outputHTML(self.filepath)

    def outputHead(self,path):
        '''
        将HTML头写进去
        '''
        fout = codecs.open(path,'w',encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')
        fout.close()


    def outputHTML(self,path):
        '''将数据写入HTML文件中'''
        fout = codecs.open(path,'a',encoding='utf-8')
        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%s</td>'%data['url'])
            fout.write('<td>%s</td>'%data['title'])
            fout.write('<td>%s</td>'%data['summary'])
            fout.write('<tr>')
            self.datas.remove(data)
        fout.close()

    def outputEnd(self,path):
        '''
        输出HTML结尾标志'''
        fout = codecs.open(path,'a',encoding='utf-8')
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()
