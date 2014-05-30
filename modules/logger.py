__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

LOGFILE = 'log.txt'

from modules import constants

with open(LOGFILE, 'w') as f:
    f.write('Initializing version={}\n'.format(constants.version))

def write(msg):
    with open(LOGFILE, 'a') as f:
        f.write(str(msg)+'\n')