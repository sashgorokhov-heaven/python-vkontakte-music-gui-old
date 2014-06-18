import os
import sys
import threading
import time
from modules.forms.downloadform.components.audiolist.components.audiolistitemwidget import AudioDownloadWidgetItem
from modules.util import VkAudio, ThreadedWorker
from .ui import Ui_Form
from PySide import QtCore, QtGui

class _Downloader(ThreadedWorker):
    def _workfunc(self):
        while not self._kwargs['manager']._exiting:
            time.sleep(1)
            while self._kwargs['manager'].downloadListWidget.count()>0:
                with self._kwargs['manager'].pauseLock:
                    self._kwargs['manager']._showLabels()
                    # TODO
            self._kwargs['manager']._hideLabels()

class DownloadManager(QtGui.QWidget, Ui_Form):
    _exiting_signal = QtCore.Signal()
    _updateButton_signal = QtCore.Signal()
    def __init__(self, mainui):
        super().__init__()
        self.setupUi(self)
        self.mainui = mainui
        self._exiting = False
        self.visible = False
        self._uploaddir = os.path.split(sys.argv[0])[0]
        self._firstshow = True
        self._pauseLock = threading.Lock()
        self._pauseLock.acquire()
        self._updateButton_signal.connect(self._updateButton)
        self.startButton.clicked.connect(self.startButtonClicked)
        self.pauseButton.clicked.connect(self.pauseButtonClicked)
        self.hide()

    @QtCore.Slot(VkAudio)
    def add_audio(self, vkaudio):
        item = QtGui.QListWidgetItem()
        widget = AudioDownloadWidgetItem(vkaudio, self, item)
        self.downloadListWidget.addItem(item)
        self.downloadListWidget.setItemWidget(item, widget)
        self._updateButton_signal.emit()

    @QtCore.Slot()
    def _updateButton(self):
        self.mainui.downloadButton.setText('Ожидают загрузки: {}'.format(self.downloadListWidget.count()))

    @QtCore.Slot()
    def exiting(self):
        self._exiting = True
        self._exiting_signal.emit()
        self.close()

    def _setVisible(self, visible):
        self.visible = visible
        self.setVisible(visible)

    def hide(self):
        self._setVisible(False)

    def show(self):
        if self._firstshow:
            ndir = QtGui.QFileDialog.getExistingDirectory(self, 'Папка для загрузки', self._uploaddir, QtGui.QFileDialog.ShowDirsOnly)
            if ndir:
                self._uploaddir = ndir
            self._firstshow= False
        self._setVisible(True)

    def _showLabels(self):
        self.titleLabel.setVisible(True)
        self.sepLabel.setVisible(True)
        self.artistLabel.setVisible(True)

    @QtCore.Slot()
    def _hideLabels(self):
        self.titleLabel.setVisible(False)
        self.sepLabel.setVisible(False)
        self.artistLabel.setVisible(False)

    def startButtonClicked(self):
        self._pauseLock.release()
        self.startButton.setEnabled(False)
        self.pauseButton.setEnabled(True)

    def pauseButtonClicked(self):
        self._pauseLock.acquire()
        self.startButton.setEnabled(True)
        self.pauseButton.setEnabled(False)
