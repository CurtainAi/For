import requests
import re
import csv

headers = {
   'Connection': 'keep-alive',
   'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
   'sec-ch-ua-mobile': '?0',
   'Upgrade-Insecure-Requests': '1',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
   'Sec-Fetch-Site': 'same-origin',
   'Sec-Fetch-Mode': 'navigate',
   'Sec-Fetch-User': '?1',
   'Sec-Fetch-Dest': 'document',
   'Referer': 'https://www.kuaidaili.com/free/inha/1/',
   'Accept-Language': 'zh-CN,zh;q=0.9',
}


# proxies = {
#  "http": "http://10.10.1.10:3128",
#  "https": "https://10.10.1.10:1080",
# }
# requests.get("http://example.org", proxies=proxies)

def get_ip():
    for page in range(1, 3):
        url = f'https://free.kuaidaili.com/free/inha/{page}/'
        print(url)
        response = requests.get(url, headers=headers)

        ip_list = re.findall('data-title="IP">(.*?)</td>', response.text)
        print(ip_list)



def check_ip():
    list = []
    for ip in ip_list:
        try:
            response = requests.get('https://www.baidu.com', proxies=ip, timeout=2)
            print(ip)
            if response.status_code == 200:
                list.append(ip)
        except:
            pass
        else:
            print(ip, '检测通过')


# with open('ip.csv','a',newline='') as f:
#    writer = csv.writer(f)
#    writer.writerow(list)

if __name__ == '__main__':
    get_ip()

