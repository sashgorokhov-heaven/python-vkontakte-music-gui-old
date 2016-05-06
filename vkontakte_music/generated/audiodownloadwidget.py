# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\sashg\PycharmProjects\VK-P-P-Music-Project\vkontakte_music\qtdesigner\audiodownloadwidget.ui'
#
# Created: Fri May 06 19:08:07 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(417, 22)
        Form.setMaximumSize(QtCore.QSize(16777215, 22))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setStyleSheet("QProgressBar {\n"
"padding: 1px;\n"
"border-color: rgb(36, 36, 36);\n"
"background: rgb(255, 255, 255);\n"
"text-align: left;\n"
"}\n"
"QProgressBar::chunk {\n"
"background: rgb(170, 170, 255);\n"
"border-top-right-radius: 2px;\n"
"border-bottom-right-radius: 2px;\n"
"}")
        self.progressBar.setProperty("value", 18)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtGui.QProgressBar.BottomToTop)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.progressBar.setFormat(QtGui.QApplication.translate("Form", "   Artist - Title", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
