import os
import random
import requests
import sqlite3

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}

dbpath_main = r"D:\爬虫目录\SQL\maoyan.db"
url_main= 'https://maoyan.com/'

#1.打开或创建数据库
conn = sqlite3.connect('maoyan.db')
print("成功打开数据库")

#2.创建数据表
def init_db(dbpath):
    sql = '''
        create table baiduTOP
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        title varchar,
        content text,
        num_index numeric
        )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print('创建成功！')

#3.插入数据
def saveData2DB(datalist,dbpath):
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        print(data)
        for index in range(len(data)):
            print(index)
            data[index] = '"'+data[index]+'"'
        sql = '''
            insert into baidutop(
            info_link,pic_link,title,content,num_index)
            values(%s)'''%",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

#获取response
def get_html(url):
    try:
        res=requests.get(url,headers = headers,allow_redirects=False,timeout=5)
        res.encoding='utf-8'
        return res
    except:
        print("html:ErrorURL:"+url)
        pass

#开始下载
def get_filedown(filepath,fileurl):
    try:
        with open(filepath,"wb") as f:
            f.write(requests.get(fileurl).content)
            print(filepath,url+" 下载成功！")
    except:
        print(filepath,url+"下载失败！")
        pass

#检测命名是否规范，不规范回返规范名称
def get_rename(name):
    sets = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in name:
        if char in sets:
            name = name.replace(char,"")
    if name == '':
        num = random.randrange(1000000,99999999)
        return "随机命名_"+str(num)
    else:
        return name

#获取文件信息(文件名称+后缀)
def get_filedata(url):
    try:
        res = get_html(url=url)
        useragent = res.headers

        #该处随机变动
        data = useragent['Content-Type']
        filename = data.split('/', )[0]
        filesuffix = data.split('/', )[1]

        item = [filename, filesuffix]
        return item
    except:
        print("filedata:false")
        pass

#检测目录是否存在，不存在创建目录，创建成功返回目录，创建失败返回None
def get_mkdir(filepath,filename):
    filename = get_rename(filename)
    filepath = filepath + "\\" + filename
    # 检测该目录是否存在，如果不存在进行创建，不存在则不执行
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return path
    else:
        return path

#取随机协议头
def get_UserAgent():
    user_agent_list = ['Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
                   'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
                   'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']
    UserAgent=random.choice(user_agent_list)
    return UserAgent


def main():
    print("start...")

    # datalist = get_datalist(url)
    # saveData2DB(datalist, dbpath)

if __name__ == "__main__":
    main()
