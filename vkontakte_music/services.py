import pyvkontakte
import logging
from vkontakte_music import cache
from vkontakte_music.utils.vkontakte import AsyncVkontakteApi

logger = logging.getLogger(__name__)

_api = None

def api():
    """
    :rtype: AsyncVkontakteApi
    """
    global _api
    if _api is None:
        access_token = cache.get('access_token', None)
        if not access_token:
            logger.warning('Requested api but access token is None')
            raise ValueError('Access token is none')
        _api = AsyncVkontakteApi(access_token)
    return _api
