import json,re,sys,glob,decode
K=json.load(open(sys.argv[1])); pat=sys.argv[2]
FILES=sorted(glob.glob('decode/DOC*.txt'))+sorted(glob.glob('trans/R*.txt'))
n=0
for f in FILES:
  t=open(f,encoding='utf-8-sig').read(); t=re.sub(r'#.*','',t)
  for p in re.split(r'<CLEARTEXT[^>]*>',t):
    for chunk in re.split(r'[,%]',p):
      d=re.sub(r'[^0-9]','',chunk).replace('5','').replace('8','')
      if len(d)<2: continue
      tk=[x for x in decode.align1(d)]
      txt='';pos=[]
      for i,x in enumerate(tk):
        v=K.get(x,'?') if not x.startswith('*') else '{'+x[1:]+'}'
        pos+= [i]*len(v); txt+=v
      for m in re.finditer(pat,txt):
        a,b=pos[m.start()],pos[m.end()-1]
        print(f[-12:-4],' '.join(f'{x}:{K.get(x,x)}' for x in tk[max(0,a-3):b+4]))
        n+=1
        if n>int(sys.argv[3] if len(sys.argv)>3 else 12): sys.exit()
