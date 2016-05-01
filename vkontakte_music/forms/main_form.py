from urllib import urlretrieve

import requests
from datetime import timedelta

from vkontakte_music.forms.base import BaseForm
from vkontakte_music.generated import mainform
from vkontakte_music import services, cache
from PySide import QtCore, QtGui

from vkontakte_music.utils.multithreading import BaseThread, as_thread
from vkontakte_music.utils.networking import AsyncRequest
import logging

logger = logging.getLogger(__name__)


class IconListItem(QtGui.QListWidgetItem):

    def __init__(self, data, text=None):
        """
        :param dict data:
        :param QtGui.QIcon icon:
        """
        super(IconListItem, self).__init__(text or self.get_text(data))
        self._data = data
        self.set_icon(data)

    def set_icon(self, data):
        key = str(data['photo_100'])
        if not cache.exists(key):
            AsyncRequest(key, on_success=self._on_icon_downloaded)
        else:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(QtCore.QByteArray(cache.get(key)))
            self.setIcon(QtGui.QIcon(pixmap))

    @QtCore.Slot(requests.Response)
    def _on_icon_downloaded(self, response):
        key = str(self._data['photo_100'])
        response = requests.get(key)
        cache.set(key, response.raw.read(), timeout=timedelta(days=1))
        self.set_icon(self._data)

    @staticmethod
    def get_text(data):
        raise NotImplementedError


class UserListItem(IconListItem):
    @staticmethod
    def get_text(data):
        return data['first_name'] + ' ' + data['last_name']


class GroupListItem(IconListItem):
    @staticmethod
    def get_text(data):
        return data['name']


class NavigationMenu(QtCore.QObject):
    load_audio = QtCore.Signal(int)
    add_user_list_item = QtCore.Signal(dict)

    def __init__(self, main_form):
        """
        :param MainForm main_form:
        """
        super(NavigationMenu, self).__init__()
        self.main_form = main_form

        main_form.friendsList.itemDoubleClicked.connect(self.item_double_clicked_slot)
        main_form.groupsList.itemDoubleClicked.connect(self.item_double_clicked_slot)
        self.add_user_list_item.connect(self.add_user_list_item_slot)

        services.api().call('groups.get', fields='photo_100', extended=1, callback_slot=self.on_groups_loaded).start()
        services.api().call('users.get', callback_slot=self.on_user_loaded, fields='photo_100').start()

    @QtCore.Slot(dict)
    def on_user_loaded(self, data):
        user = data['response'][0]
        self.add_user_list_item.emit(user)
        services.api().call('friends.get', callback_slot=self.on_friends_loaded, fields='photo_100',
                            order='hints').start()

    @QtCore.Slot(dict)
    def add_user_list_item_slot(self, user):
        item = UserListItem(user)
        self.main_form.friendsList.addItem(item)
        self.main_form.friendsLoadPBar.setValue(self.main_form.friendsLoadPBar.value() + 1)
        return item

    @QtCore.Slot(dict)
    @as_thread
    def on_friends_loaded(self, data):
        self.main_form.friendsLoadPBar.setMinimum(1)
        self.main_form.friendsLoadPBar.setMaximum(data['response']['count'])
        for n, user in enumerate(data['response']['items'], 1):
            yield self.add_user_list_item.emit(user)


    def update_icon_cache(self, key):
        """
        :rtype: QtGui.QIcon
        """
        if not cache.exists(key):
            response = requests.get(key)
            cache.set(key, response.raw.read(), timeout=timedelta(days=1))

    @QtCore.Slot(dict)
    @as_thread
    def on_groups_loaded(self, data):
        for group in data['response']['items']:
            yield self.main_form.groupsList.addItem(GroupListItem(group))

    @QtCore.Slot(IconListItem)
    def item_double_clicked_slot(self, item):
        self.load_audio.emit(item.data['id'])


class AudioListLoadThread(BaseThread):
    def __init__(self, id):
        super(AudioListLoadThread, self).__init__()
        self.id = id

    def run(self):
        raise NotImplementedError()


class AudioList(QtCore.QObject):
    stop_loading_audio = QtCore.Signal()

    def __init__(self, widget):
        """
        :param QtGui.QListWidget widget:
        """
        self.widget = widget
        super(AudioList, self).__init__()

    @QtCore.Slot(int)
    def load_audio(self, id):
        self.stop_loading_audio.emit()
        self.widget.clear()
        thread = AudioListLoadThread(id)
        self.stop_loading_audio.connect(thread.on_exit)
        thread.start()


class MainForm(BaseForm, mainform.Ui_Form):
    def __init__(self):
        super(MainForm, self).__init__()
        self.navigation_menu = NavigationMenu(self)