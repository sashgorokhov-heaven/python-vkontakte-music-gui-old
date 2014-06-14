__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

import threading
from PySide import QtCore
from modules.gorokhovlibs.threadeddecor import threaded

class Dispatcher(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.__queque = List()
        self.__lock = threading.Lock()
        self.__stop = False
        self.worker()

    def addTask(self, runFunc, data, slot):
        with self.__lock:
            self.__queque.append((runFunc, data, slot))

    @QtCore.Slot()
    def close(self):
        self.__stop = True

    @QtCore.Slot(tuple)
    def __execute(self, tpl):
        runFunc, data = tpl

    @threaded
    def worker(self):
        while not self.__stop:
            while len(self.__queque)>0:
                with self.__lock:
                    pass