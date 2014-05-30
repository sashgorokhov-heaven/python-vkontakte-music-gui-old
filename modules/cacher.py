__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

import tempfile, pickle, os.path

CACHEFILE = "cache"
__cache = None

if not os.path.exists(CACHEFILE):
    pickle.dump(dict(), open(CACHEFILE, 'wb'))

__cache = pickle.load(open(CACHEFILE, 'rb'))
__temp_session = dict()

#Держит кэшированные файлы в запикленном словаре "имя файла":bytes файла.
#get возвращает имя временного файла

def clear():
    pickle.dump(dict(), open(CACHEFILE, 'wb'))

def exists(file):
    return file in __cache

def get_file(file):
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
    __cache[file] = b

def put_file(file):
    with open(file, 'rb') as f:
        put_bytes(f.read(), file)
