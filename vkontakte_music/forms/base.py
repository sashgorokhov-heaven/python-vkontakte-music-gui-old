from PySide import QtGui, QtCore

from vkontakte_music import settings


class BaseForm(QtGui.QWidget):
    on_exit = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'setupUi'):
            self.setupUi(self)
        self._threads = list()
        self.setWindowTitle(settings.WINDOW_TITLE)

    def closeEvent(self, event):
        self.on_exit.emit()
        event.accept()

    def run_thread(self, thread):
        """
        :param vkontakte_music.utils.multithreading.BaseThread thread:
        """
        self._threads.append(thread)
        self.on_exit.connect(thread.on_exit)
        thread.start()
