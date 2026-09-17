import re,sys
sys.path.insert(0,'.')
from key import decode
for f in sys.argv[1:]:
    print('=====',f)
    for line in open(f):
        line=line.strip()
        if not line or line.startswith('#'): continue
        line=re.sub(r'(\d)[.;]',r'\1',line)
        print(decode(line))
