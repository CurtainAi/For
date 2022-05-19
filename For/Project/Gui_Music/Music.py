from Gui import Ui_MainWindow
import sys
import os
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication
import requests
import re
import time
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QWidget, QFileDialog, QMessageBox, QTableWidgetItem, \
    QTableWidget, QCheckBox, QComboBox


def random_user():
    user1 = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    user2 = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    user3 = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"
    user4 = "Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1"
    user5 = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"
    user6 = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"
    user7 = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    user8 = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)"
    user = [user1, user2, user3, user4, user5, user6, user7, user8]
    user = random.choice(user)
    header = {"User-Agent": user}
    return header


class down_thread(QThread):
    updata_data = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(down_thread, self).__init__(parent)

    def run_(self, music_id, type, filename, count):
        self.ID = music_id
        self.type = type
        self.filename = filename
        self.count = count

    def run(self):
        url = 'https://tool22.com/zb_tools/html/MusicPlayer/api.php?callback=jQuery111307113574961899647_1613446299040'
        lrc = 'https://tool22.com/zb_tools/html/MusicPlayer/api.php?callback=jQuery1113032117325286368126_1613485913531'

        data = {
            'types': 'url',
            'id': self.ID,
            'source': self.type,
        }
        data2 = {
            'types': 'lyric',
            'id': self.ID,
            'source': self.type,
        }
        header = random_user()

        mp3_addr = requests.post(url, headers=header, data=data).text
        try:
            lrc_1 = requests.post(lrc, headers=header, data=data2).content.decode('unicode_escape')
            lrc_2 = lrc_1.split('":"')[1].split('","')[0]
            with open(self.filename + '.lrc', 'w') as f:
                f.write(lrc_2)
        except:
            pass
        mp3_addr2 = re.findall(r'"url":"(.*?)",', mp3_addr)[0]
        qq = eval(repr(mp3_addr2).replace(r'\\/', '/'))

        reponse = requests.get(qq, headers=header)

        try:
            if reponse.status_code == 200:
                with open(self.filename + '.mp3', 'wb') as f:
                    for chunk in reponse.iter_content(chunk_size=512):
                        if chunk:
                            f.write(chunk)
            self.updata_data.emit('下载成功!', self.count)

        except:
            self.updata_data.emit('下载失败!', self.count)


class firstfrom(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnWidth(0, 180)
        self.ui.tableWidget.setColumnWidth(1, 50)
        self.ui.tableWidget.setColumnWidth(2, 50)
        self.ui.tableWidget.setColumnWidth(3, 200)

        self.ui.radioButton_2.setChecked(True)
        self.ui.pushButton_2.clicked.connect(self.change_dir)
        self.ui.pushButton.clicked.connect(self.star_find)
        self.ui.pushButton_3.clicked.connect(self.star_down)
        self.ui.checkBox.clicked.connect(self.check)
        self.ui.pushButton_4.clicked.connect(QCoreApplication.instance().quit)

    def check(self):
        if self.ui.tableWidget.rowCount() != 0:
            for i in range(0, self.ui.tableWidget.rowCount()):
                self.ui.tableWidget.item(i, 0).setCheckState(self.ui.checkBox.checkState())

    def star_down(self):
        if self.ui.tableWidget.rowCount() == 0:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请先搜索歌曲！')
            msg_box.exec_()
        else:
            if not os.path.exists(self.ui.label_2.text()):
                os.mkdir(self.ui.label_2.text())
            kk = self.ui.tableWidget.rowCount()
            print(self.ui.tableWidget.rowCount)
            for num in range(0, kk):
                if self.ui.tableWidget.item(num, 0).checkState() == 2:
                    self.ui.tableWidget.setItem(num, 3, QTableWidgetItem('正在下载'))

                    title = self.ui.tableWidget.item(num, 1).text()

                    mp3_name = self.ui.label_2.text() + '/' + self.ui.tableWidget.item(num, 0).text() + '_' + title

                    if self.ui.radioButton.isChecked:
                        type = "netease"
                    elif self.ui.radioButton_3.isChecked:
                        type = "qq"
                    elif self.ui.radioButton_2.isChecked:
                        type = "kugou"
                    elif self.ui.radioButton_4.isChecked:
                        type = "kuwo"
                    elif self.ui.radioButton_5.isChecked:
                        type = "xiami"
                    time.sleep(1)
                    self.down = down_thread()
                    self.down.run_(self.ui.tableWidget.item(num, 2).text(), type, mp3_name, num)
                    self.down.start()
                    self.down.updata_data.connect(self.write_word)

    def write_word(self, wrd, cont):
        self.ui.tableWidget.setItem(cont, 3, QTableWidgetItem(wrd))

    def change_dir(self):
        dir_ = QFileDialog.getExistingDirectory(self, '选择文件夹', '/')
        if dir_ != '':
            self.ui.label_2.setText(dir_)
        else:
            self.ui.label_2.setText('./mp3')

    def star_find(self):
        if self.ui.lineEdit.text() == '':
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入要搜索的关键词')
            msg_box.exec_()
        else:
            key_word = self.ui.lineEdit.text()
            url = "https://tool22.com/zb_tools/html/MusicPlayer/api.php?callback=jQuery111302869151257299616_1613380813496"
            if self.ui.radioButton.isChecked:
                type = "netease"
            elif self.ui.radioButton_3.isChecked:
                type = "qq"
            elif self.ui.radioButton_2.isChecked:
                type = "kugou"
            elif self.ui.radioButton_4.isChecked:
                type = "kuwo"
            elif self.ui.radioButton_5.isChecked:
                type = "xiami"
            data = {
                'types': 'search',
                'count': '100',
                'source': type,
                'pages': '1',
                'name': key_word

            }

            header = random_user()
            url_html = requests.post(url, headers=header, data=data).content.decode('unicode_escape')

            name = re.findall('"name":"(.*?)",', url_html)

            title2 = re.findall('"artist":(.*?),', url_html)

            url_id = re.findall('"url_id":(.*?),', url_html)
            pattern = re.compile(r"[\/\\\:\*\?\"\<\>\|]")
            self.ui.tableWidget.clear()
            self.ui.tableWidget.setColumnWidth(0, 180)
            self.ui.tableWidget.setColumnWidth(1, 150)
            self.ui.tableWidget.setColumnWidth(2, 80)
            self.ui.tableWidget.setColumnWidth(3, 150)
            self.ui.tableWidget.setRowCount(len(name))
            self.ui.tableWidget.setHorizontalHeaderLabels(['歌曲名', '歌手信息', '下载ID', '下载进度'])
            for row in range(0, len(name)):
                title = re.sub(pattern, "", title2[row])
                new_item1 = QTableWidgetItem(name[row])
                new_item1.setTextAlignment(QtCore.Qt.AlignCenter)
                new_item2 = QTableWidgetItem(title)
                new_item2.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(new_item1))
                self.ui.tableWidget.item(row, 0).setCheckState(0)
                self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(new_item2))
                self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(url_id[row]))
                self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(''))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = firstfrom()
    screen = QDesktopWidget().screenGeometry()
    size = w.geometry()
    w.setWindowTitle('全网音乐下载器')
    left = (screen.width() - size.width()) / 2
    hight = (screen.height() - size.height()) / 2
    #w.move(left, hight)
    w.show()
    sys.exit(app.exec_())