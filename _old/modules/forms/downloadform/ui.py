# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadform.ui'
#
# Created: Tue Jun 24 16:42:06 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(376, 299)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/Icons/windowicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.downloadListWidget = QtGui.QListWidget(Form)
        self.downloadListWidget.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.downloadListWidget.setProperty("showDropIndicator", False)
        self.downloadListWidget.setAlternatingRowColors(False)
        self.downloadListWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.downloadListWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.downloadListWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.downloadListWidget.setSpacing(0)
        self.downloadListWidget.setObjectName("downloadListWidget")
        self.verticalLayout.addWidget(self.downloadListWidget)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.startButton = QtGui.QPushButton(Form)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout_3.addWidget(self.startButton)
        self.pauseButton = QtGui.QPushButton(Form)
        self.pauseButton.setEnabled(False)
        self.pauseButton.setObjectName("pauseButton")
        self.horizontalLayout_3.addWidget(self.pauseButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Загрузки", None, QtGui.QApplication.UnicodeUTF8))
        self.startButton.setText(QtGui.QApplication.translate("Form", "Начать загрузку", None, QtGui.QApplication.UnicodeUTF8))
        self.pauseButton.setText(QtGui.QApplication.translate("Form", "Пауза", None, QtGui.QApplication.UnicodeUTF8))

import resourses.resourses_rc
