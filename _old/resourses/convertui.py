__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

import os, time
os.startfile('convertui.cmd')

files = [
    r'..\modules\forms\downloadform\ui.py',
    r'..\modules\forms\mainform\ui.py',
    r'..\modules\forms\mainform\components\audiolist\components\audiolistitemwidget\ui.py',
    r'..\modules\forms\downloadform\components\audiolist\components\audiolistitemwidget\ui.py'
]

time.sleep(3)

for file in files:
    with open(file, 'r') as f:
        lines = f.read().split('\n')
    lines.reverse()
    parsed = list()
    found = False
    for line in lines:
        if line == 'import resourses_rc':
            if found:
                continue
            found = True
            parsed.append('import resourses.resourses_rc')
        else:
            parsed.append(line)
    parsed.reverse()
    with open(file, 'w') as f:
        f.write('\n'.join(parsed))