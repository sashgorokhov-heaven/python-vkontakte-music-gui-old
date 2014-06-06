__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from modules import cacher
from PySide import QtCore, QtGui
import re, os.path
from modules.util import LoadThread

SLEEPTIME = 150

class UserListItem(QtGui.QListWidgetItem):
    def __init__(self, userobject, api):
        self.object = userobject
        self.filename = str(self.object['id'])+os.path.splitext(self.object['photo_100'])[1]
        global SLEEPTIME
        if not cacher.exists(self.filename):
            cacher.put_file(api.download(self.object['photo_100']), self.filename)
            SLEEPTIME = 150
        else:
            SLEEPTIME = 10
        self.filename = cacher.get_file(self.filename)
        text = self.object['first_name']+' '+self.object['last_name']
        super().__init__(text)

class GroupsListItem(QtGui.QListWidgetItem):
    def __init__(self, groupobject, api):
        self.object = groupobject
        self.filename = str(self.object['id'])+os.path.splitext(self.object['photo_100'])[1]
        global SLEEPTIME
        if not cacher.exists(self.filename):
            cacher.put_file(api.download(self.object['photo_100']), self.filename)
            SLEEPTIME = 150
        else:
            SLEEPTIME = 10
        self.filename = cacher.get_file(self.filename)
        text = self.object['name']
        super().__init__(text)

class NavigationMenu(QtCore.QObject):
    menuItemClicked = QtCore.Signal(int)

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.__stop = False

        self.parent.friendsSearchEdit.textChanged.connect(self.__friendsSearchEditChanged)
        self.parent.groupsSearchEdit.textChanged.connect(self.__groupsSearchEditChanged)
        self.parent.userList.itemClicked.connect(self.__listsItemClicked)
        self.parent.groupsList.itemClicked.connect(self.__listsItemClicked)
        self.parent.friendsList.itemClicked.connect(self.__listsItemClicked)

        self.__loadUser()
        self.__loadFriends()
        self.__loadGroups()

    @QtCore.Slot(GroupsListItem)
    @QtCore.Slot(UserListItem)
    def __listsItemClicked(self, item):
        uid = -item.object['id'] if 'screen_name' in item.object else item.object['id']
        self.menuItemClicked.emit(uid)

    @QtCore.Slot()
    def exiting(self):
        self.__stop = True

    @QtCore.Slot(str)
    def __friendsSearchEditChanged(self, line):
        if line:
            count = self.parent.friendsList.count()
            for i in range(count):
                item = self.parent.friendsList.item(i)
                if re.match(line.lower(), item.object['first_name'].lower()) or re.match(line.lower(), item.object['last_name'].lower()):
                    self.parent.friendsList.scrollToItem(item)
                    item.setSelected(True)
        else:
            self.parent.friendsList.scrollToItem(self.parent.friendsList.item(0))

    @QtCore.Slot(str)
    def __groupsSearchEditChanged(self, line):
        if line:
            count = self.parent.groupsList.count()
            for i in range(count):
                item = self.parent.groupsList.item(i)
                if re.match(line.lower(), item.object['name'].lower()):
                    self.parent.groupsList.scrollToItem(item)
                    item.setSelected(True)
        else:
            self.parent.groupsList.scrollToItem(self.parent.groupsList.item(0))

    def __loadUser(self):
        def work(emitter):
            userobject = self.parent.api.call('users.get', fields='photo_100')[0]
            emitter.emit(userobject, 0, 0)
        self.__userLoader = LoadThread(work)
        self.__userLoader.signalEmitter.connect(self.__loadUserComplete)
        self.__userLoader.start()

    @QtCore.Slot()
    def __loadUserComplete(self, userobject, n, b):
        item = UserListItem(userobject, self.parent.api)
        item.setIcon(QtGui.QIcon(item.filename))
        self.parent.userList.addItem(item)
        item.setSelected(True)
        self.__listsItemClicked(item)

    def __loadFriends(self):
        self.__friendsLoader = LoadThread(self.__loadFriendsFunc)
        self.__friendsLoader.signalEmitter.connect(self.__addFriendSlot)
        self.__friendsLoader.start()

    def __loadFriendsFunc(self, emitter):
        friends = self.parent.api.call('friends.get', fields='photo_100', order='hints')['items']
        for n, friendobject in enumerate(friends, 1):
            if self.__stop:
                return
            emitter.emit(friendobject, n, len(friends))
            QtCore.QThread.msleep(SLEEPTIME)

    @QtCore.Slot(dict, int, int)
    def __addFriendSlot(self, friendobject, n, total):
        item = UserListItem(friendobject, self.parent.api)
        self.parent.friendsList.addItem(item)
        item.setIcon(QtGui.QIcon(item.filename))
        self.parent.friendsLoadPBar.setValue(n/total*100)

    def __loadGroups(self):
        self.__groupsLoader = LoadThread(self.__loadGroupsFunc)
        self.__groupsLoader.signalEmitter.connect(self.__addGroupSlot)
        self.__groupsLoader.start()

    def __loadGroupsFunc(self, emitter):
        groups = self.parent.api.call('groups.get', fields='photo_100', extended=1)['items']
        for n, groupobject in enumerate(groups, 1):
            if self.__stop:
                return
            emitter.emit(groupobject, n, len(groups))
            QtCore.QThread.msleep(SLEEPTIME)

    @QtCore.Slot(dict, int, int)
    def __addGroupSlot(self, groupobject, n, total):
        item = GroupsListItem(groupobject, self.parent.api)
        self.parent.groupsList.addItem(item)
        item.setIcon(QtGui.QIcon(item.filename))
        self.parent.groupsLoadPBar.setValue(n/total*100)