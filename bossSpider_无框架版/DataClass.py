#coding=utf-8
'''
*************************
file:       allproject DataClass
author:     gongyi
date:       2019/7/9 21:20
****************************
change activity:
            2019/7/9 21:20
'''
import xlwt,codecs,csv
from log import Bosslogger

logger = Bosslogger('DataClass')

class DataClass():

    def WriteTxt(self,data):
        '''
        将列表写入txt文本文件中
        :param data: 列表
        :return:
        '''
        logger.info('准备将数据写入txt文件中')
        with open('result.txt', 'a', encoding='utf-8') as f:
            f.write(str(data)+'\n')

    def WriteCSV(self,data):
        '''
        将列表写入csv文件。
        :param data:待写入列表，这里假设列表中只有一个元素。如果是datas，需要在方法内部遍历
        :return:
        '''
        logger.info('准备将数据写入csv文件中')
        file_csv = codecs.open('result.csv', 'w+', 'utf-8')
        writer = csv.writer(file_csv, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data)
        print('保存成功')


    def WriteEXCEL(self,data, i):
        '''
        将列表写入excel中
        :param data:
        :return:
        '''
        logger.info('准备将数据写入excel文件中')
        f = xlwt.Workbook()
        sheet1 = f.add_sheet(u'job_detail.xls', cell_overwrite_ok=True)  # 创建sheet

        # 写入数据
        for j in range(len(data)):
            sheet1.write(i, j, data[j])

        f.save('job_detail.xls')