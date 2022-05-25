import sys,requests,re,time
from gui import Ui_Form
from PyQt5.QtWidgets import QApplication,QMainWindow,QTableWidgetItem

regularList = r'"(http://\w+.shikee.com/\d+\.html)"[\S\s\n]*?"([\w\:/\.\_\s]*?\.jpg)"[\S\s\n]*?alt="(.*?)">[\S\s\n]*?份数：[\S\s\n]*?>(\d+)<[\S\s\n]*?申请人数：[\S\s\n^\d]*?(\d+)</[\S\s\n]*?邮费：[\S\s\n]*?red">(.*?)<'


class MainWindow(QMainWindow):
    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        #self.tablewidget.setHorizontalHeaderLabels(['title', 'applyAll', 'apply', 'send', 'url', 'urlPic'])

    def getList(self):
        self.ui.pushButton_2.setText('Start...')
        self.ui.pushButton_2.setEnabled(False)
        #_translate = self.ui.QtCore.QCoreApplication.translate

        #self.pushButton_2.clicked.connect(Form.getList)
        pageAll = 3
        listAll = []
        i = -1
        for page in range(pageAll):
            url_main = 'http://list.shikee.com/list-{}.html?type=1&cate=0&posfree=0&try_order=0&try_type=0&qr_code=0&sort=desc&pkey=0&brand_cid=0&brand_id=0'.format(page+1)
            res = requests.get(url=url_main,headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}).text
            resRrray = re.findall(regularList,res)
            #print(resRrray)
            print('正在获取第{}页，获取数量{}个...'.format(page+1,len(resRrray)))
            time.sleep(2)
            for j,list in enumerate(resRrray):
                i += 1
                print(i,list[2])

                newItem = self.ui.Q.
                self.ui.tablewidget.setItem(i, 0, newItem)
                listAll.append(list)
        print('获取完成，共获取页{}内容，应获取{}条数据，实际获取{}条数据。'.format(pageAll,pageAll*20,len(listAll)))
        self.ui.pushButton_2.setText('Start')
        self.ui.pushButton_2.setEnabled(True)
        return listAll

    def clearResult(self):
        print(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
