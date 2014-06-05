__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PyQt4 import QtCore
from modules.gorokhovlibs.qt.qtwindow import BaseQtWindow
import os
from modules import constants, navmenu, audio_list, download_manager, util
from resourses import resourses


class MainForm(BaseQtWindow):
    def __init__(self, api):
        self.api = api
        super().__init__(self, os.path.join("resourses", "mainform.ui"))
        self.setWindowTitle(str(constants.application_title))

        self.buffer = util.Buffer()

        self.navigation_menu = navmenu.NavigationMenu(self)
        self.audio_list = audio_list.AudioListWidget(self)
        self.audio_list.connect(self.navigation_menu, QtCore.SIGNAL('menuItemClicked(int)'), self.audio_list.load_audio)
        self.download_manager = download_manager.AudioDownloadWidget(self)
        self.download_manager.connect(self.audio_list, QtCore.SIGNAL('itemChoosed(int)'), self.download_manager.add)
        self.audio_list.connect(self.download_manager, QtCore.SIGNAL('updateState(int, int)'), self.audio_list.updateState)
        self.elements.downloadButton.clicked.connect(self.download_manager.show)

    def _set_connections(self):
        pass

    def closeEvent(self, event):
        self.navigation_menu.close()
        self.audio_list.close()
        self.download_manager.close()
        event.accept()