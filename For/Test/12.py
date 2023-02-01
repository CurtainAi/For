import socket
import time
import os
from threading import Thread

response = """\
Transfer-Version: 1
Server: ES Name Response Server
Content-Type: text/html
Content-Length: 2
Connection: close

OK"""

class MItemObject():
    def __init__(self,f):
        self.rootDir = "" #存储根目录
        self.f = f
        self.ItemName = f.readline()
        self.ItemType = f.readline()

        self.fileSize = None
        self.fileRange = [None,None] # 文件数据位置
        self.endPos = None #结束位置，也是下一条目开始位置
        self.end = False #是否是最后一个条目

        if (b"\r\n" not in self.ItemName) or (b"\r\n" not in self.ItemType):
            raise BaseException(r"\r\n错误")
        else:
            self.ItemName = self.ItemName.strip(b"\r\n").decode()
            self.ItemType = self.ItemType.strip(b"\r\n").decode()

        if self.ItemType == "file":
            self.fileSize = int(f.readline().strip(b"\r\n").decode())
            self.fileRange = [f.tell(),f.tell()+self.fileSize]
            f.seek(self.fileRange[1])
            if f.readline().strip(b"\r\n").decode() != "File end":
                raise BaseException(r"File end错误")
            self.endPos = f.tell()

        elif self.ItemType == "folder":
            self.endPos = f.tell()
        else:
            raise BaseException(r"文件类型错误")

        print(self.ItemName,self.ItemType,self.fileSize,self.fileRange,self.endPos)

        if f.readline().strip(b"\r\n").decode() == "OVER":
            self.end = True

        self.saveData()
        f.seek(self.endPos)

    def saveData(self):
        if self.ItemType == "folder":
            if not os.path.exists(os.path.join(self.rootDir, self.ItemName)):
                os.mkdir(os.path.join(self.rootDir, self.ItemName))
        elif self.ItemType == "file":
            self.f.seek(self.fileRange[0])
            with open(os.path.join(self.rootDir, self.ItemName),"wb") as f:
                f.write(self.f.read(self.fileSize))
        self.f.seek(self.endPos)

def progress(arg):
    scale = 50
    i = int(arg * scale)

    a = "*" * i
    b = "." * (scale - i)
    c = (i / scale) * 100
    print("\r{:^3.0f}%[{}->{}]".format(c,a,b),end = "")

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def send_UDP():
    localIp = get_host_ip()
    port= 6343
    castAddr = '224.0.0.1'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind((localIp,port)) #绑定发送端口到SENDERPORT
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL , 1) #设置使用多播发送
    while True:
        sock.sendto(b'%s:%s:receive' % (name.encode(),localIp.encode()), (castAddr,port) )
        time.sleep(1)

def server():
    s = socket.socket()
    s.bind(("0.0.0.0",42135))
    s.listen(1)

    while True:
        conn,addr = s.accept()

        data = conn.recv(1024)
        conn.settimeout(2)
        # 读取头信息
        header = data.split(b"\r\n\r\n")[0]
        extraData = data.split(b"\r\n\r\n")[1]

        headerData = header.decode().split("\r\n")[1:]
        headerDict = {i.split(":")[0].strip():i.split(":")[1].strip() for i in headerData}
        # 读取掉无用的数据,缩略图
        while True:
            try:
                extraData += conn.recv(1024)
            except Exception as e:
                # print(e)
                break

        conn.settimeout(None)
        conn.send(response.encode())
        time.sleep(0.5)

        # 读取主要数据
        f = open("stream","wb")
        streamLen = 0
        allFileSize = int(headerDict["Content-Length"])
        while True:
            result = conn.recv(2048)
            streamLen += len(result)
            f.write(result)
            if streamLen > allFileSize:
                progress(1)
            else:
                progress(streamLen/allFileSize)

            if not result:
                break

        f.close()
        print("\n写入完成！")
        f = open("stream","rb")
        while True:
            item = MItemObject(f)
            if item.end:
                break

        f.close()
        os.remove("stream")

if __name__ == '__main__':
    name = "wshuo" #用户名
    Thread(target=send_UDP).start()
    server()