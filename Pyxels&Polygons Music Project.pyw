__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

from modules import logger

try:
    import modules.testimports
except ImportError as e:
    logger.write('Import error: {}'.format(str(e)))
    exit(-1)

from modules import constants, util
from modules.gorokhovlibs.vk import accesstokener, api

access_token = user_id = expires = None
if not accesstokener.good():
    from modules.gorokhovlibs.vk.qt import auth
    from modules import cacher
    auth.DESCTIPTION = constants.application_title
    access_token, user_id, expires = auth.show_browser(constants.application_id, constants.permissions_scope)
    if not access_token:
        exit(-1)
    accesstokener.new(access_token, user_id, expires)
    cacher.clear()
else:
    access_token, user_id, expires = accesstokener.get()

try:
    if not access_token or (access_token and not api.test_connection(access_token)):
        logger.write('Empty token or invalid token')
        accesstokener.clear()
        exit(-1)
except Exception as e:
    logger.write('Seems like internet connection error')
    exit(-1)

from modules.forms import mainform
from PySide import QtGui

app = QtGui.QApplication([])
#from modules import waiter
#waiter.show()
mform = mainform.MainForm(api.VKApi(access_token))
mform.show()
app.exec_()
