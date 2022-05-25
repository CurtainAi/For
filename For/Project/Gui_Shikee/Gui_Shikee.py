
import sys
import requests
import re
import time
#from PyQt5.QtWidgets import (QWidget,QTableWidget,QHBoxLayout,QApplication,QTableWidgetItem)
from PyQt5.QtWidgets import (QWidget,QTableWidget,QHBoxLayout,QApplication,QTableWidgetItem,QAbstractItemView,QComboBox,QPushButton,QTableWidgetItem)
#from PyQt5.QtWidgets import *

from PyQt5.QtCore import Qt
#from PyQt5.QtCore import *

from PyQt5.QtGui import QColor ,QBrush,QFont

regularList = r'"(http://\w+.shikee.com/\d+\.html)"[\S\s\n]*?"([\w\:/\.\_\s]*?\.jpg)"[\S\s\n]*?alt="(.*?)">[\S\s\n]*?份数：[\S\s\n]*?>(\d+)<[\S\s\n]*?申请人数：[\S\s\n^\d]*?(\d+)</[\S\s\n]*?邮费：[\S\s\n]*?red">(.*?)<'

class ColumnSort(QWidget):
    def __init__(self):
        super(ColumnSort, self).__init__()
        self.initUI()

    def Get_Info(self,num):
        url_main = 'http://list.shikee.com/list-{}.html?type=1&cate=0&posfree=0&try_order=0&try_type=0&qr_code=0&sort=desc&pkey=0&brand_cid=0&brand_id=0'.format(num+1)
        res = requests.get(url=url_main,headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}).text
        res_array = re.findall(regularList,res)
        print('正在获取第{}页，获取数量{}个...'.format(num+1,len(res_array)))
        # list = []
        # for list in res_array:
        #     listall.append(list)
        return res_array

    def initUI(self):
        self.setWindowTitle("试客联盟数据获取列表")
        self.resize(1500,800)

        # 水平布局
        layout = QHBoxLayout()
        self.tablewidget = QTableWidget()



        #设置行和列
        self.tablewidget.setRowCount(2000)
        self.tablewidget.setColumnCount(6)
        layout.addWidget(self.tablewidget)

        # 列排序，升序or降序
        self.tablewidget.setHorizontalHeaderLabels(['title', 'applyAll', 'apply','send','url', 'urlPic'])

        # 设置按钮
        #self.button = QPushButton("开始获取")
        #self.button.clicked.connect(self.order)
        #layout.addWidget(self.button)

        self.setLayout(layout)

        # numAll = 20
        # for num in range(numAll):
        #     info = self.Get_Info(num)
        #     for i, list in enumerate(info):
        #         print(i)
        #         newItem = QTableWidgetItem(list[2])
        #         self.tablewidget.setItem(i, 0, newItem)
        #         newItem = QTableWidgetItem(list[3])
        #         self.tablewidget.setItem(i, 1, newItem)
        #         newItem = QTableWidgetItem(list[4])
        #         self.tablewidget.setItem(i, 2, newItem)
        #         newItem = QTableWidgetItem(list[5])
        #         self.tablewidget.setItem(i, 3, newItem)
        #         newItem = QTableWidgetItem(list[0])
        #         self.tablewidget.setItem(i, 4, newItem)
        #         newItem = QTableWidgetItem(list[1])
        #         self.tablewidget.setItem(i, 5, newItem)
        #     time.sleep(2)









            # for field in list:
            #self.tablewidget.setItem(0, 0, list[1])
            # self.tablewidget.setItem(0, 1, field)
            # self.tablewidget.setItem(0, 2, newItem)
            # self.tablewidget.setItem(0, 3, newItem)
            # self.tablewidget.setItem(0, 4, newItem)
            # self.tablewidget.setItem(0, 5, newItem)

        #print(info)


        #self.tablewidget.setSpan(0,0,3,1)


        # 设置单元格对齐方式
        # newItem = QTableWidgetItem("张三")
        # newItem.setTextAlignment(Qt.AlignRight | Qt.AlignBottom)
        # #newItem.setTextAlignment(Qt.Alignment | Qt.AlignBottom)
        # self.tablewidget.setItem(0,0,newItem)
        #
        # newItem = QTableWidgetItem("男")
        # newItem.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)
        # self.tablewidget.setItem(0,1,newItem)
        #
        # newItem = QTableWidgetItem("80")
        # newItem.setTextAlignment(Qt.AlignRight)
        # self.tablewidget.setItem(0,2,newItem)

        # 列排序，升序or降序
        # newItem = QTableWidgetItem("张三")
        # self.tablewidget.setItem(0,0,newItem)
        # newItem = QTableWidgetItem("男")
        # self.tablewidget.setItem(0,1,newItem)
        # newItem = QTableWidgetItem("80")
        # self.tablewidget.setItem(0,2,newItem)
        #
        # newItem = QTableWidgetItem("李四")
        # self.tablewidget.setItem(1,0,newItem)
        # newItem = QTableWidgetItem("女")
        # self.tablewidget.setItem(1,1,newItem)
        # newItem = QTableWidgetItem("60")
        # self.tablewidget.setItem(1,2,newItem)
        #
        # newItem = QTableWidgetItem("王五")
        # self.tablewidget.setItem(2,0,newItem)
        # newItem = QTableWidgetItem("男")
        # self.tablewidget.setItem(2,1,newItem)
        # newItem = QTableWidgetItem("89")
        # self.tablewidget.setItem(2,2,newItem)
        #
        # self.button = QPushButton("排序")
        # self.button.clicked.connect(self.order)
        # layout.addWidget(self.button)
        #
        # self.orderType =Qt.DescendingOrder


    # def order(self):
    #     if self.orderType == Qt.DescendingOrder:
    #         print(2)
    #         self.orderType = Qt.AscendingOrder
    #     else:
    #         print(1)
    #         self.orderType = Qt.DescendingOrder
    #     self.tablewidget.sortItems(2,self.orderType)


        # 设置字体大小和颜色
        # newItem = QTableWidgetItem("雷神")
        # newItem.setFont(QFont('Tiems',14,QFont.Black))
        # newItem.setForeground(QBrush(QColor(255,0,0)))
        # tablewidget.setItem(0,0,newItem)
        #
        # newItem = QTableWidgetItem('女')
        # newItem.setForeground(QBrush(QColor(255,255,0)))
        # newItem.setBackground(QBrush(QColor(0,0,255)))
        # tablewidget.setItem(0,1,newItem)
        #
        # newItem = QTableWidgetItem("160")
        # newItem.setFont(QFont('Tiems',20,QFont.Black))
        # newItem.setForeground(QBrush(QColor(0,0,255)))
        # tablewidget.setItem(0,2,newItem)
        #
        # self.setLayout(layout)




        # # 设置40行，4列
        # tablewidget.setRowCount(40)
        # tablewidget.setColumnCount(4)
        # layout.addWidget(tablewidget)
        #
        # # 填充数据
        # for i in range(40):
        #     for j in range(4):
        #         itemContent = '(%d,%d)'%(i,j)
        #         tablewidget.setItem(i,j,QTableWidgetItem(itemContent))
        # self.setLayout(layout)
        #
        # # 搜索满足条件的Cell(精确模式)
        # text = '(13,3)'
        # items = tablewidget.findItems(text,QtCore.Qt.MatchExactly)
        # if len(items) > 0:
        #     item = items[0]
        #     item.setBackground(QBrush(QColor(0,255,0)))
        #     item.setForeground(QBrush(QColor(255,0,0)))
        #
        #     row = item.row()
        #     #定位到指定的行(滚动)
        #     tablewidget.verticalScrollBar().setSliderPosition(row)
        #
        # # 搜索满足条件的Cell(匹配模式)
        # text = '(13'
        # items = tablewidget.findItems(text,QtCore.Qt.MatchStartsWith)
        # if len(items) > 0:
        #     item = items[0]
        #     item.setBackground(QBrush(QColor(0,255,0)))
        #     item.setForeground(QBrush(QColor(255,0,0)))
        #
        #     row = item.row()
        #     #定位到指定的行(滚动)
        #     tablewidget.verticalScrollBar().setSliderPosition(row)

        # 设置表格字段
        # tablewidget.setHorizontalHeaderLabels(['姓名','年龄','籍贯'])

        # 创建下拉选择
        # combox = QComboBox()
        # combox.addItem('男')
        # combox.addItem("女")

        # QSS
        # combox.setStyleSheet('QComboxBox{margin:3px};')
        # tablewidget.setCellWidget(0,1,combox)
        #
        # modifyButton = QPushButton("修改")
        # modifyButton.setDown(True)
        # modifyButton.setStyleSheet('QPushButton{margin:3px};')
        # tablewidget.setCellWidget(0,2,modifyButton)

        # 添加数据
        # textItem = QTableWidgetItem('小明')
        # tablewidget.setItem(0,0,textItem)
        # nameItem = QTableWidgetItem("小明")
        # tablewidget.setItem(0,0,nameItem)
        # ageItem = QTableWidgetItem("24")
        # tablewidget.setItem(0,1,ageItem)
        # jgItem = QTableWidgetItem("北京")
        # tablewidget.setItem(0,2,jgItem)

        # 禁止编辑
        # tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 整行选择
        # tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 调整列和行
        # tablewidget.resizeColumnsToContents()
        # tablewidget.resizeRowsToContents()

        # 表格头部显示和隐藏
        # tablewidget.horizontalHeader().setVisible(False)
        # tablewidget.verticalHeader().setVisible(False)

        # 设置标签
        # tablewidget.setVerticalHeaderLabels(['a','b'])

        # 隐藏表格线
        # tablewidget.setShowGrid(False)


        # self.setLayout(layout)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    #example = QTableWidgetDemo()
    example = ColumnSort()
    example.show()
    sys.exit(app.exec_())






