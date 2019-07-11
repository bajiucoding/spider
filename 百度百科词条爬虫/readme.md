分布式爬虫：
主机：  URL管理器：URLManager
	   数据存储器：DataClass
	   控制调度器：SpiderManager 	  																   产生并启动三个进程：
	   		URL管理进程：负责url的管理和将新url传递给爬虫节点
	   		数据提取进程：解析爬虫节点返回的数据，将url交给url管理进程。将data交给数据存储进程
	   		数据存储进程：存储数据提取进程交过来的数据。维护队列保持进程间的通信
爬虫节点：爬虫调度器：
		 HTML下载器：
		 HTML解析器：

	   url_q: url管理进程将url传递给爬虫节点
	   result_q: 爬虫节点将数据返回给数据提取进程
	   conn_q: 数据提取进程将新的url数据提交给url管理进程
	   store_q: 数据提取进程将新获取的数据提交给数据存储进程