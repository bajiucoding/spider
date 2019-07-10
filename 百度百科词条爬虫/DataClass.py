#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-08 20:43:47
# @Author  : gongyi

#数据存储器
import codecs

class DataClass():
    def __init__(self):
        self.datas = []

    def store_data(self,data):
        if not data:
            return
        self.datas.append(data)

    def outputHTML(self):
        fout = codecs.open('baike.html','w',encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')
        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%s</td>'%data['url'])
            fout.write('<td>%s</td>'%data['title'])
            fout.write('<td>%s</td>'%data['summary'])
            fout.write('<tr>')
            self.datas.remove(data)
        fout.write('</html>')
        fout.write('</body>')
        fout.write('</table>')
        fout.close()
