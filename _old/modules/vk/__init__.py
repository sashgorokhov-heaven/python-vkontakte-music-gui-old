__author__ = "Alexander Gorokhov"
__email__ = "sashgorokhov@gmail.com"

from . import accesstokener
import pyvkontakte

_noqt = False
try:
    import PySide
except ImportError:
    _noqt = True

def quickauth_qt(appid, permissions_scope=list()):
    access_token = user_id = expires_in = None
    if not accesstokener.good():
        from .qt.auth import show_browser
        access_token, user_id, expires_in = show_browser(appid, permissions_scope)
        if access_token:
            accesstokener.new(access_token, user_id, expires_in)
    else:
        access_token, user_id, expires_in = accesstokener.get()
    return access_token, user_id, expires_in


def quickauth_nogui(login, passwd, appid, permissions_scope=list()):
    access_token = user_id = expires_in = None
    if not accesstokener.good():
        data = auth(login, passwd, appid, permissions_scope)
        if 'access_token' in data:
            accesstokener.new(**data)
    else:
        access_token, user_id, expires_in = accesstokener.get()
    return access_token, user_id, expires_in


class VKAuthError(Exception): pass

def auth(login, passwd, appid, scope):
    return pyvkontakte.auth(login, passwd, appid, scope)

# :)
if _noqt:
    del globals()['quickauth_qt']
