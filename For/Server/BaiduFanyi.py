#[Python] python百度翻译爬虫

import requests
import re
while 1 < 10:
    f = 0
    url = "https://fanyi.baidu.com/sug"
    a = input("请输入要翻译的单词或句子:")
    head = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55"
    }
    dat = {
        "kw":a
    }
    b = requests.post(url,data=dat,headers = head)
    c = b.json()
    d = c['data']
    e = len(d)
    r = re.compile("{'k': '(?P<yc>.*?)', 'v': '(?P<fy>.*?)'}",re.S)
    while f < e:
        n = f + 1
        h = str(d[f])
        l = r.finditer(h)
        for m in l:
            print(str(n) + ". 原词: " + m.group("yc") + " 翻译 : " + m.group("fy"))
        f = f+1
        b.close()