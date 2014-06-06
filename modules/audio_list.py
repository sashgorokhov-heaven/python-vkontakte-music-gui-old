__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PySide import QtCore, QtGui
import threading
from modules import util
from modules.forms.ui.audiowidget import Ui_Form

STATES = {0:'Ожидает загрузки', 1:'Загружается', 2:'Загружено', 3:'Ошибка', 4:'Отмена'}


class AudioListWidgetItem(QtGui.QWidget, Ui_Form):
    def __init__(self, vkobject, parent, parentitem):
        super().__init__()
        self.setupUi(self)
        self.vkaudio = util.VkAudio(vkobject)
        self.parent = parent
        self.item = parentitem
        self.choosed = False

        self.item.setSizeHint(self.sizeHint())
        self.titleLabel.setText(str(self.vkaudio.title()))
        self.artistLabel.setText(str(self.vkaudio.artist()))
        self.durationLabel.setText('{}:{}'.format(*self.vkaudio.duration(True)))
        self.playLabel.setText('0:00')

        self.owner_id = self.parent.current_id
        self.vkaudio.owner_id = self.owner_id

        if self.vkaudio.id() in self.parent.choosed[self.owner_id]:
            self.parent.choosed[self.owner_id][self.vkaudio.id()] = \
                (self.parent.choosed[self.owner_id][self.vkaudio.id()][0], self)
            self.updateState(self.parent.choosed[self.owner_id][self.vkaudio.id()][0])

    def __setChoose(self, state):
        self.choosed = state
        self.setEnabled(not state)

    def choose(self):
        self.__setChoose(True)

    def unchoose(self):
        self.__setChoose(False)

    def doubleClicked(self):
        self.choose()
        self.parent.choosed[self.parent.current_id][self.vkaudio.id()] = (0, self)
        self.parent.itemChoosed.emit(self.vkaudio)

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked()

    def updateState(self, state_n):
        if state_n>=2:
            self.unchoose()
        self.stateLabel.setText(STATES[state_n])

class AudioListWidget(QtCore.QObject):
    itemChoosed = QtCore.Signal(util.VkAudio)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.__stop = False
        self.worklock = threading.Lock()
        self.choosed = dict() # user_id -> audio_id -> (state, widget)
        self.current_id = None

    @QtCore.Slot()
    def exiting(self):
        self.__stop = True

    @QtCore.Slot(util.VkAudio, int)
    def updateState(self, vkaudio, state_n):
        state, widget = self.choosed[vkaudio.owner_id][vkaudio.id()]
        if widget:
            widget.updateState(state_n)
        self.choosed[vkaudio.owner_id][vkaudio.id()] = (state_n, widget)

    @QtCore.Slot()
    def load_audio(self, owner_id):
        self.__stop = True
        with self.worklock:
            self.__stop = False
            if owner_id not in self.choosed:
                self.choosed[owner_id] = dict()
            if self.current_id:
                for key in self.choosed[self.current_id]:
                    self.choosed[self.current_id][key] = \
                        (self.choosed[self.current_id][key][0], None)
            self.current_id = owner_id
            self.parent.audioList.clear()
            self.parent.countLabel.setText('0')
            self.__list_filler = util.LoadThread(self.__fill_list)
            self.__list_filler.signalEmitter.connect(self.__addAudioItemSlot)
            self.__list_filler.start()

    def __fill_list(self, emitter):
        with self.worklock:
            try:
                audios = self.parent.api.call('audio.get', owner_id=self.current_id)['items']
            except Exception as e:
                if e.error['error_code']==15:
                    self.parent.audioList.addItem(
                        QtGui.QListWidgetItem('Аудиозаписи в группе отключены.'))
                if e.error['error_code']==201:
                    self.parent.audioList.addItem(
                        QtGui.QListWidgetItem('Пользователь скрыл свои драгоценные аудиозаписи.'))
                return
            self.parent.countLabel.setText(str(len(audios)))
            if len(audios)==0:
                self.parent.audioList.addItem(
                    QtGui.QListWidgetItem('Аудиозаписей нет.'))
            for vkobject in audios:
                if self.__stop:
                    return
                emitter.emit(vkobject, 0, 0)
                QtCore.QThread.msleep(60)

    @QtCore.Slot(dict, int, int)
    def __addAudioItemSlot(self, vkobject, n, p):
        if self.__stop:
            return
        try:
            item = QtGui.QListWidgetItem()
            widget = AudioListWidgetItem(vkobject, self, item)
            self.parent.audioList.addItem(item)
            self.parent.audioList.setItemWidget(item, widget)
        except Exception as e:
            self.parent.audioList.addItem(QtGui.QListWidgetItem('Ошибка создания объекта аудиозаписи: {}'.format(e)))