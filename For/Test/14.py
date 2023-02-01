import flask  # 导入自带的web服务
from flask import request  # 导入自带的web服务中的request
from gevent import pywsgi  # 导入第三方的web服务

server = flask.Flask(__name__)


@server.route('/list/project', methods=['get'])  # 创建路径为/list/project的get接口
def Projectlist():
    proj = request.values.get('project')  # 获取get接口的参数project保存在proj中
    name = request.values.get('name')  # 获取get接口的参数name保存在name中
    project = {  # 准备构造返回的json
        "msg": "ok",
        "status": 200,
        "data": {
            "project": proj,
            "name": name
        }
    }
    return project  # 把构造的json格式返回


@server.route('/', methods=['POST'])  # 创建根路径的post接口
def post():
    name = request.stream.read()  # 额，这里其实是不想写了，只是想测试一下，就直接把请求体返回回去！
    return name


if __name__ == '__main__':
    app = pywsgi.WSGIServer(('127.0.0.1', 80), server)  # 创建一个本地服务
    app.serve_forever()  # 启动这个服务