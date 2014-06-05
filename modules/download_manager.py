__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

import threading
from modules import util
from modules.gorokhovlibs.threadeddecor import threaded
import time
from modules.gorokhovlibs.qt import qtwindow
import os.path
from PyQt4 import QtGui, QtCore, uic


class AudioDownloadWidgetItem(QtGui.QWidget):
    def __init__(self, vkaudio, parent, item):
        self.vkaudio = vkaudio
        self.parent = parent
        self.item = item
        super().__init__()
        uic.loadUi(os.path.join('resourses', 'audiodownloadwidget.ui'), self)
        self.item.setSizeHint(self.sizeHint())
        setattr(self, 'elements', qtwindow._Elements(qtwindow.BaseQtWindow._set_childs(None, self)))
        self.elements.titleLabel.setText(vkaudio.title())
        self.elements.artistLabel.setText(vkaudio.artist())

    def doubleClicked(self):
        self.emit(QtCore.SIGNAL('updateState(int, int)'), self.vkaudio.id(), 4)
        self.parent.elements.downloadListWidget.takeItem(self.parent.elements.downloadListWidget.row(self.item))

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked()

class AudioDownloadWidget(qtwindow.BaseQtWindow):
    def __init__(self, parent):
        super().__init__(self, os.path.join('resourses', 'loadform.ui'))
        self.parent = parent
        self.stop = False
        self.loading = False
        self.audiolist = list()
        self.pauseLock = threading.Lock()
        self.pauseLock.acquire()
        self.worklock1 = threading.Lock()
        self.worklock2 = threading.Lock()
        self.hide()
        self.download_loop()
        self.hideLabels()
        self.elements.statusLabel.setText('Ожидание')

    def hideLabels(self):
        self.elements.titleLabel.setVisible(False)
        self.elements.sepLabel.setVisible(False)
        self.elements.artistLabel.setVisible(False)

    def showLabels(self):
        self.elements.titleLabel.setVisible(True)
        self.elements.sepLabel.setVisible(True)
        self.elements.artistLabel.setVisible(True)

    def closeEvent(self, event):
        self.hide()

    def close(self):
        self.stop = True

    def show(self):
        self._setVisible(True)

    def hide(self):
        self._setVisible(False)

    def add(self, aid):
        vkaudio = self.parent.buffer.remove(aid)
        assert isinstance(vkaudio, util.VkAudio)
        item = QtGui.QListWidgetItem()
        widget = AudioDownloadWidgetItem(vkaudio, self, item)
        self.elements.downloadListWidget.addItem(item)
        self.elements.downloadListWidget.setItemWidget(item, widget)
        self.updateButton('Ожидают загрузки')

    def updateButton(self, text):
        self.parent.elements.downloadButton.setText('{}: {}'.format(text, self.downloadListWidget.count()))

    def _setVisible(self, visible):
        self.visible = visible
        self.setVisible(visible)

    def _set_connections(self):
        self.elements.startButton.clicked.connect(self.startButtonClicked)
        self.elements.pauseButton.clicked.connect(self.pauseButtonClicked)
        self.connect(self, QtCore.SIGNAL('work()'), self.__work)

    def startButtonClicked(self):
        self.pauseLock.release()
        self.elements.startButton.setEnabled(False)
        self.elements.pauseButton.setEnabled(True)

    @threaded
    def download_loop(self):
        while not self.stop:
            time.sleep(1)
            while self.elements.downloadListWidget.count()>0:
                time.sleep(0.5)
                with self.pauseLock:
                    self.showLabels()
                    self.elements.statusLabel.setText('Загружается')
                    vkaudio = self.getVkaudio()
                    self.emit(QtCore.SIGNAL('updateState(int, int)'), vkaudio.id(), 1)
                    try:
                        self.download(vkaudio)
                    except Exception as e:
                        print(e)
                        self.emit(QtCore.SIGNAL('updateState(int, int)'), vkaudio.id(), 3)
                    #widget.doubleClicked()
                    else:
                        self.emit(QtCore.SIGNAL('updateState(int, int)'), vkaudio.id(), 2)
                    self.updateButton('Ожидают загрузки')
            self.elements.statusLabel.setText('Ожидание')
            self.hideLabels()

    def __work(self):
        with self.worklock2:
            item = self.elements.downloadListWidget.takeItem(0)
            widget = self.elements.downloadListWidget.itemWidget(item)
            self.elements.titleLabel.setText(widget.vkaudio.title())
            self.elements.artistLabel.setText(widget.vkaudio.artist())
            self.parent.buffer.put('object', widget.vkaudio)

    def getVkaudio(self):
        self.emit(QtCore.SIGNAL('work()'))
        time.sleep(1)

        self.worklock2.acquire()
        self.worklock2.release()

        return self.parent.buffer.remove('object')




    def download(self, vkaudio):
        self.parent.api.download(vkaudio.url(),str(vkaudio.id())+'.mp3')

    def pauseButtonClicked(self):
        self.pauseLock.acquire()
        self.elements.startButton.setEnabled(True)
        self.elements.pauseButton.setEnabled(False)
        pass
