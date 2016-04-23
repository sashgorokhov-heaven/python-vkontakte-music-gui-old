__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PySide import QtCore, QtGui
from modules import cacher, util
import os.path, re, threading


class _FriendsListItem(QtGui.QListWidgetItem):
    def __init__(self, friend_vkobject, iconfilename):
        self.vkobject = friend_vkobject
        super().__init__(self.get_caption())
        self.setIcon(QtGui.QIcon(iconfilename))

    def get_caption(self):
        return self.vkobject['first_name']+' '+self.vkobject['last_name']

class _FriendsListWorker(util.ThreadedWorker):
    def _workfunc(self):
        friends_vkobject = self._kwargs['api'].call('friends.get', fields='photo_100', order='hints')['items']
        for n, friend_vkobject in enumerate(friends_vkobject, 1):
            filename = str(friend_vkobject['id'])+os.path.splitext(friend_vkobject['photo_100'])[1]
            if not cacher.exists(filename):
                cacher.put_file(self._kwargs['api'].download(friend_vkobject['photo_100']), filename)
            iconfilename = cacher.get_file(filename)
            self._kwargs['addfriend_signal'].emit(friend_vkobject, iconfilename, n, len(friends_vkobject))


class FriendsList(QtCore.QObject):
    friendslist_itemclicked = QtCore.Signal(int)
    _addfriend_signal = QtCore.Signal(dict, str, int, int)
    _exiting_signal = QtCore.Signal()
    def __init__(self, parentform_ui, api, dispatcher):
        super().__init__()
        self.ui = parentform_ui
        self._api = api
        self._dispatcher = dispatcher
        self._exiting = False

        self.ui.friendsList.itemDoubleClicked.connect(self._friendsList_itemclicked)
        self.ui.friendsSearchEdit.textChanged.connect(self._friendssearch_editchanged)
        self._addfriend_signal.connect(self._addfriend)
        self._add_friends()

    @QtCore.Slot(_FriendsListItem)
    def _friendsList_itemclicked(self, item):
        self.friendslist_itemclicked.emit(item.vkobject['id'])

    @QtCore.Slot()
    def exiting(self):
        self._exiting = True
        self._exiting_signal.emit()

    def _add_friends(self):
        self.ui.friendsLoadPBar.setValue(0)
        self._worker_thread = _FriendsListWorker(api=self._api, addfriend_signal=self._addfriend_signal)
        self._worker_thread.finished.connect(self._work_complete)
        self._exiting_signal.connect(self._worker_thread.terminate)
        self._worker_thread.start()

    @QtCore.Slot(dict, str, int, int)
    def _addfriend(self, friend_vkobject, iconfilename, n, len_friends):
        if self._exiting: return
        self._dispatcher.addTask(FriendsList._addfriend_guiwork, (self, friend_vkobject, iconfilename, n, len_friends))

    @staticmethod
    def _addfriend_guiwork(self, friend_vkobject, iconfilename, n, len_friends):
        item = _FriendsListItem(friend_vkobject, iconfilename)
        self.ui.friendsList.addItem(item)
        self.ui.friendsLoadPBar.setValue(round((n/len_friends)*100))

    @QtCore.Slot()
    def _work_complete(self):
        self.ui.friendsLoadPBar.setValue(100)

    @QtCore.Slot(str)
    def _friendssearch_editchanged(self, line):
        if line:
            count = self.ui.friendsList.count()
            for i in range(count):
                item = self.ui.friendsList.item(i)
                if re.match(line.lower(), item.vkobject['first_name'].lower()) or re.match(line.lower(), item.vkobject['last_name'].lower()):
                    self.ui.friendsList.scrollToItem(item)
                    item.setSelected(True)
        else:
            self.ui.friendsList.scrollToItem(self.ui.friendsList.item(0))