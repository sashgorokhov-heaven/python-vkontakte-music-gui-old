import collections
from PySide import QtCore, QtGui
from collections import Iterator
import logging

logger = logging.getLogger(__name__)


class ThreadRunnerMixin(object):
    def __init__(self):
        self._threads = list()
        super(ThreadRunnerMixin, self).__init__()

    def run_thread(self, thread):
        """
        :param QtCore.QThread thread:
        :rtype: QtCore.QThread
        """

        thread.start()
        logger.debug('Running thread: %s', thread)
        if not hasattr(self, '_threads'):
            self._threads = list()
        self._threads.append(thread)
        return thread


class BaseThread(QtCore.QThread):
    exititng = False

    @QtCore.Slot()
    def on_exit(self, *args, **kwargs):
        logger.debug('%s exiting', str(self))
        self.exititng = True


class ExecutableThread(BaseThread):
    def __init__(self, executable, *args, **kwargs):
        self.executable = executable
        self.args = args
        self.kwargs = kwargs
        super(ExecutableThread, self).__init__()

    def run(self):
        try:
            logger.debug('Running %s', str(self.executable))
            return self.executable(*self.args, **self.kwargs)
        finally:
            logger.debug('Complete: %s', str(self.executable))


def as_thread(func):
    def wrapper(*args, **kwargs):
        thread = ExecutableThread(func, *args, **kwargs)
        thread.start()
        return thread
    return wrapper


class GeneratorExecutor(QtCore.QObject):
    execute = QtCore.Signal(collections.Iterator)

    def __init__(self, process_events=True):
        super(GeneratorExecutor, self).__init__()
        self.process_events = process_events
        self.execute.connect(self.execute_slot)

    @QtCore.Slot(collections.Iterator)
    def execute_slot(self, iterator):
        try:
            result = next(iterator)
            if self.process_events:
                QtGui.QApplication.processEvents()
            self.execute.emit(iterator)
            return result
        except StopIteration:
            return
        except:
            logger.exception('Error while executing iterator: %s', iterator)
            raise

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, collections.Iterator):
                self.execute.emit(result)
            else:
                logger.warning('Result of %s is not and Iterator', func)
            return result
        return wrapper