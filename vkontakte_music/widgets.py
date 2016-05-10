import logging

from PySide import QtGui, QtCore

import requests

from vkontakte_music import cache
from vkontakte_music.utils.multithreading import ThreadRunnerMixin
from vkontakte_music.utils.networking import AsyncRequest

logger = logging.getLogger(__name__)


class VkontakteData(object):
    def __init__(self, data):
        self._data = data
        super(VkontakteData, self).__init__()

    def get_data(self):
        return self._data

    def get_text(self, data):
        raise NotImplementedError


class VkontakteListWidgetItem(VkontakteData, QtGui.QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super(VkontakteListWidgetItem, self).__init__(*args, **kwargs)
        self.setText(self.get_text(self.get_data()))


class UrlIconListWidgetItem(VkontakteListWidgetItem, ThreadRunnerMixin):
    def __init__(self, data, load_immediately=True):
        super(UrlIconListWidgetItem, self).__init__(data)
        if load_immediately:
            self.load_icon()

    def load_icon(self):
        url = self.get_icon_url(self._data)
        if not cache.exists(url):
            logger.debug('Not found in cache: %s', url)
            self.run_thread(AsyncRequest(url, on_success=self._on_icon_loaded))
        else:
            self._set_icon_from_cache(url)

    def _set_icon_from_cache(self, key):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(cache.get(key))
        self.setIcon(QtGui.QIcon(pixmap))
        #logger.debug('Set from cache: %s', key)

    @QtCore.Slot(requests.Response)
    def _on_icon_loaded(self, response):
        url = self.get_icon_url(self._data)
        logger.debug('Loaded icon: %s', url)
        cache.set(url, response.content)
        self._set_icon_from_cache(url)

    def get_icon_url(self, data):
        raise NotImplementedError


class UserListWidgetItem(UrlIconListWidgetItem):
    def get_text(self, data):
        return data['first_name'] + ' ' + data['last_name']

    def get_icon_url(self, data):
        return str(data['photo_100'])


class GroupListWidgetItem(UserListWidgetItem):
    def get_text(self, data):
        return data['name']


class AudioListItemWidget(VkontakteListWidgetItem):
    format = '{0[artist]} - {0[title]} {1[0]}:{1[1]}'

    def get_text(self, data):
        return unicode(self.format).format(data, self.get_duration(data))

    def get_duration(self, data):
        mins = str('0' * (2 - len(str(data['duration'] // 60))) + str(data['duration'] // 60))
        secs = str(data['duration'] - 60 * (data['duration'] // 60))
        return mins, secs


class DownloadListItemWidget(VkontakteData, QtGui.QProgressBar):
    downloading = False

    def __init__(self, *args, **kwargs):
        super(DownloadListItemWidget, self).__init__(*args, **kwargs)
        self.setFormat(self.get_text(self.get_data()))
        self.setMinimum(0)
        self.setMaximum(100)
        self.setAlignment(QtCore.Qt.AlignHCenter)
        self.setAlignment(QtCore.Qt.AlignVCenter)
        self.setValue(0)

    def get_text(self, data):
        return unicode(AudioListItemWidget.format).format(data, self.get_duration(data)) + '  %p%'

    def get_duration(self, data):
        mins = str('0' * (2 - len(str(data['duration'] // 60))) + str(data['duration'] // 60))
        secs = str(data['duration'] - 60 * (data['duration'] // 60))
        return mins, secs

    def __unicode__(self):
        return u'{0[artist]} - {0[title]}'.format(self.get_data())
