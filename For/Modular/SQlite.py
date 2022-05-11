import sqlite3

#1.打开或创建数据库
conn = sqlite3.connect('test.db')
print("成功打开数据库")

#2.创建数据表
c = conn.cursor()   #获取游标
sql = '''
    create table company
        (id int primary key not null,
        name text not null,
        age int not null,
        address char(50),
        salary real);
'''
c.execute(sql)  #执行sql语句
conn.commit()   #提交数据库操作
conn.close()    #关闭数据库链接
print("成功建表")

#3.插入数据
c = conn.cursor()
sql1 = '''
    insert into company (id,name,age,address,salary)
    values (1,'张三',32,'成都',8000);
'''
sql2 = '''
    insert into company (id,name,age,address,salary)
    values (2,'李四',30,'青岛',15000);
'''
c.execute(sql1)
c.execute(sql2)
conn.commit()
conn.close()
print("插入成功")

#4.查询数据
c = conn.cursor()
sql = 'select id,name,address,age,salary from company'
curses = c.execute(sql)
for row in curses:
    print('id=',row[0] )
    print('name=', row[1])
    print('address=', row[2])
    print('age=', row[3])
    print('salary=', row[4],'\n')

conn.close()
print("查询完毕")

def main():
    print("start...")
    dbpath = r"D:\爬虫目录\SQL\baidutop.db"
    url = 'https://top.baidu.com/board?tab=realtime'
    datalist = get_datalist(url)
    saveData2DB(datalist, dbpath)

#保存数据到SQL
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

#创建数据库及数据表
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

if __name__ == "__main__":
    main()
    #init_db(dapath)



