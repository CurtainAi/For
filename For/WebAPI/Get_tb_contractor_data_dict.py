import flask
import json
from flask import request
import requests
import time,datetime
import psycopg2

app = flask.Flask(__name__)
# server.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['get'])
def mysql_server():

    name = '通风工'

    if name == '':
        datas = {'code':10001,'message':'参数不能为空，请输入名称'}
        datas = json.dumps(datas, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    else:
        datas = select_data(name)
        datas = create_dic(datas)
        if datas==[]:
            datas = {'code': -1, 'message': '日期无效，日期格式：01-01'}
            datas = json.dumps(datas, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
        else:
            pass
            datas = json.dumps(datas, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)


    return datas


#1、输入日期，创建dic，并返回JSON文本，get获取，数据格式化
def create_dic(results):
    data_all = []
    for result in results[0]:
        data_all.append(result)
    # try:
    #     for result in results[0]:
    #         print(result)
    #         data_all.append(result)
    #         # data = {}
    #         # for i in range(len(results)):
    #         #     print(data)
    #         #     data_all.append(result)
    #         #     # print('----')
    #         #     # data[field_list[i][0]]=result[i]
    #
    # except:
    #     data_all= []
    # 4.返回数组
    print(data_all)
    return data_all



#2、获取访问者信息
def create_userinfo(datetime):
    # 1.定义返回数据类型数据
    userinfo_list = []
    # 2.获取User-Agent信息
    Agent = request.headers.get('User-Agent')
    Agent = "'"+Agent+"'"
    # 3.获取访问者IP
    ip = request.environ.get('HTTP_X_REAL_IP',request.remote_addr)
    ip = "'" + ip + "'"
    # 4.获取登录时间
    # time_new =time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(time_new)
    time_new=get_nowtime()

    time_new = "'" + str(time_new) + "'"

    # 5.用户信息
    datetime = "'"+str(datetime)+"'"

    # 5.所有信息加入数组
    userinfo_list.append("'historytoday'")
    userinfo_list.append(datetime)
    userinfo_list.append(Agent)
    userinfo_list.append(ip)
    userinfo_list.append(str(time_new))
    # insert_userinfo(userinfo_list)

    #return userinfo_list

#4、查询表所有数据并返回
def select_data(name):
    connect = server_postgrescon()
    cur = connect.cursor()
    # sql = '''
    # SELECT * FROM tb_contractor_data_dict where name='''+"'"+str(data)+"'"

    print(name)

    if name == 'all':
        sql = '''
        SELECT * FROM tb_contractor_data_dict 
        '''
    else:
        sql = '''
        SELECT * FROM tb_contractor_data_dict where name = '''+"'"+str(name)+"'"
    print(sql)

    cur.execute(sql)
    results = cur.fetchall()

    cur.close()
    connect.close()
    return results


#10、创建数据库链接
def server_postgrescon():
    #0.链接数据库

    conn = psycopg2.connect(
        host='127.0.0.1',  # 外网地址  (数据库管理中查看)
        port=5432,  # 外网端口  (数据库管理中查看)
        user='postgres',  # 账号      (初始化的账号)
        password='123456',  # 密码      (初始化的密码)
        database='postgres'  # 数据库名称
    )
    return conn


#11、获取北京时间，利用淘宝api
def get_nowtime():
    response =requests.get('http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp').text
    data = json.loads(response)
    timeStamp=data['data']['t']
    timeStamp=int(timeStamp)
    time_now=intTodatetime(timeStamp)
    return time_now


#12、时间戳格式化
def intTodatetime(intValue):
	if len(str(intValue)) == 10:
		# 精确到秒
		timeValue = time.localtime(intValue)
		tempDate = time.strftime("%Y-%m-%d %H:%M:%S", timeValue)
		datetimeValue = datetime.datetime.strptime(tempDate, "%Y-%m-%d %H:%M:%S")
	elif 10 <len(str(intValue)) and len(str(intValue)) < 15:
		# 精确到毫秒
		k = len(str(intValue)) - 10
		timetamp = datetime.datetime.fromtimestamp(intValue/(1* 10**k))
		datetimeValue = timetamp.strftime("%Y-%m-%d %H:%M:%S.%f")
	else:
		return -1
	return datetimeValue


if __name__ == '__main__':
    app.run(debug=True, port=9100, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问