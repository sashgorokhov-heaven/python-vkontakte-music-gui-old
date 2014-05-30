__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PyQt4 import QtCore
import random

def showmessage(msg):
    print(str(msg))

class SafeExecutor(QtCore.QObject):
    def __init__(self, parent):
        super().__init__(parent)

    def execute(self, func):
        self.connect(self, QtCore.SIGNAL('signal()'), func)
        self.emit(QtCore.SIGNAL('signal()'))