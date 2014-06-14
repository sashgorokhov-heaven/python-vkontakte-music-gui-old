__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

import threading, random
from PySide import QtCore

class Dispatcher(QtCore.QThread):
    _take_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self._queque = list()
        self._lock = threading.Lock()
        self._continue_lock = threading.Lock()
        self._IDs = set()
        self._worksleep = 150
        self._results = dict() # ID -> result
        self._take_signal.connect(self._take)
        self._condition = threading.Condition()

    def addTask(self, run_func, data=None, ID:int=None):
        with self._lock:
            self._queque.append((run_func, data, ID))

    @QtCore.Slot()
    def _take(self):
        with self._lock:
            run_func, data, ID = self._queque.pop()
            if ID is not None:
                self._results[ID] = run_func(data) if data is not None else run_func()
            else:
                _ = run_func(data) if data is not None else run_func()
            self._condition.acquire()
            self._condition.notify()
            self._condition.release()

    def run(self):
        while True:
            self.msleep(100)
            while len(self._queque)>0:
                self.msleep(self._worksleep)
                self._take_signal.emit()
                self._condition.acquire()
                self._condition.wait()
                self._condition.release()

    def getID(self) -> int:
        while True:
            ID = random.randint(0, 1024)
            if ID in self._IDs:
                continue
            self._IDs.add(ID)
            return ID

    def get_result(self, ID:int):
        self._IDs.pop(ID)
        return self._results.pop(ID)