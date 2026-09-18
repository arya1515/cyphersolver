import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from show17 import T
from family import code2ch
def show(s, a):
    sy = [s[i:i+2] for i in range(0, len(s), 2)]
    out = []
    for i in range(a, len(sy)-1, 2):
        c = '%02d%02d' % (T[sy[i]], T[sy[i+1]]) if sy[i] in T and sy[i+1] in T else '????'
        out.append(sy[i]+sy[i+1]+'='+c+code2ch.get(c, '□'))
    return ' '.join(out)
if __name__ == '__main__':
    for a in (0, 1): print(a, show(sys.argv[1], a))
