

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

class TableView(QWidget):

    def __init__(self,arg=None):
        super(TableView, self).__init__(arg)

        self.setWindowTitle('试客联盟信息表获取')
        self.resize(500,300);

        self.model = QStandardItemModel(4,3)
        self.model.setHorizontalHeaderLabels(['ID','姓名','年龄'])

        self.tableviev = QTableView()
        # 关联QTableView控件Modle
        self.tableviev.setModel(self.model)

        # 添加数据
        # item11 = QStandardItem("10")
        # item12 = QStandardItem("雷神")
        # item13 = QStandardItem("200")
        self.model.setItem(0,0,QStandardItem("10"))
        self.model.setItem(0,1, QStandardItem("雷神"))
        self.model.setItem(0,2,  QStandardItem("200"))

        item11 = QStandardItem("10")
        item12 = QStandardItem("雷神")
        item13 = QStandardItem("200")
        self.model.setItem(1,0,item11)
        self.model.setItem(1,1, item12)
        self.model.setItem(1,2, item13)

        #设置布局
        Layout = QVBoxLayout()
        Layout.addWidget(self.tableviev)

        #禁止编辑



        self.setLayout(Layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    table = TableView()
    table.show()
    sys.exit(app.exec_())






