import execjs
import requests
import re

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}
url = "http://login.shikee.com/getkey?v=fbb1d0fcaa1e2d9c4c6e321ba6c5cc5f"

resp = requests.get(url, headers=header).text  # 拿到ras_n的密文
ex = 'var rsa_n = "(.*?)";'  # 正则
ras_n = re.findall(ex, resp)[0]


node = execjs.get()  # 创建node对象

pwd = '111111'  # 密码
ctx = node.compile(open(r'C:\Users\ZhangJinJun\Desktop\rsa.js', encoding="utf-8").read())  # 编译js文件
funcName = 'getPwd("{0}","{1}")'.format(pwd, ras_n)  # 为函数传入参数
password = ctx.eval(funcName)  # 执行函数
print(password)