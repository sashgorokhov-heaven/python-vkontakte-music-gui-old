__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PySide import QtCore, QtGui


class __Form(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.__close = False

    def _close(self):
        self.__close = True

    def closeEvent(self, event):
        if self.__close:
            event.accept()

__form = __Form()


def show():
    __form.show()


def hide():
    __form.hide()


def close():
    __form._close()
    __form.close()