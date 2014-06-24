import os
import sys
import threading
from modules import util
from modules.forms.downloadform.components.audiolist.components.audiolistitemwidget import AudioDownloadWidgetItem
from modules.util import VkAudio, ThreadedWorker
from .ui import Ui_Form
from PySide import QtCore, QtGui
from modules.vk.api import VKApi

MAXDOWNLOADS = 2

class _Downloader(ThreadedWorker):
    # item, vkaudio, set_value, on_complete, upload_dir
    def _workfunc(self):
        item, vkaudio, set_value, on_complete, upload_dir = [self._kwargs[i] for i in ['item', 'vkaudio', 'set_value', 'on_complete', 'upload_dir']]
        set_value.emit(0)
        def reportHook(transfered, block_size, total_size):
            p = round(((transfered*block_size)/total_size)*100)
            set_value.emit(p)
            vkaudio.set_state('loading', p)
        try:
            VKApi.download(
                None,
                vkaudio.url(),
                os.path.join(
                    upload_dir,
                    util.getValidFilename(
                        '{} - {}'.format(vkaudio.artist(),
                                         vkaudio.title())+'.mp3')
                ),
                reportHook)
            set_value.emit(100)
        except Exception as e:
            on_complete.emit(item, -1, str(e))
        else:
            on_complete.emit(item, 0, '')

class _DownloaderFacade(QtCore.QObject):
    _exiting_signal = QtCore.Signal()
    _download_complete_signal = QtCore.Signal(QtGui.QListWidgetItem, int, str)
    def __init__(self, manager):
        super().__init__()
        self._manager = manager
        self._downloading = list() # list of items (QListWidgetItem) of downloadList
        self._download_complete_signal.connect(self._download_complete_slot)
        self._lock = threading.Lock()

    @QtCore.Slot()
    def exiting(self):
        self._exiting_signal.emit()

    @QtCore.Slot(QtGui.QListWidgetItem)
    def audio_added(self, item):
        if len(self._downloading)<MAXDOWNLOADS:
            self._add_download(item)

    def _add_download(self, item):
        widget = self._manager.downloadListWidget.itemWidget(item)
        #assert isinstance(widget, AudioDownloadWidgetItem)
        widget.downloading = True
        downloader = _Downloader(
            set_value=widget.set_value_signal,
            item=item,
            vkaudio=widget.vkaudio,
            on_complete=self._download_complete_signal,
            upload_dir=self._manager._uploaddir)
        self._exiting_signal.connect(downloader.terminate)
        downloader.start()
        with self._lock:
            self._downloading.append((downloader, widget.vkaudio))

    @QtCore.Slot(QtGui.QListWidgetItem, int, str)
    def _download_complete_slot(self, item, code, error_msg):
        widget = self._manager.downloadListWidget.itemWidget(item)
        with self._lock:
            i = -1
            for n, k in enumerate(self._downloading):
                _, vkaudio = k
                if vkaudio.id()==widget.vkaudio.id():
                    i = n
                    break
            _, vkaudio = self._downloading.pop(i)
        if code!=0:
            vkaudio.set_state('error', error_msg)
        else:
            vkaudio.set_state('complete')
        with self._lock:
            self._manager.downloadListWidget.takeItem(self._manager.downloadListWidget.row(item))
            item = None
            if len(self._downloading)<MAXDOWNLOADS and self._manager.downloadListWidget.count()!=0:
                for i in range(self._manager.downloadListWidget.count()):
                    itm = self._manager.downloadListWidget.item(i)
                    widget = self._manager.downloadListWidget.itemWidget(itm)
                    if not widget.downloading:
                        item = itm
                        break
        if item:
            self._add_download(item)


class DownloadManager(QtGui.QWidget, Ui_Form):
    _exiting_signal = QtCore.Signal()
    _updateButton_signal = QtCore.Signal()
    _audio_added = QtCore.Signal(QtGui.QListWidgetItem)
    def __init__(self, mainui):
        super().__init__()
        self.setupUi(self)
        self.mainui = mainui
        self._exiting = False
        self._visible = False
        self._uploaddir = os.path.split(sys.argv[0])[0]
        self._firstshow = True
        self._pauseLock = threading.Lock()
        self._pauseLock.acquire()
        self._updateButton_signal.connect(self._updateButton)
        self.startButton.clicked.connect(self.startButtonClicked)
        self.pauseButton.clicked.connect(self.pauseButtonClicked)
        self.hide()
        self._start_downloader()

    @QtCore.Slot(VkAudio)
    def add_audio(self, vkaudio):
        item = QtGui.QListWidgetItem()
        widget = AudioDownloadWidgetItem(vkaudio, self, item)
        self.downloadListWidget.addItem(item)
        self.downloadListWidget.setItemWidget(item, widget)
        self._updateButton_signal.emit()
        self._audio_added.emit(item)

    def _start_downloader(self):
        self._downloader_facade = _DownloaderFacade(self)
        self._exiting_signal.connect(self._downloader_facade.exiting)
        self._audio_added.connect(self._downloader_facade.audio_added)

    @QtCore.Slot()
    def _updateButton(self):
        self.mainui.downloadButton.setText('Ожидают загрузки: {}'.format(self.downloadListWidget.count()))

    @QtCore.Slot()
    def exiting(self):
        self._exiting = True
        self._exiting_signal.emit()
        self.close()

    def _setVisible(self, visible):
        self._visible = visible
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

    def startButtonClicked(self):
        self._pauseLock.release()
        self.startButton.setEnabled(False)
        self.pauseButton.setEnabled(True)

    def pauseButtonClicked(self):
        self._pauseLock.acquire()
        self.startButton.setEnabled(True)
        self.pauseButton.setEnabled(False)
