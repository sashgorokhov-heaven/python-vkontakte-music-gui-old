__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

try:
    import modules.testimports
except ImportError:
    #logerror
    exit(-1)

from modules import constants, util
from modules.gorokhovlibs.vk import accesstokener, api

access_token = user_id = expires = None
if not accesstokener.good():
    from modules.gorokhovlibs.vk.qt import auth
    auth.DESCTIPTION = constants.application_title
    access_token, user_id, expires = auth.show_browser(constants.application_id, constants.permissions_scope)
    if not access_token:
        exit(-1)
    accesstokener.new(access_token, user_id, expires)
else:
    access_token, user_id, expires = accesstokener.get()

if not access_token or (access_token and not api.test_connection(access_token)):
    #logerror
    exit(-1)

from modules.forms import mainform
from PyQt4 import QtGui

vkapi = api.VKApi(access_token)
app = QtGui.QApplication([])
mform = mainform.MainForm(access_token)
mform.show()
app.exec_()
