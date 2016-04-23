__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

import tempfile, pickle, os.path, threading

CACHEFILE = "cache"
__cache = None
__lock = threading.Lock()

if not os.path.exists(CACHEFILE):
    pickle.dump(dict(), open(CACHEFILE, 'wb'))

__cache = pickle.load(open(CACHEFILE, 'rb'))
__temp_session = dict()

#Держит кэшированные файлы в запикленном словаре "имя файла":bytes файла.
#get возвращает имя временного файла

def clear():
    with __lock:
        pickle.dump(dict(), open(CACHEFILE, 'wb'))
        global __cache
        del __cache
        __cache = dict()

def exists(file):
    return file in __cache

def get_file(file):
    with __lock:
        b = get_bytes(file)
        tf = tempfile.NamedTemporaryFile('wb', delete=False, suffix=os.path.splitext(file)[1])
        with tf:
            tf.write(b)
        return tf.name

def get_bytes(file):
    if not exists(file):
        raise KeyError
    return __cache[file]

def put_bytes(b, file):
    with __lock:
        __cache[file] = b
        pickle.dump(__cache, open(CACHEFILE, 'wb'))

def put_file(file, name=None):
    with open(file, 'rb') as f:
        if name:
            put_bytes(f.read(), name)
        else:
            put_bytes(f.read(), file)
