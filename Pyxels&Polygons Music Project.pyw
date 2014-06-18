__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from modules import logger

try:
    import modules.testimports
except ImportError as e:
    logger.write('Import error: {}'.format(str(e)))
    exit(-1)

from modules import constants, vk
from modules.vk import api, accesstokener

access_token, user_id, expires = vk.quickauth_qt(constants.application_id, constants.permissions_scope)

try:
    if not access_token or (access_token and not api.test_connection(access_token)):
        logger.write('Empty token or invalid token')
        accesstokener.clear()
        exit(-1)
except Exception as e:
    logger.write('Seems like internet connection error: {}'.format(e))
    exit(-1)

from modules.forms import mainform
from PySide import QtGui

app = QtGui.QApplication([])
mform = mainform.MainForm(api.VKApi(access_token))
mform.show()
app.exec_()