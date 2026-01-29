import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from window1 import Ui_Form


class Ui_widget(QWidget):

    def __init__(self):
        super(Ui_widget, self).__init__()
        self.setupUi()
        self.use_palette()


    def openwin(self):
        self.close()

        win.show()

    def use_palette(self):

        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("zhu4.png")))

        self.setPalette(window_pale)


    def setupUi(self):
        self.setObjectName("widget")
        self.resize(632, 473)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(70, 60, 501, 230))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(200, 250, 211, 61))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "首页"))
        self.label.setText(_translate("widget", "欢迎使用生猪疾病防治问题查询系统"))
        self.pushButton.setText(_translate("widget", "点击开始使用"))
        self.pushButton.clicked.connect(self.openwin)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_widget()

    window.show()
    win = Ui_Form()
    sys.exit(app.exec_())