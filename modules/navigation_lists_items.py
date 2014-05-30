__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PyQt4 import QtGui, QtCore
from modules import cacher, util
import os.path

class UserListItem(QtGui.QListWidgetItem):
    def __init__(self, userobject, api):
        self.userobject = userobject
        self.filename = str(self.userobject['id'])+os.path.splitext(self.userobject['photo_100'])[1]
        if not cacher.exists(self.filename):
            cacher.put_file(api.download(self.userobject['photo_100']), self.filename)
        self.filename = cacher.get_file(self.filename)
        text = self.userobject['first_name']+' '+self.userobject['last_name']
        super().__init__(text)

    def _setIcon(self):
        self.setIcon(QtGui.QIcon(self.filename))