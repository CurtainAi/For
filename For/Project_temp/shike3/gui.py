# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget,QTableWidget,QHBoxLayout,QApplication,QTableWidgetItem)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(978, 530)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 951, 441))
        self.groupBox.setObjectName("groupBox")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 931, 411))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(2000)
        self.tableWidget.setHorizontalHeaderLabels(['title', 'applyAll', 'apply', 'send', 'url', 'urlPic'])
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 460, 100, 50))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(150, 460, 100, 50))
        self.pushButton.setObjectName("pushButton")

        QTableWidgetItem('123')

        self.retranslateUi(Form)
        self.pushButton_2.clicked.connect(Form.getList)
        self.pushButton.clicked.connect(Form.clearResult)
        QtCore.QMetaObject.connectSlotsByName(Form)


        # self.resultText = QtWidgets.QTextEdit(self.groupBox)
        # self.resultText.setGeometry(QtCore.QRect(10, 60, 411, 181))
        # self.resultText.setObjectName("resultText")
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Getlist"))
        self.pushButton_2.setText(_translate("Form", "Start"))
        self.pushButton.setText(_translate("Form", "Clear"))
