from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtWidgets import QPushButton, QTableWidget, QTableWidgetItem, QLabel
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("窗口标题")  # 创建了一个窗口标题

        self.resize(980, 450)  # 创建窗口宽和高

        # 创建垂直布局
        layout = QVBoxLayout()

        # 1.创建水平布局，
        header_layout = QHBoxLayout()

        # 3.创建按钮控件
        btn_start = QPushButton("开始")

        # 4.将创建的按钮控件添加到header_layout水平布局中
        header_layout.addWidget(btn_start)

        # 5.创建按钮控件
        btn_stop = QPushButton("暂停")
        header_layout.addWidget(btn_stop)

        # 2.将水平布局添加到垂直布局中
        layout.addLayout(header_layout)

        # ------------------------------------

        # 1.创建水平布局
        from_layout = QHBoxLayout()

        # 3.创建输入框
        text_asin = QLineEdit()  # 创建输入框

        # 4.设置输入框提示信息
        text_asin.setPlaceholderText("请输入请求URL")

        # 5.将创建好的输入框控件添加到from_layout水平布局中
        from_layout.addWidget(text_asin)

        # 6.创建按钮控件
        btn_add = QPushButton("添加")
        from_layout.addWidget(btn_add)

        # 2.将创建的水平布局添加到layout水平布局中
        layout.addLayout(from_layout)

        # --------------------------------------

        # 1.创建水平布局
        table_layout = QHBoxLayout()

        # 3.创建表格
        # 参数1 多少行
        # 参数2 多少列
        table = QTableWidget(0, 8)
        # 创建一个列表，通过for循环来遍历里面的内容
        table_header = [
            {"field": "asin", "text": "ASIN", "width": 120},
            {"field": "title", "text": "标题", "width": 150},
            {"field": "url", "text": "URL", "width": 400},
            {"field": "price", "text": "低价", "width": 100},
            {"field": "success", "text": "成功次数", "width": 100},
            {"field": "error", "text": "503次数", "width": 100},
            {"field": "status", "text": "状态", "width": 100},
            {"field": "frequency", "text": "频率(N秒/次)", "width": 100},
        ]
        for idx, info in enumerate(table_header):
            # 4.创建表单元素内容
            item = QTableWidgetItem()
            # 设置元素的标题名称
            item.setText(info['text'])
            # 将创建的标题名称添加到表格中
            table.setHorizontalHeaderItem(idx, item)
            # 设置表格的编号和宽度
            table.setColumnWidth(idx, info['width'])

        # 5.将创建好的表格添加到 table_layout 水平布局中
        table_layout.addWidget(table)
        # 2.将创建的垂直布局添加到layout水平布局中
        layout.addLayout(table_layout)

        # ------------------------------------
        # 1.创建水平布局
        footer_layout = QHBoxLayout()

        label_status = QLabel("未检测", self)  # 创建标签
        footer_layout.addWidget(label_status)  # 将标签添加到底部菜单布局中

        # 添加弹簧
        footer_layout.addStretch()

        btn_reinit = QPushButton("重新初始化")
        footer_layout.addWidget(btn_reinit)

        btn_recheck = QPushButton("重新检测")
        footer_layout.addWidget(btn_recheck)

        btn_reset_count = QPushButton("次数清零")
        footer_layout.addWidget(btn_reset_count)

        btn_deleye = QPushButton("删除检测项")
        footer_layout.addWidget(btn_deleye)

        btn_alert = QPushButton("SMTP报警配置")
        footer_layout.addWidget(btn_alert)

        btn_proxy = QPushButton("代{过}{滤}理IP")
        footer_layout.addWidget(btn_proxy)

        # 2.将水平布局添加到layout垂直布局中
        layout.addLayout(footer_layout)

        # 将已设置好的布局应用到窗口中
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())