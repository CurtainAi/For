
import psycopg2


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

#4、查询mysql，获取数据，并返回
def select_data(name):
    connect = server_postgrescon()
    cur = connect.cursor()
    # sql = '''
    # SELECT * FROM tb_contractor_data_dict where name='''+"'"+str(data)+"'"

    sql = '''
    SELECT name FROM tb_contractor_data_dict 
    '''
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    connect.close()
    print(results)
    return results


if __name__ == "__main__":
    conn = server_postgrescon()
    data = '特种设备作业资格证（气瓶充装）'
    select_data(data)
    print(conn )