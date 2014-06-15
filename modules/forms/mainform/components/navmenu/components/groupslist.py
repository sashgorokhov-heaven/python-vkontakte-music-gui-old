__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PySide import QtCore, QtGui
from modules import cacher, util
import os.path,threading, re


class _GroupsListItem(QtGui.QListWidgetItem):
    def __init__(self, group_vkobject, iconfilename):
        self.vkobject = group_vkobject
        super().__init__(self.get_caption())
        self.setIcon(QtGui.QIcon(iconfilename))

    def get_caption(self):
        return self.vkobject['name']

class _GroupsListWorker(util.ThreadedWorker):
    def _workfunc(self):
        groups_vkobject = self._kwargs['api'].call('groups.get', fields='photo_100', extended=1)['items']
        for n, group_vkobject in enumerate(groups_vkobject, 1):
            filename = str(group_vkobject['id'])+os.path.splitext(group_vkobject['photo_100'])[1]
            if not cacher.exists(filename):
                cacher.put_file(self._kwargs['api'].download(group_vkobject['photo_100']), filename)
            iconfilename = cacher.get_file(filename)
            self._kwargs['addgroup_signal'].emit(group_vkobject, iconfilename, n, len(groups_vkobject))


class GroupsList(QtCore.QObject):
    groupslist_itemclicked = QtCore.Signal(int)
    _addgroup_signal = QtCore.Signal(dict, str, int, int)
    _exiting_signal = QtCore.Signal()
    def __init__(self, parentform_ui, api, dispatcher):
        super().__init__()
        self.ui = parentform_ui
        self._api = api
        self._dispatcher = dispatcher
        self._exiting = False

        self.ui.groupsList.itemDoubleClicked.connect(self._groupsList_itemclicked)
        self.ui.groupsSearchEdit.textChanged.connect(self._groupssearch_editchanged)

        self._addgroup_signal.connect(self._addgroup)
        self._add_groups()

    @QtCore.Slot(_GroupsListItem)
    def _groupsList_itemclicked(self, item):
        self.groupslist_itemclicked.emit(-item.vkobject['id'])

    @QtCore.Slot()
    def exiting(self):
        self._exiting = True
        self._exiting_signal.emit()

    def _add_groups(self):
        self.ui.groupsLoadPBar.setValue(0)
        self._worker_thread = _GroupsListWorker(api=self._api, addgroup_signal=self._addgroup_signal)
        self._worker_thread.finished.connect(self._work_complete)
        self._exiting_signal.connect(self._worker_thread.terminate)
        self._worker_thread.start()

    @QtCore.Slot(dict, str, int, int)
    def _addgroup(self, group_vkobject, iconfilename, n, len_groups):
        if self._exiting: return
        self._dispatcher.addTask(GroupsList._addgroup_guiwork, (self, group_vkobject, iconfilename, n, len_groups))

    @staticmethod
    def _addgroup_guiwork(self, group_vkobject, iconfilename, n, len_groups):
        item = _GroupsListItem(group_vkobject, iconfilename)
        self.ui.groupsList.addItem(item)
        self.ui.groupsLoadPBar.setValue(round((n/len_groups)*100))

    @QtCore.Slot()
    def _work_complete(self):
        self.ui.groupsLoadPBar.setValue(100)

    @QtCore.Slot(str)
    def _groupssearch_editchanged(self, line):
        if line:
            count = self.ui.groupsList.count()
            for i in range(count):
                item = self.ui.groupsList.item(i)
                if re.match(line.lower(), item.vkobject['name'].lower()):
                    self.ui.groupsList.scrollToItem(item)
                    item.setSelected(True)
        else:
            self.ui.groupsList.scrollToItem(self.ui.groupsList.item(0))