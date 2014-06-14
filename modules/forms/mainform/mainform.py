from PySide import QtCore, QtGui
from modules.forms.downloadform import downloadform
from modules.forms.mainform.components.navmenu import navmenu
from modules.forms.mainform.components.audiolist import audio_list
from modules.forms.mainform.ui import Ui_Form
from modules import constants

__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'


class MainForm(QtGui.QWidget, Ui_Form):
    exiting = QtCore.Signal()

    def __init__(self, api):
        self.api = api
        super().__init__()
        self.ui = self.setupUi(self)

        self.setWindowTitle(str(constants.application_title))

        self.navigation_menu = navmenu.NavigationMenu(self)
        self.exiting.connect(self.navigation_menu.exiting)

        self.audio_list = audio_list.AudioListWidget(self)
        self.exiting.connect(self.audio_list.exiting)
        self.navigation_menu.menuItemClicked.connect(self.audio_list.load_audio)

        self.download_manager = downloadform.AudioDownloadWidget(self)
        self.exiting.connect(self.download_manager.exiting)
        self.audio_list.itemChoosed.connect(self.download_manager.add)
        self.download_manager.updateState.connect(self.audio_list.updateState)

        self.downloadButton.clicked.connect(self.download_manager.show)

    def closeEvent(self, event):
        self.exiting.emit()
        event.accept()