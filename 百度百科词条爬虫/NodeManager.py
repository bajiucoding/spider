#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-10 15:45:10
# @Author  : gongyi
from log import logger
import time
from multiprocessing.managers import BaseManager
from multiprocessing import Process,Queue
# from queue import Queue
from URLManager import URLManager
from DataClass import DataClass
logger = logger('Process')

class NodeManager(BaseManager):
    def startManager(self,url_q,result_q):
        '''
        创建一个分布式管理器
        ：param url_q:url队列
        :param result_1:结果队列
        :return:
        '''
        #把创建的两个队列注册在网络上，利用register方法，callable参数关联了queue
        #将queue对象在网络上暴露
        BaseManager.register('get_task_queue',callable=lambda:url_q)
        BaseManager.register('get_result_queue',callable=lambda:result_q)

        #绑定端口8001，设置验证口令'baike'。相当于对象初始化
        manager = BaseManager(address=('',8001),authkey='baike'.encode('utf-8'))
        #返回manager对象
        return manager

    def url_manager_proc(self,url_q,conn_q,root_url):
        '''
        URL管理进程：将从conn_q队列获取到的新url提交给url管理器，去重之后，取出url放入url_queue队列中传递给爬虫节点
        '''
        #初始化url管理器
        url_manager = URLManager()
        #将根节点加入待爬取列表
        url_manager.add_new_url(root_url)

        while True:
            while(url_manager.has_new_url()):
                #当有待爬取链接时，获取url并通过url_q队列发送给爬虫节点
                new_url = url_manager.get_new_url()
                url_q.put(new_url)
                logger.info('添加url成功，并将新url加入队列url_q中，传给爬虫节点。目前已爬取'+str(url_manager.old_url_size()))#+'url_q长度是：'+str(len(url_q)))

                #加一个判断，当爬取够2000条链接时，就关闭并保存进度
                if(url_manager.old_url_size()>100):
                    #通过队列传递停止消息
                    url_q.put('end')
                    logger.info('结束爬取通知已发出')
                    #关闭管理节点，同时保存进度
                    url_manager.store('new_urls.txt',url_manager.new_urls)
                    url_manager.store('old_urls.txt',url_manager.old_urls)
                    return None

            #将爬虫节点中html解析出的url交给url管理器
            try:
                if not conn_q.empty():
                    #数据提取进程存放新url的队列不为空，就取url
                    logger.info('从conn队列中提取url加入待爬取url集合')
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except BaseException as e:
                #没取到新url，说明这里暂时没解析出来，等0.1s
                logger.info('暂时没有新的url，等等再说')
                time.sleep(0.1)

    def result_solve_proc(self,result_q,conn_q,store_q):
        '''
        数据提取进程，将爬虫传回来的数据(result_q中)解析，url交给url管理器，数据交给数据存储器，
        :param result_q:爬虫返回的数据存储队列
        :param store_1:队列，存储着解析得到的数据
        return:
        '''
        # logger.info(str('resulr_q的长度是：'+str(len(result_q))))
        # logger.info(str('conn_q的长度是：'+str(len(conn_q))))
        # logger.info(str('store_q的长度是：'+str(len(store_q))))
        while(True):
            try:
                if not result_q.empty():
                    #结果队列不为空，就说明有结果返回
                    logger.info('开始解析结果')
                    content = result_q.get(True)
                    if content['new_urls'] == 'end':
                        logger.info('结果分析进程接收通知然后结束')
                        store_q.put('end')
                        return None
                    logger.info('开始将url和数据分别提交给url管理器和数据存储进程')
                    conn_q.put(content['new_urls'])   #将url提交给url管理器
                    store_q.put(content['data'])      #将数据放入数据存储队列中
                else:
                    #还没结束，稍等一段时间
                    time.sleep(0.1)
            except BaseException as e:
                logger.info('提取结果的时候异常了'+str(e))
                time.sleep(0.1)      #延时休息

    def store_proc(self,store_q):
        '''
        数据存储进程，从store_q中读取数据，调用数据存储器进程存储
        '''
        output = DataClass()
        while True:
            if not store_q.empty():
                #数据队列非空
                data = store_q.get()
                if data == 'end':
                    logger.info('数据存储进程收到结束通知，即将结束')
                    output.outputEnd(output.filepath)
                    return None
                output.store_data(data)
            else:
                time.sleep(1)


if __name__ == '__main__':
    logger.info('初始化队列启动进程')
    #启动分布式管理器和三个进程，并初始化四个队列
    url_q = Queue()
    result_q = Queue()
    store_q = Queue()
    conn_q = Queue()

    root_url = 'https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB'

    #创建分布式管理器
    node = NodeManager()
    manager = node.startManager(url_q,result_q)
    #创建url管理进程，数据提取进程和数据存储进程
    # url_manager_proc = Process(target=node.url_manager_proc, args=(node.return_queue(url_q), node.return_queue(conn_q), node.return_queue(root_url),))
    # result_solve_proc = Process(target=node.result_solve_proc, args=(node.return_queue(result_q), node.return_queue(conn_q), node.return_queue(store_q),))
    # store_proc = Process(target=node.store_proc, args=(node.return_queue(store_q),))
    url_manager_proc = Process(target=node.url_manager_proc,args=(url_q,conn_q,root_url,))
    result_solve_proc = Process(target=node.result_solve_proc,args=(result_q,conn_q,store_q,))
    store_proc = Process(target=node.store_proc,args=(store_q,))

    #启动这三个进程
    logger.info('三个进程启动了')
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()
