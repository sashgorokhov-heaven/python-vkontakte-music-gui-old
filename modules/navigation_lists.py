__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from modules.gorokhovlibs.threadeddecor import threaded
from modules import cacher
from PyQt4 import QtCore, QtGui
import re, os.path

class UserListItem(QtGui.QListWidgetItem):
    def __init__(self, userobject, api):
        self.object = userobject
        self.filename = str(self.object['id'])+os.path.splitext(self.object['photo_100'])[1]
        if not cacher.exists(self.filename):
            cacher.put_file(api.download(self.object['photo_100']), self.filename)
        self.filename = cacher.get_file(self.filename)
        text = self.object['first_name']+' '+self.object['last_name']
        super().__init__(text)

    def _setIcon(self):
        self.setIcon(QtGui.QIcon(self.filename))

class GroupsListItem(QtGui.QListWidgetItem):
    def __init__(self, groupobject, api):
        self.object = groupobject
        self.filename = str(self.object['id'])+os.path.splitext(self.object['photo_100'])[1]
        if not cacher.exists(self.filename):
            cacher.put_file(api.download(self.object['photo_100']), self.filename)
        self.filename = cacher.get_file(self.filename)
        text = self.object['name']
        super().__init__(text)

    def _setIcon(self):
        self.setIcon(QtGui.QIcon(self.filename))

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
        self.connect(self, QtCore.SIGNAL('setIcons(int, QString)'), self.__setIcon)
        self.connect(self, QtCore.SIGNAL('loadUserComplete()'), self.loadUserComplete)
        self.parent.elements.userList.itemClicked.connect(self.listsItemClicked)
        self.parent.elements.groupsList.itemClicked.connect(self.listsItemClicked)
        self.parent.elements.friendsList.itemClicked.connect(self.listsItemClicked)
        self.parent.elements.friendsSearchEdit.textChanged.connect(self.friendsSearchEditChanged)
        self.parent.elements.groupsSearchEdit.textChanged.connect(self.groupsSearchEditChanged)
        self.connect(self, QtCore.SIGNAL('setFriendsLoadPbar(int)'), self.parent.elements.friendsLoadPBar.setValue)
        self.connect(self, QtCore.SIGNAL('setGroupsLoadPbar(int)'), self.parent.elements.groupsLoadPBar.setValue)

    def friendsSearchEditChanged(self, line):
        if line:
            count = self.parent.elements.friendsList.count()
            for i in range(count):
                item = self.parent.elements.friendsList.item(i)
                if re.match(line.lower(), item.object['first_name'].lower()) or re.match(line.lower(), item.object['last_name'].lower()):
                    self.parent.elements.friendsList.scrollToItem(item)
                    item.setSelected(True)
        else:
            self.parent.elements.friendsList.scrollToItem(self.parent.elements.friendsList.item(0))

    def groupsSearchEditChanged(self, line):
        if line:
            count = self.parent.elements.groupsList.count()
            for i in range(count):
                item = self.parent.elements.groupsList.item(i)
                if re.match(line.lower(), item.object['name'].lower()):
                    self.parent.elements.groupsList.scrollToItem(item)
                    item.setSelected(True)
        else:
            self.parent.elements.groupsList.scrollToItem(self.parent.elements.groupsList.item(0))

    def setIcon(self, id, listname):
        self.emit(QtCore.SIGNAL('setIcons(int, QString)'), id, listname)

    def __setIcon(self, id, listname):
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
        item = UserListItem(userobject, self.parent.api)
        self.parent.elements.userList.addItem(item)
        self.userlist.append((userobject, item))
        self.setIcon(userobject['id'], 'userlist')
        self.emit(QtCore.SIGNAL('loadUserComplete()'))

    def loadUserComplete(self):
        self.userlist[-1][1].setSelected(True)
        self.listsItemClicked(self.userlist[-1][1])

    def listsItemClicked(self, item):
        id = -item.object['id'] if 'screen_name' in item.object else item.object['id']
        self.emit(QtCore.SIGNAL('listsItemClicked(int)'), id)

    @threaded
    def loadFriends(self):
        friends = self.parent.api.call('friends.get', fields='photo_100', order='hints')['items']
        for n, friendobject in enumerate(friends, 1):
            if self.stop:
                return
            item = UserListItem(friendobject, self.parent.api)
            self.parent.elements.friendsList.addItem(item)
            self.friendslist.append((friendobject, item))
            self.setIcon(friendobject['id'], 'friendslist')
            self.emit(QtCore.SIGNAL('setFriendsLoadPbar(int)'), n/len(friends)*100)

    @threaded
    def loadGroups(self):
        groups = self.parent.api.call('groups.get', fields='photo_100', extended=1)['items']
        for n, groupobject in enumerate(groups, 1):
            if self.stop:
                return
            item = GroupsListItem(groupobject, self.parent.api)
            self.parent.elements.groupsList.addItem(item)
            self.groupslist.append((groupobject, item))
            self.setIcon(groupobject['id'], 'groupslist')
            self.emit(QtCore.SIGNAL('setGroupsLoadPbar(int)'), n/len(groups)*100)