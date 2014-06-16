import random
from PySide import QtCore

__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

import threading, re

def showmessage(msg):
    print(str(msg))

def getValidFilename(filename):
    regexp = re.compile(r"[0-9a-zA-ZА-Яа-я\-\(\)\.\' ]")
    return ''.join(i for i in filename if re.match(regexp, i))[:100]

class VkAudio:
    def __init__(self, audioobject):
        self.__object = audioobject
        self.owner_id = None

    def id(self):
        return self.__object['id']

    def getObject(self):
        return self.__object

    def artist(self):
        return self.__object['artist']

    def title(self):
        return self.__object['title']

    def url(self):
        return self.__object['url']

    def duration(self, parsed=False):
        if parsed:
            mins = (self.__object['duration'] // 60)
            secs = self.__object['duration']-60*(self.__object['duration'] // 60)
            return (mins, secs)
        return self.__object['duration']

    def __getattr__(self, item):
        return self.__object[item]

    def __str__(self):
        return '[{0}] {} - {}'.format(':'.join(self.duration(True)), self.artist(), self.title())


class ThreadedWorker(QtCore.QThread):
    def __init__(self, **kwargs):
        super().__init__()
        self._result = None
        self._lock = threading.Lock()
        self._kwargs = kwargs

    def run(self):
        with self._lock:
            self._result = self._workfunc()

    def _workfunc(self):
        raise NotImplementedError

    def get_result(self):
        with self._lock:
            return self._result


class Dispatcher(QtCore.QThread):
    _take_signal = QtCore.Signal()

    def __init__(self, worksleep=0):
        super().__init__()
        self._queque = list()
        self._lock = threading.Lock()
        self._continue_lock = threading.Lock()
        self._IDs = set()
        self._worksleep = worksleep
        self._results = dict() # ID -> result
        self._take_signal.connect(self._take)
        self._condition = threading.Condition()
        self._wait_condition = threading.Condition()

    def addTask(self, run_func, data=None, ID:int=None):
        with self._lock:
            self._queque.append((run_func, data, ID))
            self._wait_condition.acquire()
            self._wait_condition.notify()
            self._wait_condition.release()

    @QtCore.Slot()
    def _take(self):
        with self._lock:
            run_func, data, ID = self._queque.pop(0)
            if ID is not None:
                self._results[ID] = run_func(*data) if data is not None else run_func()
            else:
                _ = run_func(*data) if data is not None else run_func()
            self._condition.acquire()
            self._condition.notify()
            self._condition.release()

    def run(self):
        while True:
            self._wait_condition.acquire()
            self._wait_condition.wait()
            self._wait_condition.release()
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