import sys
V=dict(zx='s',Sr='-',gl='f',x4='x',blot='?',d='e',qq='que',hk='i',do='-',b='e',lt='vous',eq='-',sl='-',et='t',mJ='i',**{'9':'n'},a1='n',x1='e',TT='pour',G='t',R='r',ss='o',z='a',S='a',La='d',mu='u',Lo='l',io='i',c='s',sh='y',f='ff',**{'3':'c'},C='o',at='g',B='l',g='o',eta='a',sig='l',zs='s',lam='u',k='i',zy='-',pi='h',Rx='d',m='c',cg='g',Vb='qui',th='m',yn='-',ds='?',s3='r',ll='ss',star='b',E='c',**{'4':'f'},pl='bien',plus='y',md='ce',Sao='?',**{'as':'?'},RR='?',w='v',T='t',gb='?',N='o',dar='?',pour='[pour]',que='[que]',est='[est]',en='[en]',bien='[bien]')
V.update(E='f',g='u',gl='m',N='l',ll='[plus]',sh='y',T='y',Lo='-')
for ln in open(sys.argv[1],encoding='utf-8'):
    if ln.startswith('#') or not ln.strip(): continue
    print(''.join(V.get(t,'{%s}'%t).replace('-','') for t in ln.split()))
