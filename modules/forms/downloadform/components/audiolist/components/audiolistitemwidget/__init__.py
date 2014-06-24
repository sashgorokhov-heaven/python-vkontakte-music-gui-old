from PySide import QtGui, QtCore
from .ui import Ui_Form

__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'


class AudioDownloadWidgetItem(QtGui.QWidget, Ui_Form):
    set_value_signal = QtCore.Signal(int)
    def __init__(self, vkaudio, download_manager, item):
        super().__init__()
        self.setupUi(self)
        self.item = item
        self.vkaudio = vkaudio
        self.vkaudio.set_state('waiting')
        self.download_manager = download_manager
        self.progressBar.setFormat('{} - {}'.format(self.vkaudio.artist(), self.vkaudio.title()))
        self.downloading = False
        self.set_value_signal.connect(self._set_value_slot)
        self.set_value_signal.emit(0)

    def doubleClicked(self):
        self.vkaudio.set_state('idle')
        self.download_manager.downloadListWidget.takeItem(
            self.download_manager.downloadListWidget.row(self.item))
        self.download_manager._updateButton()

    def mouseDoubleClickEvent(self, event=None):
        if not self.downloading:
            self.doubleClicked()

    @QtCore.Slot(int)
    def _set_value_slot(self, n:int):
        self.progressBar.setValue(n)