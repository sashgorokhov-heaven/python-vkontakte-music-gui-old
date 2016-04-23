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
    def __init__(self, vkobject, widget=None, owner=None):
        self.__vkobject = vkobject
        self._current_widget = widget
        self._state = 'idle'
        self._owner = owner

    def get_owner(self):
        return self._owner

    def get_state(self):
        return self._state

    @QtCore.Slot(str, int)
    @QtCore.Slot(str, Exception)
    def set_state(self, state:str, params=None):
        self._state = state
        if self._current_widget:
            func = self._current_widget.__getattribute__('state_'+self._state)
            func(params) if params else func()

    def current_widget(self):
        return self._current_widget

    def set_current_widget(self, widget):
        self._current_widget = widget

    def id(self):
        return self.__vkobject['id']

    def get_vkobject(self):
        return self.__vkobject

    def artist(self):
        return self.__vkobject['artist']

    def title(self):
        return self.__vkobject['title']

    def url(self):
        return self.__vkobject['url']

    def duration(self, parsed=False):
        if parsed:
            mins = str('0'*(2-len(str(self.__vkobject['duration'] // 60)))+str(self.__vkobject['duration'] // 60))
            secs = str(self.__vkobject['duration']-60*(self.__vkobject['duration'] // 60))
            return (mins, secs)
        return self.__vkobject['duration']

    def __getattr__(self, item):
        return self.__vkobject[item]

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

    def clear_queque(self):
        with self._lock:
            self._queque.clear()
            self._results.clear()
            self._IDs.clear()

    def addTask(self, run_func, data=None, ID:int=None):
        with self._lock:
            self._queque.append((run_func, data, ID))
            self._wait_condition.acquire()
            self._wait_condition.notify()
            self._wait_condition.release()

    @QtCore.Slot()
    def _take(self):
        with self._lock:
            try:
                if len(self._queque)!=0:
                    run_func, data, ID = self._queque.pop(0)
                    if ID is not None:
                        self._results[ID] = run_func(*data) if data is not None else run_func()
                    else:
                        _ = run_func(*data) if data is not None else run_func()
            except Exception as e:
                print(e)
            finally:
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


class SpeedController(QtCore.QObject):
    _exiting_signal = QtCore.Signal()
    _tick_signal = QtCore.Signal()

    class _SpeedControllerThreaded(ThreadedWorker):
        def _workfunc(self):
            while True:
                self.sleep(1)
                self._kwargs['tick'].emit()

    def __init__(self):
        super().__init__()
        self._tick_signal.connect(self._tick_slot)
        self._thread = self._SpeedControllerThreaded(tick=self._tick_signal)
        self._exiting_signal.connect(self._thread.terminate)
        self._total_amount = 0
        self._speed = 0
        self._lock = threading.Lock()
        self._thread.start()

    @QtCore.Slot()
    def _tick_slot(self):
        print('aaaa')
        with self._lock:
            self._speed = self._total_amount
            self._total_amount = 0

    @QtCore.Slot()
    def exiting(self):
        self._exiting_signal.emit()

    def feed(self, amount:int):
        with self._lock:
            self._total_amount += amount

    def get_speed(self) -> int:
        return self._speed
