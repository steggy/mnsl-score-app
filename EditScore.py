# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editscore.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditScoreWindow(object):
    def setupUi(self, EditScoreWindow):
        EditScoreWindow.setObjectName("EditScoreWindow")
        EditScoreWindow.resize(738, 606)
        self.centralwidget = QtWidgets.QWidget(EditScoreWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lnEditScoreShooterName = QtWidgets.QLineEdit(self.centralwidget)
        self.lnEditScoreShooterName.setGeometry(QtCore.QRect(225, 51, 286, 36))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lnEditScoreShooterName.setFont(font)
        self.lnEditScoreShooterName.setObjectName("lnEditScoreShooterName")
        self.comboBoxDate = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxDate.setGeometry(QtCore.QRect(40, 51, 166, 36))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.comboBoxDate.setFont(font)
        self.comboBoxDate.setObjectName("comboBoxDate")
        self.ButtSelect = QtWidgets.QPushButton(self.centralwidget)
        self.ButtSelect.setGeometry(QtCore.QRect(515, 50, 89, 36))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ButtSelect.setFont(font)
        self.ButtSelect.setObjectName("ButtSelect")
        self.lblSelectedShooter = QtWidgets.QLabel(self.centralwidget)
        self.lblSelectedShooter.setGeometry(QtCore.QRect(45, 95, 626, 26))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lblSelectedShooter.setFont(font)
        self.lblSelectedShooter.setObjectName("lblSelectedShooter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 130, 711, 376))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tblScores = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tblScores.setObjectName("tblScores")
        self.tblScores.setColumnCount(7)
        self.tblScores.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblScores.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblScores.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblScores.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblScores.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblScores.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblScores.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblScores.setHorizontalHeaderItem(6, item)
        self.verticalLayout.addWidget(self.tblScores)
        self.ButtUpdate = QtWidgets.QPushButton(self.centralwidget)
        self.ButtUpdate.setGeometry(QtCore.QRect(45, 520, 89, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ButtUpdate.setFont(font)
        self.ButtUpdate.setObjectName("ButtUpdate")
        self.ButtCancel = QtWidgets.QPushButton(self.centralwidget)
        self.ButtCancel.setGeometry(QtCore.QRect(570, 520, 151, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ButtCancel.setFont(font)
        self.ButtCancel.setStyleSheet("background-color: rgb(239, 41, 41);")
        self.ButtCancel.setObjectName("ButtCancel")
        self.lblSession = QtWidgets.QLabel(self.centralwidget)
        self.lblSession.setGeometry(QtCore.QRect(140, 10, 571, 26))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblSession.setFont(font)
        self.lblSession.setObjectName("lblSession")
        EditScoreWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(EditScoreWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 738, 22))
        self.menubar.setObjectName("menubar")
        EditScoreWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(EditScoreWindow)
        self.statusbar.setObjectName("statusbar")
        EditScoreWindow.setStatusBar(self.statusbar)

        self.retranslateUi(EditScoreWindow)
        self.comboBoxDate.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(EditScoreWindow)
        EditScoreWindow.setTabOrder(self.comboBoxDate, self.lnEditScoreShooterName)
        EditScoreWindow.setTabOrder(self.lnEditScoreShooterName, self.ButtSelect)

    def retranslateUi(self, EditScoreWindow):
        _translate = QtCore.QCoreApplication.translate
        EditScoreWindow.setWindowTitle(_translate("EditScoreWindow", "Edit Score"))
        self.ButtSelect.setText(_translate("EditScoreWindow", "Select"))
        self.lblSelectedShooter.setText(_translate("EditScoreWindow", "TextLabel"))
        item = self.tblScores.horizontalHeaderItem(0)
        item.setText(_translate("EditScoreWindow", "id"))
        item = self.tblScores.horizontalHeaderItem(1)
        item.setText(_translate("EditScoreWindow", "sid"))
        item = self.tblScores.horizontalHeaderItem(2)
        item.setText(_translate("EditScoreWindow", "Date"))
        item = self.tblScores.horizontalHeaderItem(3)
        item.setText(_translate("EditScoreWindow", "event"))
        item = self.tblScores.horizontalHeaderItem(4)
        item.setText(_translate("EditScoreWindow", "division"))
        item = self.tblScores.horizontalHeaderItem(5)
        item.setText(_translate("EditScoreWindow", "cal"))
        item = self.tblScores.horizontalHeaderItem(6)
        item.setText(_translate("EditScoreWindow", "score"))
        self.ButtUpdate.setText(_translate("EditScoreWindow", "Update"))
        self.ButtCancel.setText(_translate("EditScoreWindow", "CANCEL/CLOSE"))
        self.lblSession.setText(_translate("EditScoreWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditScoreWindow = QtWidgets.QMainWindow()
    ui = Ui_EditScoreWindow()
    ui.setupUi(EditScoreWindow)
    EditScoreWindow.show()
    sys.exit(app.exec_())
