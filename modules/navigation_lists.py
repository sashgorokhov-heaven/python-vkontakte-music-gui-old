__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from modules.gorokhovlibs.threadeddecor import threaded
from modules import navigation_lists_items
from PyQt4 import QtCore, QtGui


class NavigationLists(QtCore.QObject):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.set_connections()
        self.stop = False
        self.userlist = list()
        self.friendslist = list()
        self.groupslist = list()
        self.loadUser()
        self.loadFriends()
        self.loadGroups()

    def close(self):
        self.stop = True

    def set_connections(self):
        self.connect(self, QtCore.SIGNAL('setIcons(int, QString)'), self.__setIcons)
        self.connect(self, QtCore.SIGNAL('loadUserComplete()'), self.loadUserComplete)
        self.parent.elements.userList.itemClicked.connect(self.userListItemClicked)
        self.connect(self, QtCore.SIGNAL('setFriendsLoadPbar(int)'), self.parent.elements.friendsLoadPBar.setValue)

    def setIcons(self, id, listname):
        self.emit(QtCore.SIGNAL('setIcons(int, QString)'), id, listname)

    def __setIcons(self, id, listname):
        list_ = getattr(self, listname)
        for itemobject, item in list_:
            if self.stop:
                return
            if itemobject['id'] == id:
                item.setIcon(QtGui.QIcon(item.filename))
                break

    @threaded
    def loadUser(self):
        userobject = self.parent.api.call('users.get', fields='photo_100')[0]
        item = navigation_lists_items.UserListItem(userobject, self.parent.api)
        self.parent.elements.userList.addItem(item)
        self.userlist.append((userobject, item))
        self.setIcons(userobject['id'], 'userlist')
        self.emit(QtCore.SIGNAL('loadUserComplete()'))

    def loadUserComplete(self):
        self.userlist[-1][1].setSelected(True)
        self.userListItemClicked(self.userlist[-1][1])

    def userListItemClicked(self, item):
        pass

    @threaded
    def loadFriends(self):
        friends = self.parent.api.call('friends.get', fields='photo_100', order='hints')['items']
        for n, friendobject in enumerate(friends, 1):
            if self.stop:
                return
            item = navigation_lists_items.UserListItem(friendobject, self.parent.api)
            self.parent.elements.friendsList.addItem(item)
            self.friendslist.append((friendobject, item))
            self.setIcons(friendobject['id'], 'friendslist')
            self.emit(QtCore.SIGNAL('setFriendsLoadPbar(int)'), n/len(friends)*100)

    @threaded
    def loadGroups(self):
        pass