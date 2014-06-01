__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PyQt4 import QtGui, QtCore
from modules import cacher, util
import os.path

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