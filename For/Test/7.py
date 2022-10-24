import time
import requests
import re
import win32gui
import win32con
import win32clipboard as w

url = 'http://www.ainicr.cn/qh/'


def getHtml(url, i):
    try:
        newurl = url + str(i) + '.html'
        r = requests.get(newurl)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        txt = re.findall('<p>(.*?)</p></a>', r.text)
        writetext(txt)
        sendmessage(txt)

    except:
        print("获取页面错误！")


def writetext(txt):
    f = open('C:/Users/l1768/Desktop/情话.txt', "ab")
    sum = 0
    for i in txt:
        sum = sum + 1
        f.write((str(sum) + '、' + i).encode('utf-8'))
        f.write('\n'.encode('utf-8'))
        f.seek(2)


def main():
    print("开始执行".center(20, '-'))
    for i in range(1000, 3000):
        try:
            time.sleep(10)
            getHtml(url, i)
            print(i)

        except:
            print("错误！！！")


def sendmessage(txt):
    for i in txt:
        # 发送的消息
        msg = i
        # 窗口名字
        name = "二硫碘化钾"
        # 将测试消息复制到剪切板中
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, msg)
        w.CloseClipboard()
        # 获取窗口句柄
        handle = win32gui.FindWindow(None, name)
        # while 1==1:
        if 1 == 1:
            # 填充消息
            win32gui.SendMessage(handle, 770, 0, 0)
            # 回车发送消息
            win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)


main()