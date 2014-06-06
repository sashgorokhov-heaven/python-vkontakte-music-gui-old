__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

import threading
from modules import util
from modules.gorokhovlibs.threadeddecor import threaded
import time
from PySide import QtGui, QtCore
from modules.forms.ui.loadform import Ui_Form as UI_DownloadWidget
from modules.forms.ui.audiodownloadwidget import Ui_Form as UI_DownloadWidgetItem


class AudioDownloadWidgetItem(QtGui.QWidget, UI_DownloadWidgetItem):
    def __init__(self, vkaudio, parent, item):
        super().__init__()
        self.vkaudio = vkaudio
        self.parent = parent
        self.item = item
        self.setupUi(self)
        self.item.setSizeHint(self.sizeHint())
        self.titleLabel.setText(vkaudio.title())
        self.artistLabel.setText(vkaudio.artist())

    def doubleClicked(self):
        self.parent.updateState.emit(self.vkaudio, 4)
        self.parent.downloadListWidget.takeItem(self.parent.downloadListWidget.row(self.item))

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked()

class AudioDownloadWidget(QtGui.QWidget, UI_DownloadWidget):
    updateState = QtCore.Signal(util.VkAudio, int)

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
        self.hide()
        self.download_loop()
        self.hideLabels()
        self.statusLabel.setText('Ожидание')
        self.startButton.clicked.connect(self.startButtonClicked)
        self.pauseButton.clicked.connect(self.pauseButtonClicked)

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
        self.hide()

    @QtCore.Slot()
    def exiting(self):
        self.__stop = True

    @QtCore.Slot()
    def show(self):
        self._setVisible(True)

    @QtCore.Slot()
    def hide(self):
        self._setVisible(False)

    @QtCore.Slot(util.VkAudio)
    def add(self, vkaudio):
        item = QtGui.QListWidgetItem()
        widget = AudioDownloadWidgetItem(vkaudio, self, item)
        self.downloadListWidget.addItem(item)
        self.downloadListWidget.setItemWidget(item, widget)
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
                    item = self.downloadListWidget.item(0)
                    widget = self.downloadListWidget.itemWidget(item)
                    self.titleLabel.setText(widget.vkaudio.title())
                    self.artistLabel.setText(widget.vkaudio.artist())
                    vkaudio = widget.vkaudio
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
        self.parent.api.download(vkaudio.url(),str(vkaudio.id())+'.mp3')

    def pauseButtonClicked(self):
        self.pauseLock.acquire()
        self.elements.startButton.setEnabled(True)
        self.elements.pauseButton.setEnabled(False)
