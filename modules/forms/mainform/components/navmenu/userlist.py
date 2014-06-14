__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PySide import QtCore

class Task:
    def __init__(self):
        pass



class __UserListWorker(QtCore.QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        pass


class UserList:
    def __init__(self, parentform_ui, api, dispatcher):
        self.ui = parentform_ui
        self.api = api
        self.dispatcher = dispatcher