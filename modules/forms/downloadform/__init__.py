import os
import sys

__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

import threading
from modules import util
from modules.gorokhovlibs.threadeddecor import threaded
import time
from PySide import QtGui, QtCore
from modules.forms.downloadform.ui import Ui_Form as UI_DownloadWidget

class AudioDownloadWidgetItem(QtGui.QListWidgetItem):
    def __init__(self, vkaudio, parent):
        super().__init__('{} - {}'.format(vkaudio.artist(), vkaudio.title()))
        self.vkaudio = vkaudio
        self.parent = parent

    def doubleClicked(self):
        self.parent.updateState.emit(self.vkaudio, 4)
        self.parent.downloadListWidget.takeItem(self.parent.downloadListWidget.row(self.item))

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked()


class AudioDownloadWidget(QtGui.QWidget, UI_DownloadWidget):
    updateState = QtCore.Signal(util.VkAudio, int)
    __setDownloadBarValue = QtCore.Signal(int)

    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.__stop = False
        self.loading = False
        self.audiolist = list()
        self.pauseLock = threading.Lock()
        self.pauseLock.acquire()
        self.worklock1 = threading.Lock()
        self.worklock2 = threading.Lock()
        self.firstshow = True
        self.hide()
        self.download_loop()
        self.uploaddir = os.path.split(sys.argv[0])[0]
        self.hideLabels()
        self.statusLabel.setText('Ожидание')
        self.startButton.clicked.connect(self.startButtonClicked)
        self.pauseButton.clicked.connect(self.pauseButtonClicked)
        self.__setDownloadBarValue.connect(self.downloadPBar.setValue)

    @QtCore.Slot()
    def hideLabels(self):
        self.titleLabel.setVisible(False)
        self.sepLabel.setVisible(False)
        self.artistLabel.setVisible(False)

    @QtCore.Slot()
    def showLabels(self):
        self.titleLabel.setVisible(True)
        self.sepLabel.setVisible(True)
        self.artistLabel.setVisible(True)

    def closeEvent(self, event):
        if self.__stop:
            event.accept()
        self.hide()

    @QtCore.Slot()
    def exiting(self):
        self.__stop = True
        self.close()

    @QtCore.Slot()
    def show(self):
        if self.firstshow:
            ndir = QtGui.QFileDialog.getExistingDirectory(self, 'Папка для загрузки', self.uploaddir, QtGui.QFileDialog.ShowDirsOnly)
            if ndir:
                self.uploaddir = ndir
            self.firstshow = False
        self.__setDownloadBarValue.emit(0)
        self._setVisible(True)


    @QtCore.Slot()
    def hide(self):
        self._setVisible(False)

    @QtCore.Slot(util.VkAudio)
    def add(self, vkaudio):
        item = AudioDownloadWidgetItem(vkaudio, self)
        self.downloadListWidget.addItem(item)
        self.updateButton('Ожидают загрузки')

    def updateButton(self, text):
        self.parent.downloadButton.setText('{}: {}'.format(text, self.downloadListWidget.count()))

    def _setVisible(self, visible):
        self.visible = visible
        self.setVisible(visible)

    def startButtonClicked(self):
        self.pauseLock.release()
        self.startButton.setEnabled(False)
        self.pauseButton.setEnabled(True)

    @threaded
    def download_loop(self):
        while not self.__stop:
            time.sleep(1)
            while self.downloadListWidget.count()>0:
                time.sleep(0.5)
                with self.pauseLock:
                    self.showLabels()
                    self.statusLabel.setText('Загружается')
                    item = self.downloadListWidget.takeItem(0)
                    self.titleLabel.setText(item.vkaudio.title())
                    self.artistLabel.setText(item.vkaudio.artist())
                    vkaudio = item.vkaudio
                    self.updateState.emit(vkaudio, 1)
                    try:
                        self.download(vkaudio)
                    except Exception as e:
                        print(e)
                        self.updateState.emit(vkaudio, 3)
                    else:
                        self.updateState.emit(vkaudio, 2)
                    self.updateButton('Ожидают загрузки')
            self.statusLabel.setText('Ожидание')
            self.hideLabels()

    def download(self, vkaudio):
        self.__setDownloadBarValue.emit(0)
        def reportHook(transfered, block_size, total_size):
            self.__setDownloadBarValue.emit(round(((transfered*block_size)/total_size)*100))
        self.parent.api.download(
            vkaudio.url(),
            os.path.join(
                self.uploaddir,
                util.getValidFilename(
                    '{} - {}'.format(vkaudio.artist(),
                                     vkaudio.title())+'.mp3')
            ),
            reportHook)
        self.__setDownloadBarValue.emit(100)

    def pauseButtonClicked(self):
        self.pauseLock.acquire()
        self.startButton.setEnabled(True)
        self.pauseButton.setEnabled(False)
