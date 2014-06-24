from modules.util import Dispatcher, VkAudio
from modules.vk.api import VKError

__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PySide import QtCore, QtGui
from modules import util
from modules.forms.mainform.components.audiolist.components.audiolistitemwidget import AudioListItemWidget
import threading

class _AudioListWorker(util.ThreadedWorker):
    def _workfunc(self):
        self._kwargs['set_countlabel'].emit('0')
        try:
            audiolist_vkobject = self._kwargs['api'].call('audio.get', owner_id=self._kwargs['uid'])['items']
        except VKError as e:
            if e.error_code==15:
                self._kwargs['addaudio_error_signal'].emit('Аудиозаписи в группе отключены.')
            if e.error_code==201:
                self._kwargs['addaudio_error_signal'].emit('Пользователь скрыл свои драгоценные аудиозаписи.')
            return
        self._kwargs['set_countlabel'].emit(str(len(audiolist_vkobject)))
        if len(audiolist_vkobject) == 0:
            self._kwargs['addaudio_error_signal'].emit('Аудиозаписей нет.')
        for audio_vkobject in audiolist_vkobject:
            self._kwargs['addaudio_signal'].emit(audio_vkobject)

class AudioList(QtCore.QObject):
    _exiting_signal = QtCore.Signal()
    _addaudio_error_signal = QtCore.Signal(str)
    _set_countlabel_signal = QtCore.Signal(str)
    _addaudio_signal = QtCore.Signal(dict)
    _kill_workerthread = QtCore.Signal()
    item_choosed = QtCore.Signal(VkAudio)
    def __init__(self, parentform_ui, api):
        super().__init__()
        self.ui = parentform_ui
        self._api = api
        self.ui.downloadSelectedButton.setVisible(False)
        self.ui.audioList.itemSelectionChanged.connect( # :)
            QtCore.Slot()( # :)
                lambda : # :)
                (self.ui.downloadSelectedButton.setVisible(len(self.ui.audioList.selectedItems())!=0), # :)
                 self.ui.downloadSelectedButton.setText('Загрузить выбранное ({})'.format(len(self.ui.audioList.selectedItems())))) # :)
            ) # :)
        ) # :)
        self.ui.downloadSelectedButton.clicked.connect(self.downloadSelectedButton_clicked)
        self._exiting = False
        self._dispatcher = Dispatcher()
        self._dispatcher.start()
        self._exiting_signal.connect(self._dispatcher.terminate)
        self._worklock = threading.Lock()
        self._current_uid = None

        self._vkaudio_pool = dict() # aid -> VKAudio

        self._addaudio_error_signal.connect(self._addaudio_error_slot)
        self._set_countlabel_signal.connect(self._set_countlabel_slot)
        self._addaudio_signal.connect(self._addaudio_slot)

    @QtCore.Slot()
    def downloadSelectedButton_clicked(self):
        for item in self.ui.audioList.selectedItems():
            widget = self.ui.audioList.itemWidget(item)
            if widget:
                widget.double_clicked()

    @QtCore.Slot()
    def exiting(self):
        self._exiting = True
        self._exiting_signal.emit()

    def get_current_uid(self):
        return self._current_uid

    @QtCore.Slot(int)
    def load_audio(self, uid:int):
        self._kill_workerthread.emit()
        self._dispatcher.clear_queque()
        with self._worklock:
            self.current_uid = uid
            for i in range(self.ui.audioList.count()):
                item = self.ui.audioList.item(i)
                widget = self.ui.audioList.itemWidget(item)
                if widget:
                    widget._vkaudio.set_current_widget(None)
            self.ui.audioList.clear()
            self._worker_thread = _AudioListWorker(api=self._api, uid=uid,
                                                   addaudio_error_signal=self._addaudio_error_signal,
                                                   set_countlabel=self._set_countlabel_signal,
                                                   addaudio_signal=self._addaudio_signal)
            self._worker_thread.finished.connect(self._work_complete)
            self._kill_workerthread.connect(self._worker_thread.terminate)
            self._exiting_signal.connect(self._worker_thread.terminate)
            self._worker_thread.start()

    @QtCore.Slot()
    def _work_complete(self):
        pass

    @QtCore.Slot(str)
    def _addaudio_error_slot(self, msg):
        self.ui.audioList.addItem(QtGui.QListWidgetItem(str(msg)))

    @QtCore.Slot(str)
    def _set_countlabel_slot(self, msg):
        self.ui.countLabel.setText(msg)

    @QtCore.Slot(dict)
    def _addaudio_slot(self, audio_vkobject):
        if audio_vkobject['id'] not in self._vkaudio_pool:
            self._vkaudio_pool[audio_vkobject['id']] = util.VkAudio(audio_vkobject)
        vkaudio = self._vkaudio_pool[audio_vkobject['id']]
        self._dispatcher.addTask(AudioList._addaudio_guiwork, (self, vkaudio))

    @staticmethod
    def _addaudio_guiwork(self, vkaudio):
        try:
            if vkaudio.get_owner()!=self._current_uid:
                return
            item = QtGui.QListWidgetItem()
            widget = AudioListItemWidget(vkaudio)
            self.ui.audioList.addItem(item)
            self.ui.audioList.setItemWidget(item, widget)
            widget.double_clicked_signal.connect(self._item_choosed)
        except Exception as e:
            self.ui.audioList.addItem(QtGui.QListWidgetItem('Ошибка создания объекта аудиозаписи: {}'.format(e)))

    @QtCore.Slot(VkAudio)
    def _item_choosed(self, vkaudio):
        self.item_choosed.emit(vkaudio)