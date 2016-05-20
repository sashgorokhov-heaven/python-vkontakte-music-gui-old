# coding=utf-8
import logging
import os
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve

import shutil

import functools
from PySide import QtCore, QtGui

from vkontakte_music import settings
from vkontakte_music.forms.base import BaseForm
from vkontakte_music.generated import downloadform
from vkontakte_music.utils import get_audio_filename, get_artist
from vkontakte_music.utils.multithreading import GeneratorExecutor, BaseThread, ThreadRunnerMixin
from vkontakte_music.widgets import DownloadListItemWidget

logger = logging.getLogger(__name__)


class AudioDownloadThread(BaseThread):
    update_progress = QtCore.Signal(int)
    complete = QtCore.Signal(QtGui.QListWidgetItem, DownloadListItemWidget)
    _last_p = None

    def __init__(self, path, url, item, widget):
        """
        :param QtGui.QListWidgetItem item:
        :param DownloadListItemWidget widget:
        :param QtCore.Signal complete_signal:
        """
        super(AudioDownloadThread, self).__init__()
        self.path = path
        self.url = url
        self.item = item
        self.widget = widget

    def report_hook(self, transfered, block_size, total_size):
        p = round(((float(transfered)*float(block_size))/float(total_size)) * 100.0)
        if p != self._last_p:
            self.update_progress.emit(p)
            self._last_p = p

    def run(self):
        if os.path.exists(self.path):
            self.complete.emit(self.item, self.widget)
            return
        dirname = os.path.dirname(self.path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        urlretrieve(self.url, self.path, reporthook=self.report_hook)
        self.complete.emit(self.item, self.widget)


class DownloadManager(BaseThread, ThreadRunnerMixin):
    limit = 4

    def __init__(self, download_form):
        """
        :param DownloadForm download_form:
        """
        super(DownloadManager, self).__init__()
        self.download_form = download_form

    def run(self):
        while not self.exititng:
            if self.download_form.paused:
                self.sleep(1)
                continue
            downloading = 0
            for i in range(self.download_form.download_list_widget.count()):
                item = self.download_form.download_list_widget.item(i)
                if downloading == self.limit:
                    break
                widget = self.download_form.download_list_widget.itemWidget(item)  # type: DownloadListItemWidget
                if widget.downloading:
                    downloading += 1
                    continue
                if downloading < self.limit:
                    self.start_download(item, widget)
                    downloading += 1
                    continue
            self.sleep(1)

    def start_download(self, item, widget):
        """
        :param QtGui.QListWidgetItem item:
        :param DownloadListItemWidget widget:
        """
        logger.info('Starting download of %s', str(widget))
        widget.downloading = True
        audio = widget.get_data()
        path = self.download_form.get_download_path(audio)
        thread = AudioDownloadThread(path, audio['url'], item, widget)
        thread.update_progress.connect(widget.setValue)
        thread.complete.connect(self.download_complete)
        self.run_thread(thread)

    @QtCore.Slot(QtGui.QListWidgetItem, DownloadListItemWidget)
    def download_complete(self, item, widget):
        logger.info('Downalod complete of %s', str(widget))
        widget.downloading = False
        self.download_form.delete_item_signal.emit(item)


class DownloadForm(BaseForm, downloadform.Ui_download_form):
    _download_directory = None
    _exists_ids = set()
    paused = True
    delete_item_signal = QtCore.Signal(QtGui.QListWidgetItem)

    def __init__(self):
        super(DownloadForm, self).__init__()
        self.start_button.clicked.connect(lambda: self.pause_button.setEnabled(True))
        self.start_button.clicked.connect(lambda: self.start_button.setEnabled(False))
        self.start_button.clicked.connect(lambda: setattr(self, 'paused', False))
        self.pause_button.clicked.connect(lambda: self.start_button.setEnabled(True))
        self.pause_button.clicked.connect(lambda: self.pause_button.setEnabled(False))
        self.pause_button.clicked.connect(lambda: setattr(self, 'paused', True))
        self.download_list_widget.itemSelectionChanged.connect(
            lambda: self.delete_button.setEnabled(bool(len(self.download_list_widget.selectedIndexes()))))
        self.delete_button.clicked.connect(self.delete_button_clicked)
        self.destination_button.clicked.connect(self.set_download_directory)
        self.progressBar.setMaximum(0)
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)
        self.download_manager = DownloadManager(self)
        self.on_exit.connect(self.download_manager.on_exit)
        self.run_thread(self.download_manager)

        self.delete_item_signal.connect(self.delete_item)

    @QtCore.Slot()
    def set_download_directory(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, u'Место загрузки', settings.BASE_DIR)
        if not directory:
            return
        self._download_directory = directory

    def get_download_directory(self):
        return self._download_directory or os.path.join(settings.BASE_DIR, 'Music')

    def get_download_path(self, audio):
        """
        :param dict audio:
        :rtype: str
        """
        base_directory = self.get_download_directory()
        # if self.album_folder_checkbox.isChecked():
        #     # FIXME
        #     artist = get_artist(audio)
        #     logger.debug('Artist: %s', artist)
        #     if os.path.exists(os.path.join(base_directory, artist)):
        #         base_directory = os.path.join(base_directory, artist)
        #         logger.debug('Found artists folder: %s', base_directory)
        #     else:
        #         exists = self._find_by_artist(artist, base_directory)
        #         if exists:
        #             logger.debug('Found another tracks: %s', exists)
        #             base_directory = os.path.join(base_directory, artist)
        #             os.makedirs(base_directory)
        #             for filename in exists:
        #                 src = os.path.join(self.get_download_directory(), filename)
        #                 dst = os.path.join(base_directory, filename)
        #                 shutil.move(src, dst)

        filename = get_audio_filename(audio)
        return os.path.join(base_directory, filename)

    # def _find_by_artist(self, artist, base_directory=None):
    #     download_directory = base_directory or self.get_download_directory()
    #     if not os.path.exists(download_directory):
    #         os.makedirs(download_directory)
    #         return []
    #     paths = os.listdir(download_directory)
    #     return list(filter(lambda path: path.startswith(artist), paths))

    @GeneratorExecutor()
    def delete_button_clicked(self):
        for item in self.download_list_widget.selectedItems():
            yield self.delete_item_signal.emit(item)

    @QtCore.Slot(QtGui.QListWidgetItem)
    def delete_item(self, item):
        widget = self.download_list_widget.itemWidget(item)  # type: DownloadListItemWidget
        if widget.downloading:
            return
        self.download_list_widget.removeItemWidget(item)
        item = self.download_list_widget.takeItem(self.download_list_widget.row(item))
        self._exists_ids.discard(widget.get_data()['id'])
        self.progressBar.setMaximum(self.progressBar.maximum() - 1)
        del item

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    @QtCore.Slot(dict)
    def add_download(self, audio):
        if audio['id'] in self._exists_ids or os.path.exists(self.get_download_path(audio)):
            return
        item = QtGui.QListWidgetItem()
        self.download_list_widget.addItem(item)
        widget = DownloadListItemWidget(audio)
        self.download_list_widget.setItemWidget(item, widget)
        self.progressBar.setMaximum(self.progressBar.maximum() + 1)
        self._exists_ids.add(audio['id'])

    @QtCore.Slot(list)
    @GeneratorExecutor()
    def add_downloads(self, audios):
        for audio in audios:
            yield self.add_download(audio)