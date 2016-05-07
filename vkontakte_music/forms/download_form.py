from PySide import QtCore, QtGui

from vkontakte_music.forms.base import BaseForm
from vkontakte_music.generated import downloadform
from vkontakte_music.utils.multithreading import GeneratorExecutor
from vkontakte_music.widgets import DownloadListItemWidget


class DownloadForm(BaseForm, downloadform.Ui_download_form):
    def __init__(self):
        super(DownloadForm, self).__init__()
        self.start_button.clicked.connect(lambda: self.pause_button.setEnabled(True))
        self.start_button.clicked.connect(lambda: self.start_button.setEnabled(False))
        self.pause_button.clicked.connect(lambda: self.start_button.setEnabled(True))
        self.pause_button.clicked.connect(lambda: self.pause_button.setEnabled(False))
        self.download_list_widget.itemSelectionChanged.connect(
            lambda: self.delete_button.setEnabled(bool(len(self.download_list_widget.selectedIndexes()))))
        self.delete_button.clicked.connect(self.delete_button_clicked)

    @GeneratorExecutor()
    def delete_button_clicked(self):
        for item in self.download_list_widget.selectedItems():
            widget = self.download_list_widget.itemWidget(item) # type: DownloadListItemWidget
            if widget.downloading:
                continue
            self.download_list_widget.removeItemWidget(item)
            item = self.download_list_widget.takeItem(self.download_list_widget.row(item))
            del item
            yield

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    @QtCore.Slot(dict)
    def add_download(self, audio):
        item = QtGui.QListWidgetItem()
        self.download_list_widget.addItem(item)
        widget = DownloadListItemWidget(audio)
        self.download_list_widget.setItemWidget(item, widget)

    @QtCore.Slot(list)
    @GeneratorExecutor()
    def add_downloads(self, audios):
        for audio in audios:
            yield self.add_download(audio)
