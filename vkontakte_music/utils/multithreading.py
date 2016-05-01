from PySide import QtCore
from collections import Iterator
import logging

logger = logging.getLogger(__name__)


class BaseThread(QtCore.QThread):
    exititng = False

    def __init__(self, *args, **kwargs):
        super(BaseThread, self).__init__(*args, **kwargs)
        self.run = self.auto_stop(self.run)

    @QtCore.Slot()
    def on_exit(self):
        logger.debug('%s exiting', str(self))
        self.exititng = True

    def auto_stop(self, func):
        def wrapper(*args, **kwargs):
            generator = func(*args, **kwargs)
            if not isinstance(generator, Iterator):
                return
            while not self.exititng:
                retval = next(generator, False)
                if isinstance(retval, bool) and not retval:
                    break
        return wrapper


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
