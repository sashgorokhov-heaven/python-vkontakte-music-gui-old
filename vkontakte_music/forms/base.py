from PySide import QtGui, QtCore

from vkontakte_music import settings
from vkontakte_music.utils.multithreading import ThreadRunnerMixin


class BaseForm(QtGui.QWidget, ThreadRunnerMixin):
    on_exit = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'setupUi'):
            self.setupUi(self)
        self.setWindowTitle(settings.WINDOW_TITLE)

    def closeEvent(self, event):
        self.on_exit.emit()
        event.accept()
