import re,glob,collections
tot=0; unres=collections.Counter(); resolved=0
pairs=[]
for f in sorted(glob.glob('lasry/364D-*.txt')):
    L=open(f,encoding='utf-8',errors='replace').read().splitlines()
    for i in range(len(L)-1):
        a,b=L[i],L[i+1]
        if not (a.rstrip().endswith('|') and b.rstrip().endswith('|')): continue
        if not re.match(r'^\s*[\d]',a): continue
        # column boundaries from cipher line
        cols=[m.start() for m in re.finditer(r'\S+',a)]
        # merge: token start positions where previous char is start-of-col
        starts=[]; prev_end=-2
        for m in re.finditer(r'\S+',a):
            if m.start()>prev_end+1: starts.append(m.start())
            prev_end=m.end()-1
        starts.append(len(a))
        for j in range(len(starts)-1):
            ct=a[starts[j]:starts[j+1]].strip()
            pt=b[starts[j]:starts[j+1]].strip() if starts[j]<len(b) else ''
            if ct in ('|',''): continue
            tot+=1
            pairs.append((f,ct,pt))
            if pt.endswith('?') or pt=='' or pt.startswith('<'):
                unres[ct]+=1
            else: resolved+=1
print('364D total cipher tokens:',tot,' resolved:',resolved,' unresolved:',tot-resolved,
      ' = %.1f%% read'%(100*resolved/tot))
print('\ndistinct unresolved groups:',len(unres))
for g,n in unres.most_common(40): print('  %-8s %d'%(g,n))
