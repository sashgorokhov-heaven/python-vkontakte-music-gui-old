__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PyQt4 import QtCore, QtGui, uic
import threading, os.path, time
from modules.gorokhovlibs.qt import qtwindow
from modules.gorokhovlibs.threadeddecor import threaded
from modules import util

STATES = {0:'Ожидает загрузки', 1:'Загружается', 2:'Загружено', 3:'Ошибка', 4:'Отмена'}


class AudioListWidgetItem(QtGui.QWidget):
    def __init__(self, vkobject, parent, parentitem):
        super().__init__()
        uic.loadUi(os.path.join('resourses', 'audiowidget.ui'), self)
        setattr(self, 'elements', qtwindow._Elements(qtwindow.BaseQtWindow._set_childs(None, self)))

        self.vkaudio = util.VkAudio(vkobject)
        self.parent = parent
        self.item = parentitem
        self.choosed = False

        self.item.setSizeHint(self.sizeHint())
        self.elements.titleLabel.setText(str(self.vkaudio.title()))
        self.elements.artistLabel.setText(str(self.vkaudio.artist()))
        self.elements.durationLabel.setText('{}:{}'.format(*self.vkaudio.duration(True)))
        self.elements.playLabel.setText('0:00')

        if self.vkaudio.id() in self.parent.choosed[self.parent.current_id]:
            self.parent.choosed[self.parent.current_id][self.vkaudio.id()] = \
                (self.parent.choosed[self.parent.current_id][self.vkaudio.id()][0], self)
            self.updateState(self.parent.choosed[self.parent.current_id][self.vkaudio.id()][0])

    def __setChoose(self, state):
        self.choosed = state
        self.setEnabled(not state)

    def choose(self):
        self.__setChoose(True)

    def unchoose(self):
        self.__setChoose(False)

    def doubleClicked(self):
        self.choose()
        self.parent.parent.buffer.put(self.vkaudio.id(), self.vkaudio)
        self.parent.choosed[self.parent.current_id][self.vkaudio.id()] = (0, self)
        self.parent.emit(QtCore.SIGNAL('itemChoosed(int)'), self.vkaudio.id())

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked()

    def updateState(self, state_n):
        if state_n>=2:
            self.unchoose()
        self.elements.stateLabel.setText(STATES[state_n])


#emits | itemChoosed(int)
#listents | menuItemClicked(int) | from NavigationMenu
#listens | updateState(int, int) | from DownloadManager
class AudioListWidget(QtCore.QObject):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.stop = False
        self.worklock = threading.Lock()
        self.choosed = dict() # user_id -> audio_id -> (state, widget)
        self.connect(self, QtCore.SIGNAL('addAudioItem(int)'), self.__addAudioItem)
        self.current_id = None

    def close(self):
        self.stop = True

    def updateState(self, aid, state_n):
        pass

    def load_audio(self, owner_id):
        self.stop = True
        with self.worklock:
            self.stop = False
            if owner_id not in self.choosed:
                self.choosed[owner_id] = dict()
            if self.current_id:
                for key in self.choosed[self.current_id]:
                    self.choosed[self.current_id][key] = \
                        (self.choosed[self.current_id][key][0], None)
            self.current_id = owner_id
            self.parent.elements.audioList.clear()
            self.parent.elements.countLabel.setText('0')
            try:
                audios = self.parent.api.call('audio.get', owner_id=owner_id)['items']
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
                self.parent.elements.countLabel.setText(str(len(audios)))
                self.__fill_list(audios)

    @threaded
    def __fill_list(self, audios):
        with self.worklock:
            for vkobject in audios:
                if self.stop:
                    return
                self.parent.buffer.put(vkobject['id'], vkobject)
                self.addAudioItem(vkobject['id'])
                time.sleep(0.06)

    def __addAudioItem(self, aid):
        if self.stop:
            return
        try:
            vkaudio = self.parent.buffer.remove(aid)
            item = QtGui.QListWidgetItem()
            widget = AudioListWidgetItem(vkaudio, self, item)
            self.parent.elements.audioList.addItem(item)
            self.parent.elements.audioList.setItemWidget(item, widget)
        except Exception as e:
            self.parent.elements.audioList.addItem(QtGui.QListWidgetItem('Ошибка создания объекта аудиозаписи: {}'.format(e)))

    def addAudioItem(self, n):
        self.emit(QtCore.SIGNAL('addAudioItem(int)'), int(n))