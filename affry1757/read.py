import json,sys
from view import load
k=json.load(open('key_M.json',encoding='utf8'))
def dec(r): return ' '.join(k.get(str(x),'['+str(x)+']') for x in load('U')[r])
if __name__=='__main__':
    for r in sys.argv[1:]: print('==',r); print(dec(r))
