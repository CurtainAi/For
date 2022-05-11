import flask
from flask import request
import requests
import re
import json

FindTitle = r'<a href="[\S\s\n]*?=top" target="_blank">(.*?)</a>'

app = flask.Flask(__name__)
@app.route('/',methods=['get'])

def get_news():
    num = request.values.get("num")
    try:
        url_main = 'https://s.weibo.com/top/summary'
        cookie = dict(SUB="_2AkMWyVQDf8NxqwJRmPEDSdwrEY1yyAzEieKglaXYJRMxHRl-yT9jqkk9tRB6PUl67IqWJN6ZvKHKSLDRM_OKZ68VbI12; ")
        header = {
             "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
         }
        if num == '':
            datas = {'code':10001,'message':'参数不能为空，获取数量：1-50'}
            #datas = json.dumps(datas, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
        else:
            if int(num) < 1:
                datas = {'code': 10001, 'message': '参数不能小于1，获取数量：1-50'}
            else:
                if int(num) > 50:
                    datas = {'code': 10001, 'message': '参数不能大于60，获取数量：1-50'}
                else:
                    response = requests.get(url=url_main, headers=header, cookies=cookie)
                    response.encoding = response.apparent_encoding
                    response = response.text
                    response = re.findall(FindTitle, response)
                    datas = []
                    for i, item in enumerate(response):
                        datas.append(str(i+1)+" : "+item)
                        if i == int(num) - 1:
                            break;
                    datas = json.dumps(datas)
    except:
        datas = {'code':10007,'message':'微博TOP接口获取错误！请联系管理员！'}
    return datas

if __name__ == "__main__":
    app.run(debug=True, port=9000, host='0.0.0.0')