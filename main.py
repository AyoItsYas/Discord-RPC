import sys
import time
import json

from pypresence import Presence
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QWidget


class Ui_Dialog(object):
    def clickMethod(self):
        settings = {
            "ApplicationID": int(self.ApplicationID.text()),
            "State": str(self.State.text()),
            "Details": str(self.Details.text()),
            "LargeImage": str(self.LargeImage.text()),
            "LargeImageText": str(self.LargeImageText.text()),
            "SmallImage": str(self.SmallImage.text()),
            "SmallImageText": str(self.SmallImageText.text())
        }

        for k, v in settings.items():
            if v == '':
                v = None

        with open("./.data/settings.json", "w+") as file:
            json.dump(settings, file)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(406, 180)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./resources/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)

        self.ConnectButton = QtWidgets.QDialogButtonBox(Dialog)
        self.ConnectButton.setGeometry(QtCore.QRect(210, 20, 171, 51))
        self.ConnectButton.setAutoFillBackground(False)
        self.ConnectButton.setOrientation(QtCore.Qt.Vertical)
        self.ConnectButton.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.ConnectButton.setObjectName("ConnectButton")
        self.ConnectButton.clicked.connect(self.clickMethod)

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 51, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 47, 13))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 47, 13))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 110, 61, 16))
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(210, 110, 61, 16))
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 140, 61, 16))
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(210, 140, 71, 16))
        self.label_7.setObjectName("label_7")

        self.ApplicationID = QtWidgets.QLineEdit(Dialog)
        self.ApplicationID.setGeometry(QtCore.QRect(90, 20, 113, 20))
        self.ApplicationID.setObjectName("ApplicationID")

        self.State = QtWidgets.QLineEdit(Dialog)
        self.State.setGeometry(QtCore.QRect(90, 50, 113, 20))
        self.State.setObjectName("State")

        self.Details = QtWidgets.QLineEdit(Dialog)
        self.Details.setGeometry(QtCore.QRect(90, 80, 113, 20))
        self.Details.setObjectName("Details")

        self.LargeImage = QtWidgets.QLineEdit(Dialog)
        self.LargeImage.setGeometry(QtCore.QRect(90, 110, 113, 20))
        self.LargeImage.setObjectName("LargeImage")

        self.SmallImage = QtWidgets.QLineEdit(Dialog)
        self.SmallImage.setGeometry(QtCore.QRect(90, 140, 113, 20))
        self.SmallImage.setObjectName("SmallImage")

        self.LargeImageText = QtWidgets.QLineEdit(Dialog)
        self.LargeImageText.setGeometry(QtCore.QRect(270, 110, 113, 20))
        self.LargeImageText.setObjectName("LargeImageText")

        self.SmallImageText = QtWidgets.QLineEdit(Dialog)
        self.SmallImageText.setGeometry(QtCore.QRect(270, 140, 113, 20))
        self.SmallImageText.setObjectName("SmallImageText")

        self.retranslateUi(Dialog)
        self.ConnectButton.accepted.connect(Dialog.accept)
        self.ConnectButton.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Discord RPC"))
        self.label.setText(_translate("Dialog", "Application ID"))
        self.label_2.setText(_translate("Dialog", "State"))
        self.label_3.setText(_translate("Dialog", "Details"))
        self.label_4.setText(_translate("Dialog", "Large Image"))
        self.label_5.setText(_translate("Dialog", "Image Text"))
        self.label_6.setText(_translate("Dialog", "Small Image"))
        self.label_7.setText(_translate("Dialog", "Image Text"))


class Tray(QSystemTrayIcon):

    def __init__(self, icon, parent, Dialog):
        try:
            with open("./.data/settings.json", "r+") as file:
                self.settings = json.load(file)
        except:
            Dialog.show()
            return

        QSystemTrayIcon.__init__(self, icon, parent)

        menu = QMenu(parent)

        self.presence = Presence(self.settings["ApplicationID"])

        connect = menu.addAction("Connect")
        connect.triggered.connect(self.connect)
        connect.setIcon(QIcon("./resources/connect.svg"))

        disconnect = menu.addAction("Disconnect")
        disconnect.triggered.connect(self.disconnect)
        disconnect.setIcon(QIcon("./resources/disconnect.svg"))

        configure = menu.addAction("Configure")
        configure.triggered.connect(lambda: Dialog.show())
        configure.setIcon(QIcon("./resources/configure.svg"))

        menu.addSeparator()

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())
        exit_.setIcon(QIcon("./resources/exit.svg"))

        self.setContextMenu(menu)
        self.setToolTip("RPC : Running")

    def connect(self):
        self.presence.connect()

        start_time = time.time()

        self.presence.update(
            state=self.settings["State"],
            details=self.settings["Details"],
            large_image=self.settings["LargeImage"],
            large_text=self.settings["LargeImageText"],
            small_image=self.settings["SmallImage"],
            small_text=self.settings["SmallImageText"],
            start=start_time)
        self.setToolTip('RPC : Connected')

    def disconnect(self):
        self.presence.clear()
        self.setToolTip('RPC : Disconnected')


app = QApplication(sys.argv)

Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)

icon = QIcon("./resources/icon.ico")
parent = QWidget()
tray = Tray(icon, parent, Dialog)
tray.show()

app.exec_()
