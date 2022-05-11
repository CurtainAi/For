import datetime
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main():
    weixinput()

#输入截止时间
def endtime():
    now = datetime.datetime.now()
    pmptime = datetime.datetime(2021,6,20)
    count_dowun = (pmptime-now).days
    return count_dowun
#微信提示
def weixinput():
    token = "21e474403c534045b9edefa2727e5bc1ae3dbf80"
    text = 'pmp考试'
    desp ="距离pmp考试时间还有%d天！请抓紧努力！！！"%endtime()
    url = 'https://api.ossec.cn/v1/send?token=%s&topic=%s&message=%s' % (token, text, desp)
    print(url)
    requests.get(url)
def main_handler(event, context):
    return main()

if __name__ == "__main__":
    main()

