

from PyQt5.QtWidgets import (QWidget,QTableWidget,QHBoxLayout,QApplication,QTableWidgetItem)
import sys

class QTableWidgetDemo(QWidget):
    def __init__(self):
        super(QTableWidgetDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("试客联盟数据获取列表")
        self.resize(1000,800)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = QTableWidgetDemo()
    example.show()
    sys.exit(app.exec_())






