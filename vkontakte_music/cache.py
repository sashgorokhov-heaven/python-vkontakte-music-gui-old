import shelve
from datetime import timedelta, datetime

from vkontakte_music import settings
import time
import logging

logger = logging.getLogger(__name__)


class cache(object):
    __instance__ = None
    closed = False

    def __init__(self):
        self.shelve = shelve.open(settings.CACHE_FILENAME)

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            instance = super(cache, cls).__new__(cls, *args, **kwargs)
            cls.__instance__ = instance
        return cls.__instance__

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def _get_item(self, key):
        if key in self.shelve:
            value, valid_thru = self.shelve[key]
            if valid_thru is not None:
                if valid_thru > time.time():
                    return value
                else:
                    logger.debug('Requested %s but it is outdated: %s', key, valid_thru)
                    self.shelve.pop(key, None)
                    return None
            return value
        return None

    def _set_item(self, key, value, timeout=None):
        if isinstance(timeout, int):
            timeout = time.time() + timeout
        elif isinstance(timeout, timedelta):
            timeout = time.time() + timeout.seconds * 1000
        elif isinstance(timeout, datetime):
            timeout = int(time.mktime(timeout.timetuple()))
        self.shelve[key] = value, timeout
        logger.debug('Stored %s for %s', key, timeout)

    def get(self, key, default=None):
        return self._get_item(key) or default

    def set(self, key, value, timeout=None):
        self._set_item(key, value, timeout)

    def exists(self, key):
        return key in self.shelve and self._get_item(key)

    def close(self):
        self.closed = True
        self.shelve.close()
        self.__class__.__instance__ = None

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def get(key, default=None):
    with cache() as _cache:
        return _cache.get(key, default)


def set(key, value, timeout=None):
    with cache() as _cache:
        return _cache.set(key, value, timeout)


def exists(key):
    with cache() as _cache:
        return _cache.exists(key)


def sync():
    with cache() as _cache:
        _cache.shelve.sync()
