__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PyQt4 import QtCore, QtGui, uic
import threading, os.path, time
from modules.gorokhovlibs.qt import qtwindow
from modules.gorokhovlibs.threadeddecor import threaded

class AudioListWidgetItem(QtGui.QWidget):
    def __init__(self, oobject, parent, parentitem):
        self.object = oobject
        self.parent = parent
        self.item = parentitem
        self.checked = False
        super().__init__()
        uic.loadUi(os.path.join('resourses', 'audiowidget.ui'), self)

        self.item.setSizeHint(self.sizeHint())

        setattr(self, 'elements', qtwindow._Elements(qtwindow.BaseQtWindow._set_childs(None, self)))

        self.elements.titleLabel.setText(str(oobject['title']))
        self.elements.artistLabel.setText(str(oobject['artist']))

        mins = (oobject['duration'] // 60)
        secs = oobject['duration']-60*(oobject['duration'] // 60)
        self.elements.durationLabel.setText(str(mins)+':'+'0'*(2-len(str(secs)))+str(secs))
        self.elements.playLabel.setText('0:00')

        self.elements.checkBox.setVisible(False)

    def check(self):
        self.elements.checkBox.setCheckState(2)
        self.checked = True

    def uncheck(self):
        self.elements.checkBox.setCheckState(0)
        self.checked = False

    def doubleClicked(self):
        self.setEnabled(False)
        self.parent.parent.downloadAudio(self.object)

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked()

class AudioListWidget(QtCore.QObject):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.stop = False
        self.worklock = threading.Lock()
        self.current_id = None
        self.current_audiolist = list()
        self.connect(self, QtCore.SIGNAL('addAudioItem(int)'), self.__addAudioItem)

    def close(self):
        self.stop = True

    def load_audio(self, id):
        self.stop = True
        with self.worklock:
            self.stop = False
            self.parent.elements.audioList.clear()
            self.current_audiolist = list()
            self.current_id = id
            self.parent.elements.countLabel.setText('0')
            try:
                audios = self.parent.api.call('audio.get', owner_id=id)['items']
            except Exception as e:
                if e.error['error_code']==15:
                    self.parent.elements.audioList.addItem(
                        QtGui.QListWidgetItem('Аудиозаписи в группе отключены.'))
                if e.error['error_code']==201:
                    self.parent.elements.audioList.addItem(
                        QtGui.QListWidgetItem('Пользователь скрыл свои драгоценные аудиозаписи.'))
            else:
                if len(audios)==0:
                    self.parent.elements.audioList.addItem(
                        QtGui.QListWidgetItem('Аудиозаписей нет.'))
                    return
                self.fill_list(audios)

    @threaded
    def fill_list(self, audios):
        with self.worklock:
            self.parent.elements.countLabel.setText(str(len(audios)))
            self.current_audiolist = audios
            for n, audio in enumerate(audios):
                if self.stop:
                    return
                self.addAudioItem(n)
                time.sleep(0.05)

    def __addAudioItem(self, n):
        if self.stop:
            return
        try:
            audio = self.current_audiolist[n]
            item = QtGui.QListWidgetItem()
            widget = AudioListWidgetItem(audio, self, item)
            self.parent.elements.audioList.addItem(item)
            self.parent.elements.audioList.setItemWidget(item, widget)
        except:
            return

    def addAudioItem(self, n):
        self.emit(QtCore.SIGNAL('addAudioItem(int)'), int(n))

    def checkAll(self):
        n = self.parent.elements.audioList.count()
        for i in range(n):
            item = self.parent.elements.audioList.item(i)
            widget = self.parent.elements.audioList.itemWidget(item)
            widget.check()

    def uncheckAll(self):
        n = self.parent.elements.audioList.count()
        for i in range(n):
            item = self.parent.elements.audioList.item(i)
            widget = self.parent.elements.audioList.itemWidget(item)
            widget.uncheck()