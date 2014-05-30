__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from modules.gorokhovlibs.qt.qtwindow import BaseQtWindow
import os
from modules import constants, logger
from resourses import resourses


class MainForm(BaseQtWindow):
    def __init__(self, api):
        self.api = api
        super().__init__(self, os.path.join("resourses", "mainform.ui"))
        self.setWindowTitle(str(constants.application_title))

    def _set_connections(self):
        pass