import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit

import re
#from Crypto.Cipher import DES
import base64
#from Crypto.Util.Padding import pad
import requests
import time
import json
import logging
import uuid
import os
import random, string
from requests_toolbelt.multipart.encoder import MultipartEncoder
from PIL import Image
import threading

# 全局变量
TableInfo = []
sendInfo = []

log = logging.getLogger("Foo")
logging.basicConfig(
    level=logging.INFO, format='%(levelname)s: %(filename)s - \n%(message)s')
log.setLevel(logging.DEBUG)


class ConsolePanelHandler(logging.Handler):

    def __init__(self, parent):
        logging.Handler.__init__(self)
        self.parent = parent

    def emit(self, record):
        self.parent.write(self.format(record))


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        log.debug('sendInfo.pop(0)')


class Worker(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.working = True

    def __del__(self):  # 线程状态改变与线程终止
        try:
            self.working = False
            self.wait()
        except Exception as e:
            print('get thread handle failed', e)

    def run(self):
        print('日志线程已启动')
        while True:
            if sendInfo:
                log.debug(sendInfo.pop(0))
            time.sleep(0.1)


class Table(QWidget):
    def __init__(self):
        super(Table, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('自动化模板')  # 设置标题
        self.resize(1280, 720)  # 设置初始大小

        """ 表格控件 """
        self.tableWidget = QTableWidget(0, 9)  # 水平布局，初始表格5*3，添加到布局
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive) # 手动调整列宽
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 列宽固定值
        self.tableWidget.setVerticalScrollBarPolicy(2)  # 竖直进度条常显
        # self.tableWidget.setVerticalScrollBarPolicy(2)                                     # 横向进度条常显
        # self.tableWidget.verticalHeader().setVisible(False)                                # 隐藏列表头
        self.tableWidget.verticalHeader().setHighlightSections(False)  # 不会因为鼠标点击选中而变色
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置水平方向自动伸缩填满窗口
        # self.tableWidget.horizontalHeader().setVisible(False)                              # 隐藏原始行
        self.tableWidget.horizontalHeader().setHighlightSections(False)  # 不会因为鼠标点击选中而变色
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置 不可选择单个单元格，只可选择一行。
        self.tableWidget.horizontalHeader().setStyleSheet('QHeaderView::section{background:SkyBlue}')  # 设置表头的背景色为绿色
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可更改
        # self.tableWidget.setSortingEnabled(True)                                           # 设置表头可以自动排序
        # self.tableWidget.setColumnHidden(1,True)                                           # 将第二列隐藏
        self.tableWidget.setHorizontalHeaderLabels(
            ['选中', '账号', '密码', '设备型号', '系统版本', '设备识别码', '完成次数', '目标次数', '运行状态'])  # 设置表格水平方向的头标签
        self.tableWidget.setMinimumWidth(800)
        self.tableWidget.setMaximumWidth(800)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许弹出菜单
        self.tableWidget.customContextMenuRequested.connect(self.RightMouse)  # 将信号请求连接到槽（单击鼠标右键，就调用方法）
        self.tableWidget.itemClicked.connect(self.LeftMouse)  # 将信号请求连接到槽（单击鼠标左键，就调用方法）

        """ 账号控件 """
        self.edit_user = QtWidgets.QLineEdit()  # 添加输入框控件
        self.edit_user.setFont(QFont("宋体", 16))  # 设置字体信息
        self.edit_user.setPlaceholderText('登录账号')  # 设置文本框提示文字
        self.edit_user.setMinimumHeight(30)  # 设置最小高度

        """ 密码控件 """
        self.edit_pwd = QtWidgets.QLineEdit()  # 添加输入框控件
        self.edit_pwd.setFont(QFont("宋体", 16))  # 设置字体信息
        self.edit_pwd.setPlaceholderText('登录密码')  # 设置文本框提示文字
        self.edit_pwd.setMinimumHeight(30)  # 设置最小高度

        """ 设备控件 """
        self.edit_device = QtWidgets.QLineEdit()  # 添加输入框控件
        self.edit_device.setFont(QFont("宋体", 16))  # 设置字体信息
        self.edit_device.setPlaceholderText('设备识别码')  # 设置文本框提示文字
        self.edit_device.setMinimumHeight(30)  # 设置最小高度

        """ 目标控件 """
        self.edit_updown = QtWidgets.QLineEdit()  # 添加输入框控件
        self.edit_updown.setFont(QFont("宋体", 16))  # 设置字体信息
        self.edit_updown.setPlaceholderText('目标次数')  # 设置文本框提示文字
        self.edit_updown.setMinimumHeight(30)  # 设置最小高度

        """ 登录控件 """
        self.btn_addUser = QPushButton('登录')  # 添加全选按钮
        self.btn_addUser.setFont(QFont("宋体", 16))  # 设置字体信息
        self.btn_addUser.setStyleSheet("background-color:LightCyan")  # 设置按钮颜色
        self.btn_addUser.clicked.connect(self.userLogin)  # 添加触发命令

        """ 登录模块 """
        self.loginBox = QVBoxLayout()  # 添加布局
        self.loginBox.addWidget(self.edit_user)  # 控件加入布局
        self.loginBox.addWidget(self.edit_pwd)  # 控件加入布局
        self.loginBox.addWidget(self.edit_device)  # 控件加入布局
        self.loginBox.addWidget(self.edit_updown)  # 控件加入布局
        self.loginBox.addWidget(self.btn_addUser)  # 控件加入布局

        """ 图片模块 """
        self.edit_path = QtWidgets.QLineEdit()  # 添加输入框控件
        self.edit_path.setFont(QFont("宋体", 16))  # 设置字体信息
        self.edit_path.setPlaceholderText('上传图片路径(.jpg格式)')  # 设置文本框提示文字
        self.edit_path.setMinimumHeight(30)  # 设置最小高度
        self.btn_path = QPushButton('>>')  # 添加搜索文件按钮
        self.btn_path.setFont(QFont("宋体", 16))  # 设置字体信息
        self.btn_path.setStyleSheet("background-color:LightCyan")  # 设置按钮颜色
        self.btn_path.setFixedSize(30, 30)  # 设置按钮大小
        self.btn_path.clicked.connect(self.filePath)  # 添加触发命令

        self.pathBox = QHBoxLayout()  # 添加布局
        self.pathBox.addWidget(self.edit_path)  # 控件加入布局
        self.pathBox.addWidget(self.btn_path)  # 控件加入布局

        """ 按钮控件 """
        self.btn_all = QPushButton('全选')  # 添加全选按钮
        self.btn_all.setFont(QFont("宋体", 16))  # 设置字体信息
        self.btn_all.setStyleSheet("background-color:LightCyan")  # 设置按钮颜色
        self.btn_all.clicked.connect(self.SelectAll)  # 添加触发命令

        self.btn_reverse = QPushButton('反选')  # 添加反选按钮
        self.btn_reverse.setFont(QFont("宋体", 16))  # 设置字体信息
        self.btn_reverse.setStyleSheet("background-color:LightCyan")  # 设置按钮颜色
        self.btn_reverse.clicked.connect(self.ReverseSelection)  # 添加触发命令

        self.btn_login = QPushButton('一键登录')  # 添加一键登录按钮
        self.btn_login.setFont(QFont("宋体", 16))  # 设置字体信息
        self.btn_login.setStyleSheet("background-color:GreenYellow")  # 设置按钮颜色
        self.btn_login.clicked.connect(self.All_Login)  # 添加触发命令

        self.btn_start = QPushButton('一键启动')  # 添加一键启动按钮
        self.btn_start.setFont(QFont("宋体", 16))  # 设置字体信息
        self.btn_start.setStyleSheet("background-color:GreenYellow")  # 设置按钮颜色
        self.btn_start.clicked.connect(self.All_Start)  # 添加触发命令

        """ 运行日志 """
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setStyleSheet("background-color:DimGray")
        self.textEdit.setStyleSheet(u'background-color:White; color:Green')
        self.textEdit.setMinimumWidth(480)
        # textEdit.setMaximumWidth(1000)
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        """ 登录单元 """
        self.loginModule = QFrame()  # 添加帧布局
        self.loginModule.setFrameShape(QFrame.StyledPanel)  # 显示边框
        self.loginModule.setLayout(self.loginBox)  # 加入布局
        self.loginModule.setFixedSize(300, 200)  # 设置大小

        """ 控制单元 """
        self.controlBox = QVBoxLayout()  # 添加帧布局
        self.controlBox.addLayout(self.pathBox)  # 控件加入布局
        self.controlBox.addWidget(self.btn_all)  # 控件加入布局
        self.controlBox.addWidget(self.btn_reverse)  # 控件加入布局
        self.controlBox.addWidget(self.btn_login)  # 控件加入布局
        self.controlBox.addWidget(self.btn_start)  # 控件加入布局

        self.controlModule = QFrame()  # 添加帧布局
        self.controlModule.setFrameShape(QFrame.StyledPanel)  # 显示边框
        self.controlModule.setLayout(self.controlBox)  # 加入布局

        """ 底部 水平分割 """
        self.bottomSplitter = QSplitter(self)  # 添加切割布局
        self.bottomSplitter.setOrientation(Qt.Horizontal)  # 水平分割
        self.bottomSplitter.addWidget(self.loginModule)  # 控件加入布局
        self.bottomSplitter.addWidget(self.controlModule)  # 控件加入布局
        self.bottomSplitter.handle(1).setDisabled(True)  # 禁止拖动布局

        """ 垂直分割 """
        self.leftSplitter = QSplitter(self)  # 添加切割布局
        self.leftSplitter.setOrientation(Qt.Vertical)  # 垂直分割
        self.leftSplitter.addWidget(self.tableWidget)  # 控件加入布局
        self.leftSplitter.addWidget(self.bottomSplitter)  # 控件加入布局
        self.leftSplitter.handle(1).setDisabled(True)  # 禁止拖动布局

        """ 水平分割 """
        self.rightSplitter = QSplitter(self)  # 添加切割布局
        self.rightSplitter.setOrientation(Qt.Horizontal)  # 水平分割
        self.rightSplitter.addWidget(self.leftSplitter)  # 控件加入布局
        self.rightSplitter.addWidget(self.textEdit)  # 控件加入布局
        self.rightSplitter.handle(1).setDisabled(True)  # 禁止拖动布局

        """ 主布局 """
        self.mainLayout = QVBoxLayout()  # 添加布局
        self.mainLayout.addWidget(self.rightSplitter)  # 控件加入布局
        self.setLayout(self.mainLayout)  # 加入布局

    def write(self, s):
        self.textEdit.setFontWeight(QtGui.QFont.Normal)
        self.textEdit.append(s)

    def userLogin(self):
        username = self.edit_user.text()
        password = self.edit_pwd.text()
        deviceID = self.edit_device.text()
        updown = self.edit_updown.text()
        if username == '' or password == '':
            self.edit_user.setText('')
            self.edit_pwd.setText('')
            self.edit_device.setText('')
            self.edit_updown.setText('')
            Tips('提示', '账号或密码不能为空\n\n请重新输入')
            return False

        deviceID = re.findall(r"[a-zA-Z0-9]{16}", deviceID)
        if deviceID:
            # print(deviceID)
            deviceID = deviceID[0]
        else:
            deviceID = self.getDeviceID()

        if updown == '' or int(updown) == 0:
            updown = 500
        else:
            updown = int(updown)

        phoneModel = self.getPhoneModel()
        systemVersion = self.getSystemVersion()

        userInfo = {
            'check': True,
            'username': username,
            'password': password,
            'phoneModel': phoneModel,
            'systemVersion': systemVersion,
            'deviceID': deviceID,
            'complete': 0,
            'updown': updown,
            'state': '尚未登录',
        }
        Info = Login(userInfo)
        if Info == False:
            return
        else:
            userInfo['sid'] = Info

        Info = appLoginSuccess(userInfo)
        if Info == False:
            return
        else:
            userInfo['sign'] = Info['sign']
            userInfo['JiuWDD'] = Info['JiuWDD']
            userInfo['QY_Code'] = Info['QY_Code']
            userInfo['QY_Name'] = Info['QY_Name']

        userInfo['cookie'] = 'JSESSIONID-L=' + str(uuid.uuid1())
        Info = getToken(userInfo)
        if Info == False:
            return
        else:
            userInfo['token'] = Info

        Info = apiCode(userInfo)
        if Info == False:
            return
        else:
            userInfo['WeifXW'] = Info

        userInfo['state'] = '登录成功'
        self.edit_user.setText('')
        self.edit_pwd.setText('')
        self.edit_device.setText('')
        self.edit_updown.setText('')

        for i in range(len(TableInfo)):
            if username == TableInfo[i]['username']:
                TableInfo[i].update(userInfo)
                TableInfo[i]['checkBox'].setChecked(userInfo['check'])
                self.tableWidget.item(i, 1).setText(str(TableInfo[i]['username']))
                self.tableWidget.item(i, 2).setText(str(TableInfo[i]['password']))
                self.tableWidget.item(i, 3).setText(str(TableInfo[i]['phoneModel']))
                self.tableWidget.item(i, 4).setText(str(TableInfo[i]['systemVersion']))
                self.tableWidget.item(i, 5).setText(str(TableInfo[i]['deviceID']))
                self.tableWidget.item(i, 6).setText(str(TableInfo[i]['complete']))
                self.tableWidget.item(i, 7).setText(str(TableInfo[i]['updown']))
                self.tableWidget.item(i, 8).setText(str(TableInfo[i]['state']))
                outputInfo(username, '覆盖登录', TableInfo[i])
                return
        self.addLine(userInfo)
        TableInfo.append(userInfo)
        outputInfo(username, '新增账号', TableInfo[len(TableInfo) - 1])

    def getDeviceID(self):
        code = ''
        for i in range(16):
            code += random.choice('abcdefghijklmnopqrstuvwxyz0123456789')
        return code

    def getPhoneModel(self):
        modelList = ['HD1910', 'GM1910', 'DLT-A0', 'NX627J', 'SKW-A0', 'NX629J', 'GM1900', 'SM-N9760', 'V1938T',
                     'V1936A', 'V1824A', 'V1916A', 'PCRT00', 'PCLM10', 'DT1901A', 'M973Q', 'MI 9', 'SEA-AL10',
                     'WLZ-AN00', 'PCT-AL10', 'OXF-AN10', 'ELE-AL00', 'VOG-AL00', 'HMA-AL00', 'LYA-AL10', 'TAS-AL00',
                     'TAS-AN00', 'LIO-AN00']
        return random.choice(modelList)

    def getSystemVersion(self):
        versionList = ['7.0', '7.1', '7.1.1', '7.1.2', '8.0', '8.1', '9', '10', '11']
        return random.choice(versionList)

    def filePath(self):

        file_dir = QFileDialog.getExistingDirectory(self, "选择图片文件夹", "/")
        file = file_name(file_dir)
        if file:
            self.edit_path.setText(file_dir)
        else:
            Tips('提示', '文件夹下未找到图片(.jpg格式)\n\n请检查后重试')

    def addLine(self, userInfo):
        # print(userInfo)
        row = self.tableWidget.rowCount()  # 当前已有数量
        self.tableWidget.setRowCount(row + 1)  # 增加一行
        self.tableWidget.setRowHeight(row, 35)  # 修改高度
        check = QCheckBox()  # 添加多选框
        check.setChecked(userInfo['check'])  # 修改多选框状态
        hBox = QHBoxLayout()  # 添加布局
        hBox.setAlignment(Qt.AlignCenter)  # 布局居中
        hBox.addWidget(check)  # 加入布局中
        widget = QWidget()  # 添加部件
        widget.setLayout(hBox)  # 加入
        self.tableWidget.setCellWidget(row, 0, widget)  # 加入表格

        userInfo['checkBox'] = check

        newItem = QTableWidgetItem(str(userInfo['username']))
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(row, 1, newItem)

        newItem = QTableWidgetItem(str(userInfo['password']))
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(row, 2, newItem)

        newItem = QTableWidgetItem(str(userInfo['phoneModel']))
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(row, 3, newItem)

        newItem = QTableWidgetItem(str(userInfo['systemVersion']))
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(row, 4, newItem)

        newItem = QTableWidgetItem(str(userInfo['deviceID']))
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(row, 5, newItem)

        newItem = QTableWidgetItem(str(userInfo['complete']))
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(row, 6, newItem)

        newItem = QTableWidgetItem(str(userInfo['updown']))
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(row, 7, newItem)

        newItem = QTableWidgetItem(str(userInfo['state']))
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(row, 8, newItem)

    def LeftMouse(self):
        for index in self.tableWidget.selectionModel().selection().indexes():
            row = index.row()
        if TableInfo[row]['check'] == True:
            TableInfo[row]['check'] = False
            TableInfo[row]['checkBox'].setChecked(False)
        else:
            TableInfo[row]['check'] = True
            TableInfo[row]['checkBox'].setChecked(True)

    def RightMouse(self, pos):
        for index in self.tableWidget.selectionModel().selection().indexes():
            row = index.row()
            menu = QMenu()
            item1 = menu.addAction("目标次数")
            item2 = menu.addAction("删除数据")
            item3 = menu.addAction("取消")
            # 使菜单在正常位置显示
            pos.setY(pos.y() + 25)
            screenPos = self.tableWidget.mapToGlobal(pos)
            # 单击一个菜单项就返回，使之被阻塞
            action = menu.exec(screenPos)
            if action == item1:
                d, okPressed = QInputDialog.getDouble(self, "Get double", "目标次数:", int(TableInfo[row]['updown']), 0,
                                                      10000, 0)
                if okPressed:
                    outputInfo(TableInfo[row]['username'], '修改目标', d)
            if action == item2:
                if Choice('提示', '是否删除[' + TableInfo[row]['username'] + ']\n本操作不可逆，请谨慎选择') == True:
                    outputInfo(TableInfo[row]['username'], '删除数据', TableInfo[row])
                    self.tableWidget.removeRow(row)
                    del TableInfo[row]
            else:
                return
            break

    def All_Login(self):
        for i in range(len(TableInfo)):
            if TableInfo[i]['checkBox'].isChecked() == False:
                outputInfo(userInfo['username'], '一键登录', '未选择')
                continue

            userInfo = TableInfo[i]
            if 'sid' in userInfo and 'sign' in userInfo and 'JiuWDD' in userInfo and 'QY_Code' in userInfo and 'QY_Name' in userInfo and 'token' in userInfo and 'WeifXW' in userInfo:
                outputInfo(userInfo['username'], '一键登录', '已经登录成功')
                continue

            if 'sid' not in userInfo:
                Info = Login(userInfo)
                if Info == False:
                    return
                else:
                    userInfo['sid'] = Info

            if 'sign' not in userInfo or 'JiuWDD' not in userInfo or 'QY_Code' not in userInfo or 'QY_Name' not in userInfo:
                Info = appLoginSuccess(userInfo)
                if Info == False:
                    return
                else:
                    userInfo['sign'] = Info['sign']
                    userInfo['JiuWDD'] = Info['JiuWDD']
                    userInfo['QY_Code'] = Info['QY_Code']
                    userInfo['QY_Name'] = Info['QY_Name']

            if 'token' not in userInfo:
                userInfo['cookie'] = 'JSESSIONID-L=' + str(uuid.uuid1())
                Info = getToken(userInfo)
                if Info == False:
                    return
                else:
                    userInfo['token'] = Info

            if 'WeifXW' not in userInfo:
                Info = apiCode(userInfo)
                if Info == False:
                    return
                else:
                    userInfo['WeifXW'] = Info

            userInfo['state'] = '登录成功'
            TableInfo[i].update(userInfo)
            self.tableWidget.item(i, 6).setText(str(TableInfo[i]['complete']))
            self.tableWidget.item(i, 7).setText(str(TableInfo[i]['updown']))
            self.tableWidget.item(i, 8).setText(str(TableInfo[i]['state']))
            outputInfo(userInfo['username'], '一键登录', TableInfo[i])
        outputInfo('', '一键登录', '执行完毕')

    def All_Start(self):
        thread1 = myThread(1, "Thread-1", 1)
        thread1.start()
        for i in range(len(TableInfo)):

            thread1 = myThread(1, "Thread-1", 1)
            thread1.start()

            if TableInfo[i]['checkBox'].isChecked() == False:
                outputInfo(userInfo['username'], '一键运行', '未选择')
                continue

            userInfo = TableInfo[i]
            if 'sid' in userInfo and 'sign' in userInfo and 'JiuWDD' in userInfo and 'QY_Code' in userInfo and 'QY_Name' in userInfo and 'token' in userInfo and 'WeifXW' in userInfo:
                outputInfo(userInfo['username'], '一键运行', '初始化。。。')
            else:
                outputInfo(userInfo['username'], '一键运行', '尚未登录，跳过')
                continue

            file_dir = self.edit_path.text()
            file = file_name(file_dir)
            if file:
                outputInfo(userInfo['username'], '一键运行', '图片数量[' + str(len(file)) + ']')
            else:
                outputInfo(userInfo['username'], '一键运行', '图片文件夹未找到图片，请检查后重试')
                Tips('提示', '图片文件夹未找到图片(.jpg格式)\n\n请检查后重试')
                return

            for i in range(len(file)):
                print(file[i])
                FJadd = fileSave(userInfo, file[i])
                if FJadd == False:
                    continue

                if add(userInfo, FJadd) == False:
                    continue

                outputInfo(userInfo['username'], '一键运行', '发送成功')

                # return

    def SelectAll(self):
        for i in range(len(TableInfo)):
            TableInfo[i]['check'] = True
            TableInfo[i]['checkBox'].setChecked(True)

    def ReverseSelection(self):
        for i in range(len(TableInfo)):
            if TableInfo[i]['checkBox'].isChecked() == True:
                TableInfo[i]['check'] = False
                TableInfo[i]['checkBox'].setChecked(False)
            else:
                TableInfo[i]['check'] = True
                TableInfo[i]['checkBox'].setChecked(True)


def Tips(title, info):
    messageBox = QMessageBox()
    messageBox.setWindowTitle(title)
    messageBox.setText(info)
    messageBox.addButton(QPushButton('确定'), QMessageBox.YesRole)
    messageBox.exec_()


def Choice(title, info):
    messageBox = QMessageBox()
    messageBox.setWindowTitle(title)
    messageBox.setText(info)
    messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    buttonY = messageBox.button(QMessageBox.Yes)
    buttonY.setText('确定')
    buttonN = messageBox.button(QMessageBox.No)
    buttonN.setText('取消')
    messageBox.exec_()
    if messageBox.clickedButton() == buttonY:
        return True
    else:
        return False


def Login(userInfo):
    url = '网址/appLogin'
    user = DesDecode(userInfo['username'], userInfo['password'])
    Data = {
        'userInfo': user,
        'terminal': 'app',
        'appVer': '1.0.1090',
        'loginOS': '8',
        'deviceID': userInfo['deviceID'],
        'OSVer': '30',
    }
    Headers = {
        'Connection': 'keep-alive',
        'platform': '2',
        'phoneModel': userInfo['phoneModel'],
        'systemVersion': userInfo['systemVersion'],
        'appVersion': '3.2.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '145',
        'Host': 'Host',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.2.0',
    }
    outputInfo(userInfo['username'], 'POST请求',
               'Url：' + url + '  Data：' + json.dumps(Data) + '  Headers：' + json.dumps(Headers))
    r = requests.post(url, allow_redirects=False, headers=Headers, data=Data)
    outputInfo(userInfo['username'], 'POST结果', 'StatusCode：' + str(r.status_code) + '  Response：' + r.text)
    # print(r)
    # print(r.encoding)
    # print(r.status_code)
    # print(r.text)
    # print(r.json())
    if r.status_code == 200:
        outputInfo(userInfo['username'], '登录失败', r.json()['outMsg'])
    elif r.status_code == 302 and r.headers['Location']:
        Location = r.headers['Location']
        # print(Location)
        re_data = re.compile('网址/appLoginSuccess;JSESSIONID=', re.I)
        SID = re_data.sub('', Location)  # 去掉DATA
        outputInfo(userInfo['username'], '登录成功', SID)
        return SID
    return False


def appLoginSuccess(userInfo):
    url = '网址/appLoginSuccess;JSESSIONID=' + userInfo['sid']
    Headers = {
        'Connection': 'keep-alive',
        'platform': '2',
        'phoneModel': userInfo['phoneModel'],
        'systemVersion': userInfo['systemVersion'],
        'appVersion': '3.2.0',
        'Host': 'Host',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.2.0',
        'Cookie': 'JSESSIONID-L=' + userInfo['sid'] + ';rememberMe=deleteMe',
    }
    outputInfo(userInfo['username'], 'GET请求', 'Url：' + url + '  Headers：' + json.dumps(Headers))
    r = requests.get(url, headers=Headers)
    outputInfo(userInfo['username'], 'GET结果', 'StatusCode：' + str(r.status_code) + '  Response：' + r.text)
    # print(r.encoding)
    # print(r.text)
    if r.status_code == 200:
        r_Json = r.json()
        if r_Json['outOk'] == '1':
            data = r_Json['data']
            Info = {
                'sign': data['sign'],
                'JiuWDD': data['unit']['dw_name_pre'] + data['unit']['dw_name_pre2'],
                'QY_Code': data['unitId'],
                'QY_Name': data['unit']['dw_name'],
            }
            outputInfo(userInfo['username'], '获取Sign成功', Info['sign'])
            return Info
        else:
            outputInfo(userInfo['username'], '获取Sign失败', r.json()['outMsg'])
    return False


def getToken(userInfo):
    url = '网址/app/getToken'
    Data = {
        'temianl': 'xxx',
        'platform': '8',
        'appversion': '1.5.4',
    }
    Headers = {
        'Connection': 'keep-alive',
        'Content-Length': '40',
        'Host': 'Host',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.2.0',
        'Cookie': userInfo['cookie'],
        'Accept': 'application/json',
        'sid': userInfo['sid'],
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 Html5Plus/1.0',
        'sign': userInfo['sign'],
        'Content-Type': 'application/x-www-form-urlencoded',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    outputInfo(userInfo['username'], 'POST请求',
               'Url：' + url + '  Data：' + json.dumps(Data) + '  Headers：' + json.dumps(Headers))
    r = requests.post(url, headers=Headers, data=Data)
    outputInfo(userInfo['username'], 'POST结果', 'StatusCode：' + str(r.status_code) + '  Response：' + r.text)
    # print(r)
    # print(r.encoding)
    # print(r.text)
    if r.status_code == 200:
        r_Json = r.json()
        if r_Json['outOk'] == '1':
            outputInfo(userInfo['username'], '获取Token成功', r_Json['data'])
            return r_Json['data']
        else:
            outputInfo(userInfo['username'], '获取Token失败', r.json()['outMsg'])
    return False


def apiCode(userInfo):
    url = '网址/api?apiCode=item_getlb'
    Data = {
        'ItemLB': 'QuanDXW',
        'temianl': 'xxx',
        'platform': '8',
        'appversion': '1.5.4',
    }
    Headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '54',
        'Host': 'Host',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 Html5Plus/1.0',
        'Accept': 'application/json',
        'sid': userInfo['sid'],
        'X-Requested-With': 'XMLHttpRequest',
        'sign': userInfo['sign'],
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': userInfo['cookie'],
    }
    outputInfo(userInfo['username'], 'POST请求',
               'Url：' + url + '  Data：' + json.dumps(Data) + '  Headers：' + json.dumps(Headers))
    r = requests.post(url, headers=Headers, data=Data)
    outputInfo(userInfo['username'], 'POST结果', 'StatusCode：' + str(r.status_code) + '  Response：' + r.text)
    # print(r)
    # print(r.encoding)
    # print(r.status_code)
    # print(r.text)
    # print(r.json())
    if r.status_code == 200:
        r_Json = r.json()
        if r_Json['outOk'] == 1:
            for Info in r_Json['rows1']:
                log.debug('ItemNo:' + Info['ItemNo'] + '  ItemMC:' + Info['ItemMC'])
                if Info['ItemMC'] == '不戴头盔':
                    return Info['ItemNo']
        outputInfo(userInfo['username'], '获取违法行为失败', r.json()['outMsg'])
    return False


def fileSave(userInfo, filePath):
    url = '网址/upload/fileSave?jsessionid=' + userInfo['sid']
    fileName = str(round(time.time() * 1000)) + '.jpg'
    num = string.ascii_letters + string.digits
    code = ''
    outFile = 'UpLoad/%s' % fileName
    exists(outFile)
    if compress(filePath, outFile) == True:
        filePath = outFile
    else:
        return False

    for i in range(6):
        code += random.choice(num)
    m = MultipartEncoder(fields={
        'file': (fileName, open(filePath, 'rb'), "image/jpeg"),
        'Content-Disposition': 'form-data',
        'name': 'box_camera_1',
        'Content-Type': 'image/jpeg'
    },
        boundary='------' + code)
    Headers = {
        'Connection': 'keep-alive',
        'Content-Type': m.content_type,
        'Content-Length': '8192',
        'Host': 'Host',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; M2012K10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 Html5Plus/1.0',
        'Accept': 'application/json',
        'sid': userInfo['sid'],
        'sign': userInfo['sign'],
        'Charset': 'UTF-8',
        'Cookie': userInfo['cookie'],
    }
    outputInfo(userInfo['username'], 'POST请求',
               'Url：' + url + '  fileName：' + fileName + '  filePath：' + filePath + '  code：' + code + '  Headers：' + json.dumps(
                   Headers))
    r = requests.post(url, data=m, headers=Headers)
    outputInfo(userInfo['username'], 'POST结果', 'StatusCode：' + str(r.status_code) + '  Response：' + r.text)
    # print(r)
    # print(r.encoding)
    # print(r.status_code)
    # print(r.text)
    # print(r.json())
    if r.status_code == 200:
        r_Json = r.json()
        if r_Json['outOk'] == 1:
            # print(r.json()['outMsg'])
            FJ = []
            FJ.append(r_Json['PREFIX'])
            FJ.append(r_Json['PATH'])
            FJ.append(r_Json['FILENAME'])
            FJ.append(r_Json['SIZE'])
            FJ.append(r_Json['MD5'])
            JoinStr = ','
            Str = JoinStr.join('%s' % id for id in FJ)
            outputInfo(userInfo['username'], '上传图片成功', Str)
            return Str
        else:
            outputInfo(userInfo['username'], '上传图片失败', r.json()['outMsg'])
    return False


def add(userInfo, FJadd):
    url = '网址/api?apiCode=btn_qdgzgl:add'
    Data = {
        'BM': '',
        'QY_Code': userInfo['QY_Code'],
        'QY_Name': userInfo['QY_Name'],
        'JiuWDD': userInfo['JiuWDD'],
        'BZ': '',
        'FJdel': '',
        'WeifXW': userInfo['WeifXW'],
        'XingM': '未提供',
        'CP': '无牌照',
        'JiuWSJ': time.strftime("%Y-%m-%d %H:%M", time.localtime()),
        'FJadd': FJadd,
        'temianl': 'xxx',
        'platform': '8',
        'appversion': '1.5.4',
    }
    Headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '544',
        'Host': 'Host',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; M2012K10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 Html5Plus/1.0',
        'Accept': 'application/json',
        'sid': userInfo['sid'],
        'X-Requested-With': 'XMLHttpRequest',
        'sign': userInfo['sign'],
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': userInfo['cookie'],
    }
    outputInfo(userInfo['username'], 'POST请求',
               'Url：' + url + '  Data：' + json.dumps(Data) + '  Headers：' + json.dumps(Headers))
    r = requests.post(url, headers=Headers, data=Data)
    outputInfo(userInfo['username'], 'POST结果', 'StatusCode：' + str(r.status_code) + '  Response：' + r.text)
    # print(r)
    # print(r.encoding)
    # print(r.status_code)
    # print(r.text)
    # print(r.json())
    if r.status_code == 200:
        r_Json = r.json()
        if r_Json['outOk'] == 1:
            # print(r.json()['outMsg'])
            # print(r.json()['outParam'])
            outputInfo(userInfo['username'], '上传数据成功', r.json()['outMsg'])
            return True
        else:
            # print(r.json()['outMsg'])
            outputInfo(userInfo['username'], '上传数据失败', r.json()['outMsg'])
    return False


