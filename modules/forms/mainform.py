__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PyQt4 import QtCore
from modules.gorokhovlibs.qt.qtwindow import BaseQtWindow
import os
from modules import constants, navigation_lists, audio_list, download_manager
from resourses import resourses


class MainForm(BaseQtWindow):
    def __init__(self, api):
        self.api = api
        super().__init__(self, os.path.join("resourses", "mainform.ui"))
        self.setWindowTitle(str(constants.application_title))
        self.navigation_lists = navigation_lists.NavigationLists(self)
        self.audio_list = audio_list.AudioListWidget(self)
        self.audio_list.connect(self.navigation_lists, QtCore.SIGNAL('listsItemClicked(int)'), self.audio_list.load_audio)
        self.download_manager = download_manager.AudioDownloadWidget(self)
        self.elements.downloadButton.clicked.connect(self.download_manager.show)

    def _set_connections(self):
        pass

    def downloadAudio(self, oobject):
        self.download_manager.addAudio(oobject)

    def closeEvent(self, event):
        self.navigation_lists.close()
        self.audio_list.close()
        event.accept()