import os

CLIENT_ID = '5416726'
SCOPE = ['groups', 'audio', 'friends']

WINDOW_TITLE = 'Vkontakte Music'

CACHE_FILENAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.cache.shelve')

QTDESIGNER_SOURCES = os.path.join(os.path.dirname(__file__), 'qtdesigner')
QTDESIGNER_GENERATED = os.path.join(os.path.dirname(__file__), 'generated')