import logging

from PySide import QtCore, QtGui

from vkontakte_music import services
from vkontakte_music.forms.base import BaseForm
from vkontakte_music.generated import mainform
from vkontakte_music.utils.multithreading import GeneratorExecutor
from vkontakte_music.widgets import UserListWidgetItem, GroupListWidgetItem, VkontakteListWidgetItem

logger = logging.getLogger(__name__)


class MainForm(BaseForm, mainform.Ui_Form):
    def __init__(self):
        super(MainForm, self).__init__()
        self.friendsList.itemDoubleClicked.connect(self.item_double_clicked_slot)
        self.groupsList.itemDoubleClicked.connect(self.item_double_clicked_slot)

        self.run_thread(services.api().call('groups.get', fields='photo_100', extended=1, callback_slot=self._on_groups_loaded))
        self.run_thread(services.api().call('users.get', callback_slot=self._on_user_loaded, fields='photo_100'))

    @QtCore.Slot(dict)
    def _on_user_loaded(self, data):
        user = data['response'][0]
        self.friendsList.addItem(UserListWidgetItem(user))
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

    @QtCore.Slot(VkontakteListWidgetItem)
    def item_double_clicked_slot(self, item):
        print(item.get_data())