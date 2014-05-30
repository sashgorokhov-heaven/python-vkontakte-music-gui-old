__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from modules.gorokhovlibs.qt.qtwindow import BaseQtWindow
import os
from modules import constants, logger, navigation_lists
from resourses import resourses


class MainForm(BaseQtWindow):
    def __init__(self, api):
        self.api = api
        super().__init__(self, os.path.join("resourses", "mainform.ui"))
        self.setWindowTitle(str(constants.application_title))
        self.navigation_lists = navigation_lists.NavigationLists(self)

    def _set_connections(self):
        pass

    def closeEvent(self, event):
        self.navigation_lists.close()
        event.accept()