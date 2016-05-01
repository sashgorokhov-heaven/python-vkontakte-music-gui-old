import logging

from PySide import QtCore, QtGui

from vkontakte_music import services
from vkontakte_music.forms.base import BaseForm
from vkontakte_music.generated import mainform
from vkontakte_music.utils.multithreading import GeneratorExecutor, BaseThread
from vkontakte_music.widgets import UserListWidgetItem, GroupListWidgetItem, VkontakteData, AudioWidget

logger = logging.getLogger(__name__)


class AudioLoadThread(BaseThread):
    add_audio = QtCore.Signal(dict)
    set_audio_count = QtCore.Signal(str)

    def __init__(self, owner_id):
        self.owner_id = owner_id
        super(AudioLoadThread, self).__init__()

    def run(self):
        data = services.api().call('audio.get', owner_id=self.owner_id)
        self.set_audio_count.emit(str(data['count']))
        for audio in data['items']:
            if self.exititng:
                return
            self.add_audio.emit(audio)
            self.msleep(50)


class MainForm(BaseForm, mainform.Ui_Form):
    stop = False
    load_audio = QtCore.Signal(int)

    def __init__(self):
        super(MainForm, self).__init__()
        self.friendsList.itemDoubleClicked.connect(self.item_double_clicked_slot)
        self.groupsList.itemDoubleClicked.connect(self.item_double_clicked_slot)
        self.load_audio.connect(self.load_audio_slot)

        self.run_thread(services.api().call('groups.get', fields='photo_100', extended=1, callback_slot=self._on_groups_loaded))
        self.run_thread(services.api().call('users.get', callback_slot=self._on_user_loaded, fields='photo_100'))

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
        self.friendsLoadPBar.setMaximum(data['response']['count'])
        for n, user in enumerate(data['response']['items'], 1):
            yield self.friendsList.addItem(UserListWidgetItem(user))
            self.friendsLoadPBar.setValue(n)

    @QtCore.Slot(dict)
    @GeneratorExecutor()
    def _on_groups_loaded(self, data):
        self.groupsLoadPBar.setMinimum(1)
        self.groupsLoadPBar.setMaximum(data['response']['count'])
        for n, group in enumerate(data['response']['items']):
            yield self.groupsList.addItem(GroupListWidgetItem(group))
            self.groupsLoadPBar.setValue(n)

    @QtCore.Slot(VkontakteData)
    def item_double_clicked_slot(self, item):
        id = item.get_data()['id']
        if isinstance(item, GroupListWidgetItem):
            id *= -1
        self.load_audio.emit(id)
        logger.info('Loading audio of %s', id)

    @QtCore.Slot(int)
    def load_audio_slot(self, id):
        self.audioList.clear()

        thread = AudioLoadThread(id)
        self.load_audio.connect(thread.on_exit)
        thread.add_audio.connect(self.add_audio)
        thread.set_audio_count.connect(self.countLabel.setText)

        self.run_thread(thread)

    @QtCore.Slot(dict)
    def add_audio(self, audio):
        item = QtGui.QListWidgetItem()
        widget = AudioWidget(audio)
        self.audioList.addItem(item)
        self.audioList.setItemWidget(item, widget)