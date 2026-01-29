import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication, QWidget
#from u2 import Ui_widget
from chatbot_graph import *

class Ui_Form(QWidget):

    def __init__(self):
        super(Ui_Form, self).__init__()
        self.setupUi()
        self.use_palette()

    def TextEdit_function(self):
        ques = self.textEdit.text()  # 获取文本框内容
        cb = ChatBotGraph()
        ans = cb.chat_main(ques)
        print(ans)
        self.textEdit_2.setText(ans)

    def use_palette(self):

        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("zhu2.jpg")))

        self.setPalette(window_pale)


    def setupUi(self):
        self.setObjectName("Form")
        self.resize(829, 564)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(30, 30, 221, 41))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QLineEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(30, 80, 741, 61))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(440, 200, 101, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(590, 200, 101, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self)
        self.textEdit_2.setGeometry(QtCore.QRect(30, 280, 741, 231))
        self.textEdit_2.setObjectName("textEdit_2")
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def addNum(self):
        ques = self.textEdit.text()  # 获取文本框内容
        cb = ChatBotGraph()
        ans = cb.chat_main(ques)
        print(ans)
        self.textEdit_2.setText(ans)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "生猪疾病防治问题查询"))
        self.label.setText(_translate("Form", "请输入您要查询的问题："))
        self.pushButton.setText(_translate("Form", "确 定"))
        self.pushButton_2.setText(_translate("Form", "退 出"))
        self.textEdit_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_2.clicked.connect(QCoreApplication.quit)
        self.pushButton.clicked.connect(self.addNum)
        self.textEdit.returnPressed.connect(self.TextEdit_function)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_Form()

    window.show()
    sys.exit(app.exec_())
