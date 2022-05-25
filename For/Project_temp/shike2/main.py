
import sys
from PyQt5.QtWidgets import (QWidget,QTableWidget,QHBoxLayout,QApplication,QTableWidgetItem)
from PyQt5.QtCore import Qt
#from PyQt5.QtWidgets import (QWidget,QTableWidget,QHBoxLayout,QApplication,QTableWidgetItem,QAbstractItemView,QComboBox,QPushButton,QTableWidgetItem)
#from PyQt5.QtWidgets import *
#from PyQt5.QtGui import QColor ,QBrush,QFont
#from PyQt5.QtCore import *


class ColumnSort(QWidget):
    def __init__(self):
        super(ColumnSort, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("试客联盟数据获取列表")
        self.resize(1500,800)

        # 水平布局
        layout = QHBoxLayout()
        self.tablewidget = QTableWidget()

        #设置行和列
        self.tablewidget.setRowCount(4)
        self.tablewidget.setColumnCount(3)
        layout.addWidget(self.tablewidget)

        # 列排序，升序or降序
        self.tablewidget.setHorizontalHeaderLabels(['姓名', '性别', '体重[KG]'])
        newItem = QTableWidgetItem("张三")
        self.tablewidget.setItem(0, 0, newItem)
        #self.tablewidget.setSpan(0,0,3,1)
        newItem = QTableWidgetItem("男")
        self.tablewidget.setItem(0, 1, newItem)
        newItem = QTableWidgetItem("80")
        self.tablewidget.setItem(0, 2, newItem)

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
        self.setLayout(layout)

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






