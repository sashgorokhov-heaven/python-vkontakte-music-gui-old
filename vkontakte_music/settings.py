# coding=utf-8
import os
import string

CLIENT_ID = '5416726'
SCOPE = ['groups', 'audio', 'friends']

WINDOW_TITLE = 'Vkontakte Music'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CACHE_FILENAME = os.path.join(BASE_DIR, '.cache.shelve')

QTDESIGNER_SOURCES = os.path.join(BASE_DIR, 'vkontakte_music', 'qtdesigner')
QTDESIGNER_GENERATED = os.path.join(BASE_DIR, 'vkontakte_music', 'generated')


REPLACE_CHAR = '#'
VALID_CHARS = set(string.printable) - set('\*:"<>|/')
#VALID_CHARS = VALID_CHARS.union(set((chr(i) for i in range(ord(u'А'), ord(u'я')+1))))