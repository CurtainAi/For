import sys, os, io
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon, QPixmap
import ddddocr
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import json
from threading import Thread
import base64
from PIL import Image
import pyperclip


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(
            str("请以POST方式发送图片数据    {img:'图像的base64编码'}\r\n返回格式   {\"status\": 1, \"msg\":\"识别成功\", \"code\": \"验证码内容\"}"
                ).encode())

    def do_POST(self):
        args = self.rfile.read(int(
            self.headers['content-length'])).decode("utf-8")
        self._response(self.path, args)

    def _response(self, path, args):
        # 组装参数为字典
        if args:
            args = urllib.parse.parse_qs(args).items()
            args = dict([(k, v[0]) for k, v in args])
        else:
            args = {}
        # 设置响应结果
        # print(args)
        if args.get("img") is not None:
            text = window.showImage(base64.b64decode(args["img"]))
            result = {"status": 1, "msg": "识别成功", "code": text}
        else:
            result = {
                "status": 0,
                "msg": "数据格式有误，请以POST方式发送 {img:'图像的base64编码'}",
                "code": ""
            }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(300, 200)
        loadUi(os.path.dirname(__file__) + "/ocr_web.ui", self)
        # self.sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        self.ocr = ddddocr.DdddOcr()
        self.btn.clicked.connect(self.startHttp)

    def showImage(self, _imageBytes, _clipboard):
        # print(_imageBytes)
        text = self.ocr.classification(_imageBytes)
        self.codeText.setText(text)
        print(text)
        pixmap = QPixmap()
        pixmap.loadFromData(_imageBytes)
        pixmap = pixmap.scaled(150, 60)
        self.image.setPixmap(pixmap)
        if _clipboard == "clipboard":
            # clipboard.setText(text)
            pyperclip.copy(text)  # 相当如写入到剪切板
        return text

    def startHttp(self):
        port = int(self.inputLabel.text())
        if port < 60 or port > 65535:
            port = 2300
        self.btn.setEnabled(False)
        self.btn.setText("服务已启动")
        Thread(target=openServer, args=(port,)).start()


def openServer(_port):
    print(_port)
    httpd = HTTPServer(('', _port), HttpHandler)
    httpd.serve_forever()


def image2byte(image):
    # 创建一个字节流管道
    img_bytes = io.BytesIO()
    # 把PNG格式转换成的四通道转成RGB的三通道，然后再保存成jpg格式
    image = image.convert("RGB")
    # 将图片数据存入字节流管道， format可以按照具体文件的格式填写
    image.save(img_bytes, format="JPEG")
    # 从字节流管道中获取二进制
    image_bytes = img_bytes.getvalue()
    return image_bytes


# 当剪切板变动会执行该方法
def clipboardChange():
    if window.cpCheckBox.checkState() == 2:
        data = clipboard.mimeData()
        # 获取剪切板内容格式
        print(data.formats())
        # 如果是文本格式，把内容打印出来
        if ('application/x-qt-image' in data.formats()):
            window.showImage(image2byte(Image.fromqimage(clipboard.pixmap())),
                             "clipboard")
        else:
            print("text:" + data.text())


app = QApplication(sys.argv)
clipboard = app.clipboard()
# 监听剪切板变动
clipboard.dataChanged.connect(clipboardChange)
clipboard.setText("pwm")
window = MainWindow()
window.setWindowTitle("P娃儿猫验证码识别v1.0")
window.setWindowIcon(QIcon(os.path.dirname(__file__) + '/Pwaerm.ico'))
window.show()
sys.exit(app.exec_())