__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from modules.gorokhovlibs.qt import qtwindow
import os.path
from PyQt4 import QtGui, QtCore, uic

class AudioDownloadWidgetItem(QtGui.QWidget):
    def __init__(self, oobject, parent, item):
        self.object = oobject
        self.parent = parent
        self.item = item
        super().__init__()
        uic.loadUi(os.path.join('resourses', 'audiodownloadwidget.ui'), self)

        self.item.setSizeHint(self.sizeHint())

        setattr(self, 'elements', qtwindow._Elements(qtwindow.BaseQtWindow._set_childs(None, self)))

        self.elements.titleLabel.setText(str(oobject['title']))
        self.elements.artistLabel.setText(str(oobject['artist']))

class AudioDownloadWidget(qtwindow.BaseQtWindow):
    def __init__(self, parent):
        super().__init__(self, os.path.join('resourses', 'loadform.ui'))
        self.parent = parent
        self.audiolist = list()
        self.hide()

    def closeEvent(self, event):
        self.hide()

    def show(self):
        self._setVisible(True)

    def hide(self):
        self._setVisible(False)

    def _setVisible(self, visible):
        self.visible = visible
        self.setVisible(visible)

    def _set_connections(self):
        pass

    def addAudio(self, oobject):
        item = QtGui.QListWidgetItem()
        widget = AudioDownloadWidgetItem(oobject, self, item)
        self.elements.downloadListWidget.addItem(item)
        self.elements.downloadListWidget.setItemWidget(item, widget)
        self.audiolist.append(oobject)