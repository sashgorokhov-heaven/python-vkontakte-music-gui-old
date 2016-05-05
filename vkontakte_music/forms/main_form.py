# coding=utf-8
import logging
import re
import webbrowser
import functools
from PySide import QtCore, QtGui

from vkontakte_music import services
from vkontakte_music.forms.base import BaseForm
from vkontakte_music.generated import mainform
from vkontakte_music.utils.multithreading import GeneratorExecutor, BaseThread
from vkontakte_music.widgets import UserListWidgetItem, GroupListWidgetItem, VkontakteData, AudioWidget, \
    AudioListItemWidget

logger = logging.getLogger(__name__)


class AudioLoadThread(BaseThread):
    add_audio = QtCore.Signal(dict)
    set_audio_count = QtCore.Signal(str)

    def __init__(self, owner_id, album_id=0):
        self.owner_id = owner_id
        self.album_id = album_id
        super(AudioLoadThread, self).__init__()

    def run(self):
        # TODO: chunk loading of audios, on request, by ~200 items at once
        kwargs = dict(owner_id=self.owner_id)
        if self.album_id:
            kwargs['album_id'] = self.album_id
        data = services.api().call('audio.get', **kwargs)
        loading_message = '{total} ({p:.0f}%)'
        for n, audio in enumerate(data['items'], 1):
            if self.exititng:
                return
            self.add_audio.emit(audio)
            if n % 3 == 0:
                p = float(n)/data['count']*100
                self.set_audio_count.emit(loading_message.format(total=data['count'], p=p))
            self.msleep(80)
        self.set_audio_count.emit(str(data['count']))


class MainForm(BaseForm, mainform.Ui_Form):
    stop = False
    load_audio = QtCore.Signal(int, int)
    current_id = None

    def __init__(self):
        super(MainForm, self).__init__()
        self.friendsList.itemDoubleClicked.connect(self.item_double_clicked_slot)
        self.groupsList.itemDoubleClicked.connect(self.item_double_clicked_slot)

        self.friendsSearchEdit.textChanged.connect(
            functools.partial(self._search_edit_text_changed, item_list=self.friendsList))
        self.groupsSearchEdit.textChanged.connect(
            functools.partial(self._search_edit_text_changed, item_list=self.groupsList))

        self.open_in_browser_function = None

        self.load_audio.connect(self.load_audio_slot)

        self.select_all_button.clicked.connect(self.audioList.selectAll)
        self.deselect_all_button.clicked.connect(self.audioList.clearSelection)

        self.albums_combobox.currentIndexChanged.connect(self.album_changed)

        self.run_thread(services.api().call('groups.get', fields='photo_100', extended=1, callback_slot=self._on_groups_loaded))
        self.run_thread(services.api().call('users.get', callback_slot=self._on_user_loaded, fields='photo_100'))

    def _search_edit_text_changed(self, text, item_list):
        if not text:
            item_list.scrollToItem(item_list.item(0))
        else:
            count = item_list.count()
            for i in range(count):
                item = item_list.item(i)  # type: UserListWidgetItem
                data = item.get_data()
                item_text = item.get_text(data)
                if re.search(text.lower(), item_text.lower()):
                    item_list.scrollToItem(item)
                    item.setSelected(True)
                    break

    @QtCore.Slot(int)
    def album_changed(self, i):
        album = self.albums_combobox.itemData(i)
        if album is None:
            return
        self.load_audio.emit(album['owner_id'], album['id'])

    @QtCore.Slot(dict)
    def _on_user_loaded(self, data):
        user = data['response'][0]
        item = UserListWidgetItem(user)
        self.friendsList.addItem(item)
        self.item_double_clicked_slot(item)
        self.run_thread(services.api().call('friends.get', callback_slot=self._on_friends_loaded, fields='photo_100',
                                            order='hints'))

    @QtCore.Slot(dict)
    @GeneratorExecutor()
    def _on_friends_loaded(self, data):
        self.friendsLoadPBar.setMinimum(1)
        self.friendsLoadPBar.setMaximum(data['response']['count']-1)
        for n, user in enumerate(data['response']['items'], 1):
            yield self.friendsList.addItem(UserListWidgetItem(user))
            self.friendsLoadPBar.setValue(n)

    @QtCore.Slot(dict)
    @GeneratorExecutor()
    def _on_groups_loaded(self, data):
        self.groupsLoadPBar.setMinimum(1)
        self.groupsLoadPBar.setMaximum(data['response']['count']-1)
        for n, group in enumerate(data['response']['items']):
            yield self.groupsList.addItem(GroupListWidgetItem(group))
            self.groupsLoadPBar.setValue(n)

    @QtCore.Slot(VkontakteData)
    def item_double_clicked_slot(self, item):
        id = item.get_data()['id']
        if isinstance(item, GroupListWidgetItem):
            id *= -1
        self.load_audio.emit(id, 0)
        self.run_thread(services.api().call('audio.getAlbums', callback_slot=self.set_albums, owner_id=id))

    @QtCore.Slot(dict)
    @GeneratorExecutor()
    def set_albums(self, data):
        self.albums_combobox.clear()
        for album in data['response']['items']:
            yield self.albums_combobox.addItem(album['title'], album)

    @QtCore.Slot(int)
    @QtCore.Slot(int, int)
    def load_audio_slot(self, owner_id, album_id=0):
        logger.info('Loading audio of %s and %s', owner_id, album_id)
        self.current_id = owner_id
        self.audioList.clear()

        if self.open_in_browser_function is not None:
            self.open_in_browser_button.clicked.disconnect(self.open_in_browser_function)
        url = 'https://vk.com/audios{}'.format(owner_id)
        if album_id:
            url += '?album_id={}'.format(album_id)
        self.open_in_browser_function = lambda *args, **kwargs: webbrowser.open(url, new=2)
        self.open_in_browser_button.clicked.connect(self.open_in_browser_function)

        thread = AudioLoadThread(owner_id, album_id)
        self.load_audio.connect(thread.on_exit)
        thread.add_audio.connect(self.add_audio)
        thread.set_audio_count.connect(self.countLabel.setText)

        self.run_thread(thread)

    @QtCore.Slot(dict)
    def add_audio(self, audio):
        if self.current_id and str(self.current_id) != str(audio['owner_id']):
            return
        self.audioList.addItem(AudioListItemWidget(audio))