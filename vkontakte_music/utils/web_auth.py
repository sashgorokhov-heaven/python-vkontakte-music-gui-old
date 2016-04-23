import logging

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from PySide import QtCore, QtWebKit, QtGui
from vkontakte_music import settings

logger = logging.getLogger(__name__)

class WebAuthWindow(QtWebKit.QWebView):
    data = None
    url = 'http://oauth.vk.com/oauth/authorize?redirect_uri=oauth.vk.com/blank.html&' \
          'response_type=token&' \
          'client_id={client_id}&' \
          'scope={scope}&' \
          'display=wap&' \
          'revoke=1'

    def __init__(self, client_id, scope):
        super(WebAuthWindow, self).__init__()
        url = self.url.format(client_id=client_id, scope=','.join(scope))
        self.setWindowTitle(settings.WINDOW_TITLE)
        self.urlChanged.connect(self.urlChangedSlot)
        logger.debug('Loading url %s', url)
        self.load(QtCore.QUrl(url))

    def urlChangedSlot(self, url):
        logger.debug('Url changed to: %s', url)
        url = url.toString()
        if urlparse(url).path != '/blank.html':
            return
        self.data = {i[0]: i[1] for i in map(lambda i: i.split("="), urlparse(url).fragment.split('&'))}
        self.close()


def show_browser(client_id, scope):
    logger.info('Showing browser')
    app = QtGui.QApplication([])
    browser = WebAuthWindow(client_id, scope)
    browser.show()
    app.exit(app.exec_())
    app.quit()
    logger.debug('Browser closed with data: %s', browser.data)
    return browser.data