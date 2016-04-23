__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PySide import QtCore, QtGui
from modules import cacher, util
import os.path


class _UserListItem(QtGui.QListWidgetItem):
    def __init__(self, user_vkobject, iconfilename):
        self.vkobject = user_vkobject
        super().__init__(self.get_caption())
        self.setIcon(QtGui.QIcon(iconfilename))

    def get_caption(self):
        return self.vkobject['first_name']+' '+self.vkobject['last_name']

class _UserListWorker(util.ThreadedWorker):
    def _workfunc(self):
        user_vkobject = self._kwargs['api'].call('users.get', fields='photo_100')[0]
        filename = str(user_vkobject['id'])+os.path.splitext(user_vkobject['photo_100'])[1]
        if not cacher.exists(filename):
            cacher.put_file(self._kwargs['api'].download(user_vkobject['photo_100']), filename)
        iconfilename = cacher.get_file(filename)
        return user_vkobject, iconfilename


class UserList(QtCore.QObject):
    userlist_itemclicked = QtCore.Signal(int)

    def __init__(self, parentform_ui, api, dispatcher):
        super().__init__()
        self.ui = parentform_ui
        self._api = api
        self._dispatcher = dispatcher
        self._exiting = False

        self.ui.userList.itemDoubleClicked.connect(self._userlist_itemclicked)

        self._add_user()
        # TODO: self.add_recomendations()
        # TODO: self.add_playlists()

    @QtCore.Slot(_UserListItem)
    def _userlist_itemclicked(self, item):
        self.userlist_itemclicked.emit(item.vkobject['id'])

    @QtCore.Slot()
    def exiting(self):
        self._exiting = True

    def _add_user(self):
        self._worker_thread = _UserListWorker(api=self._api)
        self._worker_thread.finished.connect(self._work_complete)
        self._worker_thread.start()

    @QtCore.Slot()
    def _work_complete(self):
        if self._exiting: return
        self._dispatcher.addTask(UserList._gui_work, (self, ))

    @staticmethod
    def _gui_work(self):
        user_vkobject, iconfilename = self._worker_thread.get_result()
        item = _UserListItem(user_vkobject, iconfilename)
        self.ui.userList.addItem(item)
        item.setSelected(True)
        self._userlist_itemclicked(item)

    def add_recomendations(self):
        raise NotImplementedError

    def add_playlists(self):
        raise NotImplementedError