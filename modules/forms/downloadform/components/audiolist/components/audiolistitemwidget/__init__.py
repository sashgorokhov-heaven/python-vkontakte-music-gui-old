from PySide import QtGui
from .ui import Ui_Form

__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'


class AudioDownloadWidgetItem(QtGui.QWidget, Ui_Form):
    def __init__(self, vkaudio, download_manager, item):
        super().__init__()
        self.setupUi(self)
        self.item = item
        self.vkaudio = vkaudio
        self.vkaudio.set_state('waiting')
        self.download_manager = download_manager
        self.titleLabel.setText(self.vkaudio.title())
        self.artistLabel.setText(self.vkaudio.artist())

    def doubleClicked(self):
        self.vkaudio.set_state('idle')
        self.download_manager.downloadListWidget.takeItem(
            self.download_manager.downloadListWidget.row(self.item))

    def mouseDoubleClickEvent(self, event=None):
        self.doubleClicked()