import logging

logging.basicConfig(level=logging.DEBUG, stream=None)

logger = logging.getLogger(__name__)


def main():
    from PySide import QtGui
    from vkontakte_music.utils.web_auth import show_browser
    from vkontakte_music.forms.main_form import MainForm
    from vkontakte_music import settings, cache

    logger.debug('Application initialized')
    access_token = cache.get('access_token')
    if not access_token:
        data = show_browser(settings.CLIENT_ID, settings.SCOPE)
        if not data or data and 'access_token' not in data:
            logger.warning('Access token not in browser data: %s', data)
            return
        access_token = data['access_token']
        cache.set('access_token', access_token, int(data['expires_in']))
    else:
        logger.info('Got access token from cache')

    logger.info('Showing main window')
    app = QtGui.QApplication.instance() or QtGui.QApplication([])
    main_form = MainForm()
    main_form.show()
    app.exec_()

if __name__ == '__main__':
    main()