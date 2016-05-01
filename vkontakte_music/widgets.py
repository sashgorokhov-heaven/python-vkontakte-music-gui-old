import logging

from PySide import QtGui, QtCore

import requests

from vkontakte_music import cache
from vkontakte_music.utils.multithreading import ThreadRunnerMixin
from vkontakte_music.utils.networking import AsyncRequest

logger = logging.getLogger(__name__)


class VkontakteListWidgetItem(QtGui.QListWidgetItem):
    def __init__(self, data):
        self._data = data
        super(VkontakteListWidgetItem, self).__init__(self.get_text(data))

    def get_data(self):
        return self._data

    def get_text(self, data):
        raise NotImplementedError


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
        logger.debug('Set from cache: %s', key)

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