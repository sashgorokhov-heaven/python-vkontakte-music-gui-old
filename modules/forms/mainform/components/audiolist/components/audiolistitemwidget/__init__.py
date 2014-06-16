__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PySide import QtCore, QtGui
from .ui import Ui_Form
from modules.util import VkAudio

playicon = QtGui.QPixmap(QtGui.QIcon(":/newFlatIcons/Icons/Button-Play-icon.png"))
pauseicon = QtGui.QPixmap(QtGui.QIcon(":/newFlatIcons/Icons/Button-Pause-icon.png"))

class AudioListItemWidget(QtGui.QWidget, Ui_Form):
    play_signal = QtCore.Signal(VkAudio)
    pause_signal = QtCore.Signal(VkAudio)
    def __init__(self, vkaudio: VkAudio):
        super().__init__()
        self._vkaudio = vkaudio
        self.setupUi(self)
        self._vkaudio.set_current_widget(self)
        self.artistLabel.setText(vkaudio.artist())
        self.titleLabel.setText(vkaudio.title())
        self.__getattribute__('state_'+self._vkaudio.get_state())()

    def _set_iconlabel(self, playing:bool):
        self.playpauseLabel.setPixmap(playicon if playing else pauseicon)

    def play(self):
        self._set_iconlabel(False)
        self.play_signal.emit(self._vkaudio)

    def pause(self):
        self._set_iconlabel(False)
        self.pause_signal.emit(self._vkaudio)

    def state_idle(self):
        self.stateLabel.setText('')
        self._state = 'idle'

    def state_waiting(self):
        self.stateLabel.setText('Ожидание')
        self._state = 'waiting'

    def state_loading(self, p:int=None):
        self.stateLabel.setText('Загрузка {}%'.format(p) if p else 'Загрузка')
        self._state = 'loading'

    def state_complete(self):
        self.stateLabel.setText('Загружено')
        self._state = 'complete'

    def state_error(self, e:Exception=None):
        self.stateLabel.setText('Ошибка {}'.format(e) if e else 'Ошибка')
        self._state = 'error'

    def __del__(self):
        self._vkaudio.set_current_widget(None)