def exists(path):  # 路径不存在则创建
    try:
        file_dir = os.path.split(path)[0]  # 获取路径目录
        if not os.path.isdir(file_dir):  # 目录是否存在
            os.makedirs(file_dir)  # 不存在则创建
    except:
        print(IOError)
        print('判断路径是否存在失败')
        return False


def compress(inFile, outFile, maxSize=150, step=10, quality=80, width=271, height=490):
    img = Image.open(inFile)
    w, h = img.size
    if w > h:  # 横屏图片
        limit_w = height
        limit_h = width
    else:
        limit_w = width
        limit_h = height
    if w > limit_w:
        h = int(limit_w / w * h)
        w = limit_w
    if h > limit_h:
        w = int(limit_h / h * w)
        h = limit_h
    out = img.resize((w, h), Image.ANTIALIAS)
    out.save(outFile)
    return True


def DesDecode(username, password):
    key = base64.b64decode('keY+V1ja1eo=')
    iv = base64.b64decode('AQIDBAUGBwg=')
    cryptor = DES.new(key=key, mode=DES.MODE_CBC, iv=iv)  # 秘钥
    text = '{"username":"' + username + '","password":"' + password + '"}'  # 合并字符串
    base = text.encode()  # base64 转字节
    padtext = pad(base, 8, style='pkcs7')
    entext = cryptor.encrypt(padtext)
    detext = base64.b64encode(entext).decode()
    return detext


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpeg' or os.path.splitext(file)[1] == '.jpg':
                # print(os.path.join(root, file))
                L.append(os.path.join(root, file))
    return L


def outputInfo(username, title='', info=''):
    timeInfo = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    output = '[%s]%s\n%s => %s' % (timeInfo, username, title, info)
    # example.thread.sinOut.emit(output)
    sendInfo.append(output)
    return output


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    example = Table()
    handler = ConsolePanelHandler(example)
    log.addHandler(handler)
    example.show()

    example.thread = Worker()
    # example.thread.sinOut.connect(log.debug)
    example.thread.start()
    sys.exit(app.exec_())