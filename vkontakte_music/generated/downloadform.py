# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\sashg\PycharmProjects\VK-P-P-Music-Project\vkontakte_music\qtdesigner\downloadform.ui'
#
# Created: Sat May 07 23:37:50 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_download_form(object):
    def setupUi(self, download_form):
        download_form.setObjectName("download_form")
        download_form.resize(493, 448)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(172, 215, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(172, 215, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(172, 215, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(172, 215, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        download_form.setPalette(palette)
        self.verticalLayout = QtGui.QVBoxLayout(download_form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.destination_button = QtGui.QPushButton(download_form)
        self.destination_button.setObjectName("destination_button")
        self.verticalLayout.addWidget(self.destination_button)
        self.progressBar = QtGui.QProgressBar(download_form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.download_list_widget = QtGui.QListWidget(download_form)
        self.download_list_widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.download_list_widget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.download_list_widget.setObjectName("download_list_widget")
        self.verticalLayout.addWidget(self.download_list_widget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start_button = QtGui.QPushButton(download_form)
        self.start_button.setObjectName("start_button")
        self.horizontalLayout.addWidget(self.start_button)
        self.pause_button = QtGui.QPushButton(download_form)
        self.pause_button.setEnabled(False)
        self.pause_button.setObjectName("pause_button")
        self.horizontalLayout.addWidget(self.pause_button)
        self.delete_button = QtGui.QPushButton(download_form)
        self.delete_button.setEnabled(False)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout.addWidget(self.delete_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.album_folder_checkbox = QtGui.QCheckBox(download_form)
        self.album_folder_checkbox.setObjectName("album_folder_checkbox")
        self.verticalLayout.addWidget(self.album_folder_checkbox)

        self.retranslateUi(download_form)
        QtCore.QMetaObject.connectSlotsByName(download_form)

    def retranslateUi(self, download_form):
        download_form.setWindowTitle(QtGui.QApplication.translate("download_form", "Загрузки", None, QtGui.QApplication.UnicodeUTF8))
        self.destination_button.setText(QtGui.QApplication.translate("download_form", "Выбрать место загрузки", None, QtGui.QApplication.UnicodeUTF8))
        self.start_button.setText(QtGui.QApplication.translate("download_form", "Начать загрузку", None, QtGui.QApplication.UnicodeUTF8))
        self.pause_button.setText(QtGui.QApplication.translate("download_form", "Пауза", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_button.setText(QtGui.QApplication.translate("download_form", "Удалить", None, QtGui.QApplication.UnicodeUTF8))
        self.album_folder_checkbox.setToolTip(QtGui.QApplication.translate("download_form", "<html><head/><body><p>Будет создаваться отдельная папка с именем исполнителя, если мелодий больше одной</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.album_folder_checkbox.setText(QtGui.QApplication.translate("download_form", "Отдельная папка на каждого исполнителя", None, QtGui.QApplication.UnicodeUTF8))

