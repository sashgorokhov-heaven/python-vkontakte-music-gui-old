__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

import threading

def showmessage(msg):
    print(str(msg))

class VkAudio:
    def __init__(self, audioobject):
        self.__object = audioobject

    def id(self):
        return self.__object['id']

    def getObject(self):
        return self.__object

    def artist(self):
        return self.__object['artist']

    def title(self):
        return self.__object['title']

    def url(self):
        return self.__object['url']

    def duration(self, parsed=False):
        if parsed:
            mins = (self.__object['duration'] // 60)
            secs = self.__object['duration']-60*(self.__object['duration'] // 60)
            return (mins, secs)
        return self.__object['duration']

    def __getattr__(self, item):
        return self.__object[item]

    def __str__(self):
        return '[{0}] {} - {}'.format(':'.join(self.duration(True)), self.artist(), self.title())


#колеса
class Buffer:
    def __init__(self):
        self.__lock = threading.Lock()
        self.__buffer = dict()

    def get(self, key):
        with self.__lock:
            return self.__buffer[key]

    def put(self, key, value):
        with self.__lock:
            self.__buffer[key] = value

    def remove(self, key):
        with self.__lock:
            return self.__buffer.pop(key)

    def __contains__(self, item):
        with self.__lock:
            return item in self.__buffer