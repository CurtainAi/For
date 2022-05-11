# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 16:55:51 2022

@author: admin
"""
import pandas as pd
import time
import datetime
import requests
from pyquery import PyQuery as pq


def creat_header(headerstr):
    data = headerstr.split('\n')
    result = {}
    for x in data:
        if x == '':
            # print(x)
            continue
        ix = x.index(':')
        k = x[:ix].strip()
        v = x[ix + 1:].strip()
        result[k] = v
    return result


list_urls = [
    'https://www.che168.com/jinan/benchi/benchiglc/',
    'https://www.che168.com/jinan/list/?kw=glc%20300&pvareaid=101025&sw=glc%20300&risk=0',
    'https://www.che168.com/jinan/list/?kw=glc%20260&pvareaid=101025&sw=glc%20260&risk=0',
]

headerstr = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Connection: keep-alive
Cookie: userarea=370100; ahpvno=1; fvlid=16476109083133XbHw6QuFmRV; sessionid=8a61d859-b91f-438b-b6ab-e005429f202c; sessionip=112.232.129.200; area=370103; sessionvisit=72111219-d4d4-413a-8b97-84ffc23357a6; sessionvisitInfo=8a61d859-b91f-438b-b6ab-e005429f202c||100519; UsedCarBrowseHistory=0%3A43114327; showNum=1; sessionuid=8a61d859-b91f-438b-b6ab-e005429f202c
DNT: 1
Host: www.che168.com
sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'''

headers = creat_header(headerstr)
target_urls = []
# 获取详情页
for list_url in list_urls:
    req = requests.get(url=list_url, headers=headers)
    html = req.content.decode('gbk')

    doc = pq(html)

    lis = doc('div.tp-cards-tofu.fn-clear ul.viewlist_ul li')

    for i in range(len(lis)):
        li = lis.eq(i)
        a = li('a.carinfo')
        url = a.attr['href']
        if 'che168.com' in url or 'semnt.autohome.com.cn' in url:
            continue
        url = 'https://www.che168.com' + url
        target_urls.append(url)
        # print(li.text())
    # %%
alldata = []
url = target_urls[0]
url = 'https://www.che168.com/dealer/111769/42084571.html?pvareaid=105562'
target_urls = list(set(target_urls))

for url in target_urls:
    url_key = url.split('?')[0]
    req = requests.get(url=url, headers=headers)
    html = req.content.decode('gbk')

    # 名称、是否原创质保、表显里程、上牌时间、档位/排量、车辆所在地、查看限迁地
    # 价格、新车价格、二手车参考价格、
    # 车商
    doc = pq(html)
    data = {}

    data['url_key'] = url_key
    data['title'] = doc('h3.car-brand-name').text()

    data['price'] = doc('div.brand-price-item span.price').text()
    # data['base_price'] = doc('div.brand-price-item p#CarNewPrice').text()

    lis = doc('ul.basic-item-ul li')

    for li in lis.items():
        print(li.html())
        k = li('span').text().replace('  ', '').replace('\xa0', '')
        li.remove('span')
        data[k] = li.text().replace('  ', '').replace('\xa0', '')

    # 原厂质保 'https://www.che168.com/dealer/111769/42084571.html?pvareaid=105562'
    tag = doc('div.car-tags')
    data['tag_content'] = doc('div.car-tags div.tag-content').text()
    tag.remove('div.tag-content')
    data['tag'] = tag.text()

    # % 二手车商
    data['manger-name'] = doc('div.protarit-list span.manger-name').text()
    data['protarit-adress'] = doc('div.protarit-list div.protarit-adress').text()

    alldata.append(data)
    time.sleep(3)

alldata2 = pd.DataFrame(alldata)

today = datetime.datetime.now()
today = str(today.date())

alldata2.to_excel(f'{today}.xlsx')