import flask
from flask import request
import requests
import re
import json

FindJson = r'<\!\-\-s\-data\:(.*?)\-\-\>'

app = flask.Flask(__name__)
@app.route('/',methods=['get'])

def get_news():
    num = request.values.get("num")
    try:
        url = 'https://top.baidu.com/board?tab=realtime'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
            "Host": "top.baidu.com"
        }
        response = requests.get(url=url, headers = headers)
        response.encoding = response.apparent_encoding
        response = response.text
        response = re.findall(FindJson,response)
        datas = response[0]
        datas = json.loads(datas)["data"]["cards"][0]["content"]
        #datas = json.dumps(datas)
        json_datas = []
        for i, item in enumerate(datas):
            json_data = []

            try:
                index = item['index']
            except:
                index = "unll"

            try:
                word = item["word"]
            except:
                word = "unll"

            try:
                desc = item["desc"]
            except:
                desc = "unll"

            try:
                img = item["img"]
            except:
                img = "unll"

            try:
                rawUrl = item['rawUrl']
            except:
                rawUrl = "unll"

            try:
                hotTag = item['hotTag']
            except:
                hotTag = "unll"

            json_data.append(index)
            json_data.append(word)
            json_data.append(desc)
            json_data.append(img)
            json_data.append(rawUrl)
            json_data.append(hotTag)
            json_datas.append(json_data)

            if i > int(num)-2:
                break;
        jsons = json.dumps(json_datas)
    except:
        jsons = {'code':10007,'message':'百度TOP接口获取错误！请联系管理员！'}
    return jsons

if __name__ == "__main__":
    app.run(debug=True, port=9000, host='0.0.0.0')