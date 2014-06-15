from PySide import QtGui, QtCore
from modules.forms.mainform.components.navmenu.components.userlist import UserList
from modules.forms.mainform.components.navmenu.components.friendslist import FriendsList
from modules.forms.mainform.components.navmenu.components import Dispatcher

class NavigationMenu(QtCore.QObject):
    _exiting_signal = QtCore.Signal()
    menu_itemclicked = QtCore.Signal(int)
    def __init__(self, parentform_ui, api):
        super().__init__()
        self.ui = parentform_ui
        self._api = api
        self._exiting = True
        self._dispatcher = Dispatcher()
        self._exiting_signal.connect(self._dispatcher.terminate)
        self._dispatcher.start()

        self.user_list = UserList(self.ui, self._api, self._dispatcher)
        self._exiting_signal.connect(self.user_list.exiting)
        self.user_list.userlist_itemclicked.connect(self._menu_itemclicked)

        self.friends_list = FriendsList(self.ui, self._api, self._dispatcher)
        self._exiting_signal.connect(self.friends_list.exiting)
        self.user_list.userlist_itemclicked.connect(self._menu_itemclicked)

    @QtCore.Slot(int)
    def _menu_itemclicked(self, uid):
        self.menu_itemclicked.emit(uid)

    @QtCore.Slot()
    def exiting(self):
        self._exiting = True
        self._exiting_signal.emit()

