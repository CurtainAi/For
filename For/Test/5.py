import sys, json
from PyQt5.QtWidgets import (QWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QLabel,QMessageBox)


class JsonToDict(QWidget):

    def __init__(self, parent=None):
        super(JsonToDict, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle('JsonToDict')

        json_label = QLabel('json文本')
        self.json_text_edit = QTextEdit(self)
        dict_label = QLabel('dict文本')
        self.dict_text_edit = QTextEdit(self)

        json_layout = QHBoxLayout()  # 将label和textEdit横向布局
        json_layout.addWidget(json_label)
        json_layout.addWidget(self.json_text_edit)

        dict_layout = QHBoxLayout()
        dict_layout.addWidget(dict_label)
        dict_layout.addWidget(self.dict_text_edit)

        json_btn = QPushButton('json_to_dict')
        json_btn.clicked.connect(self.json_click)  # 添加点击事件
        dict_btn = QPushButton('dict_to_json')
        dict_btn.clicked.connect(self.dict_click)  # 添加点击事件
        clear_btn = QPushButton('清空')
        clear_btn.clicked.connect(self.clear_click)  # 添加点击事件

        btn_layout = QHBoxLayout()  # 将button横向布局
        btn_layout.addWidget(json_btn)
        btn_layout.addWidget(dict_btn)
        btn_layout.addWidget(clear_btn)

        overall_layout = QVBoxLayout()  # 整体竖向布局
        overall_layout.addLayout(json_layout)
        overall_layout.addLayout(dict_layout)
        overall_layout.addLayout(btn_layout)

        self.setLayout(overall_layout)

        self.show()

    def json_click(self):
        json_content = self.json_text_edit.toPlainText()
        try:
            self.dict_text_edit.setText(str(json.loads(json_content)))
        except Exception as e:
            QMessageBox.critical(self, "错误", "输入有误!")

    def dict_click(self):
        dict_content = self.dict_text_edit.toPlainText()
        try:
            self.json_text_edit.setText(json.dumps(eval(dict_content)))
        except Exception as e:
            QMessageBox.critical(self, "错误", "输入有误!")

    def clear_click(self):
        self.json_text_edit.clear()
        self.dict_text_edit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JsonToDict()
    sys.exit(app.exec_())