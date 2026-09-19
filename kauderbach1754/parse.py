import re,glob,collections
def segs(f):
    t=open(f,encoding='utf-8-sig').read()
    t=re.sub(r'#.*','',t); t=re.sub(r'<[^>]*>','|',t)
    t=re.sub(r'[^0-9|]','',re.sub(r'[,.%?A-Za-z_]','|',t))
    return [s for s in t.split('|') if s]
if __name__=='__main__':
  for f in sorted(glob.glob('decode/DOC*.txt')):
    S=segs(f); print(f, [len(s) for s in S])
