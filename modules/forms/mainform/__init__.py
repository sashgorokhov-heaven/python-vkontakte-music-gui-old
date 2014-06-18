from modules.forms.mainform.components.audiolist import AudioList

__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from PySide import QtCore, QtGui
from modules.forms.mainform.components.navmenu import NavigationMenu
from .ui import Ui_Form
from modules import constants
from modules.util import Dispatcher


class MainForm(QtGui.QWidget, Ui_Form):
    exiting = QtCore.Signal()

    def __init__(self, api):
        super().__init__()
        self.api = api
        self.setupUi(self)
        self.setWindowTitle(str(constants.application_title))

        self._dispatcher = Dispatcher()
        self.exiting.connect(self._dispatcher.terminate)
        self._dispatcher.start()

        self.navigation_menu = NavigationMenu(self, self.api, self._dispatcher)
        self.exiting.connect(self.navigation_menu.exiting)

        self.audio_list = AudioList(self, self.api)
        self.exiting.connect(self.audio_list.exiting)
        self.navigation_menu.menu_itemclicked.connect(self.audio_list.load_audio)

        #self.download_manager = downloadform.AudioDownloadWidget(self)
        #self.exiting.connect(self.download_manager.exiting)
        #self.audio_list.itemChoosed.connect(self.download_manager.add)
        #self.download_manager.updateState.connect(self.audio_list.updateState)

        #self.downloadButton.clicked.connect(self.download_manager.show)

    def closeEvent(self, event):
        self.exiting.emit()
        event.accept()