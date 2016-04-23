import logging

logging.basicConfig(level=logging.DEBUG, stream=None)

logger = logging.getLogger(__name__)


def main():
    from vkontakte_music.utils.web_auth import show_browser
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
        logging.info('Got access token from cache')

if __name__ == '__main__':
    main()