# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'audiolistitemwidget.ui'
#
# Created: Thu Jun 19 00:03:49 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(393, 27)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(16777215, 55))
        Form.setAutoFillBackground(False)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(9, 0, 9, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.playpauseLabel = QtGui.QLabel(Form)
        self.playpauseLabel.setMaximumSize(QtCore.QSize(16, 16))
        self.playpauseLabel.setText("")
        self.playpauseLabel.setPixmap(QtGui.QPixmap(":/newFlatIcons/Icons/Button-Play-icon.png"))
        self.playpauseLabel.setScaledContents(True)
        self.playpauseLabel.setObjectName("playpauseLabel")
        self.horizontalLayout_2.addWidget(self.playpauseLabel)
        self.artistLabel = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.artistLabel.setFont(font)
        self.artistLabel.setWordWrap(False)
        self.artistLabel.setObjectName("artistLabel")
        self.horizontalLayout_2.addWidget(self.artistLabel)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.titleLabel = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.titleLabel.setFont(font)
        self.titleLabel.setWordWrap(False)
        self.titleLabel.setObjectName("titleLabel")
        self.horizontalLayout_2.addWidget(self.titleLabel)
        self.durationLabel = QtGui.QLabel(Form)
        self.durationLabel.setObjectName("durationLabel")
        self.horizontalLayout_2.addWidget(self.durationLabel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.stateLabel = QtGui.QLabel(Form)
        self.stateLabel.setText("")
        self.stateLabel.setObjectName("stateLabel")
        self.horizontalLayout_2.addWidget(self.stateLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.artistLabel.setText(QtGui.QApplication.translate("Form", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", " - ", None, QtGui.QApplication.UnicodeUTF8))
        self.titleLabel.setText(QtGui.QApplication.translate("Form", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.durationLabel.setText(QtGui.QApplication.translate("Form", "4:20", None, QtGui.QApplication.UnicodeUTF8))

import resourses.resourses_rc
