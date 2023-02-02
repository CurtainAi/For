import tkinter as tk
from tkinter import messagebox
import execjs
import requests
import re

from requests import  Session
from requests.cookies import cookiejar_from_dict

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}
url = "http://login.shikee.com/getkey?v=fbb1d0fcaa1e2d9c4c6e321ba6c5cc5f"

resp = requests.get(url, headers=header).text  # 拿到ras_n的密文
ex = 'var rsa_n = "(.*?)";'  # 正则
ras_n = re.findall(ex, resp)[0]

root = tk.Tk()
root.geometry('300x180')
root.title("登录页")

username = tk.StringVar()
password = tk.StringVar()


page = tk.Frame(root)
page.pack()

tk.Label(page).grid(row=0,column=0)

tk.Label(page,text='账户：').grid(row=1,column=1)
tk.Entry(page,textvariable=username).grid(row=1,column=2)

tk.Label(page,text='密码：').grid(row=2,column=1,pady=10)
tk.Entry(page,textvariable=password).grid(row=2,column=2)

def login():
    # name = username.get()
    # pwd = password.get()
    name =  "火钳刘明"
    pwd = "jinjun521"

    node = execjs.get()  # 创建node对象
    ctx = node.compile(open(r'C:\Users\ZhangJinJun\PycharmProjects\For\Project\Gui_Shikee_Login\rsa.js', encoding="utf-8").read())  # 编译js文件
    funcName = 'getPwd("{0}","{1}")'.format(pwd, ras_n)  # 为函数传入参数
    pwd = ctx.eval(funcName)  # 执行函数


    url = "http://login.shikee.com/check/"
    params = {
        "": "",
        "_1675319354633": ""
    }
    data = {
        "username": name,
        "password": pwd,
        "vcode": "",
        "to": "http://www.shikee.com/"
    }

    response = requests.post(url, headers=header, params=params, data=data, verify=False)
    cookies = response.cookies
    cookie = requests.utils.dict_from_cookiejar(cookies)
    print(cookie)

    # try:
    #     response = requests.post(url, headers=header, params=params, data=data, verify=False)
    #     cookies = res.cookies
    #     cookie = requests.utils.dict_from_cookiejar(cookies)
    #     print(cookie)
    #
    # except Exception as err:
    #     print('获取cookie失败：\n{0}'.format(err))





    print(response.json())
    print(cookies)


    # messagebox.showwarning(title='cookie',message=pwd)
    # print(pwd)
    # if name == 'admin ' and pwd =='123456':
    #     print("登录成功！")
    # else:
    #     messagebox.showwarning(title='警告',message='登录失败，请检查账号密码是否正确')

tk.Button(page,text='登录',command=login).grid(row=3,column=1,pady=10)
tk.Button(page,text='退出',command = page.quit).grid(row=3,column=2)

root.mainloop()


























