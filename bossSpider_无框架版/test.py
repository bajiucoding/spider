#coding=utf-8
'''
*************************
file:       bossSpider_无框架版 test
author:     gongyi
date:       2019/7/10 10:32
****************************
change activity:
            2019/7/10 10:32
'''
import requests,re
from bs4 import BeautifulSoup
import time

def getContent():
    time.sleep(5)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    headers = {'User-Agent': user_agent}
    url = 'https://www.zhipin.com/job_detail/b61f9c03ed52275b1HBz3NS7FVI~.html'
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    job = soup.find('div','detail-op').find('a')['ka']
    jobId = re.search(r'\d+',job).group(0)
    details = soup.find('div', 'detail-content').find('div', 'text').contents
# logger.info('获取了职位详情数据**'+str(len(details))+'***'+jobId)
    assert details is not None, "未获取到职位详情数据"
    with open('details.txt','w') as f:
        f.write(''.join(details).encode('utf-8'))
    return details

getContent()
def ana():
    with open('details.txt','r') as f:
        details = f.read()

    for i in range(len(details)):
        if i % 2 != 0:
            continue
        if '年' in details[i].strip():
            if re.match(r'[1-9]', details[i].strip()) and '经验' in details[i].strip():
                print(details[i].strip())
    print(type(details))
    for i in details:
        if type(i) is not 'bs4.element.Tag' and len(i)!=0:
            print('正确',type(i),i)
            # print('最终结果'.join(i))
    # try:
    #     detail = ''.join(i.strip() for i in details if type(i) is not 'bs4.element.Tag' and i.strip())
    # except Exception as e:
    #     print(details)
    # print(detail)
    # detail = ''.join(i.strip() for i in details).replace(' ','')
    # job_info[jobId].append(detail)
    # return job_info

ana()