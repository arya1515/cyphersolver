import sys
sys.argv=[sys.argv[0]]+sys.argv[1:]
from lattice import decode
A=dict(d='e',qq='que',hk='i',do='e|-',b='e|p',lt='vous',eq='-',sl='-',et='t',mJ='i|m',a1='n',x1='e',TT='pour|n',G='t',R='r',ss='o|g',z='a|p',S='a|s',La='d',mu='u',Lo='l|-',io='i',c='s',sh='i|et',f='ff',C='o|h',at='a|e|-',B='l',g='t|o',eta='a|n',sig='l',zs='s|e',lam='u|v',k='i',zy='d|-',pi='h',Rx='d|-',m='c',cg='o|g',Vb='qui',th='m',yn='n',s3='r|s',star='x',E='c|f',pl='bien',plus='y|s',w='v|u',T='t',N='o',pour='pour|-',que='que|-',est='est|-',en='en|-',bien='bien')
A.update({'9':'n|m','3':'c|e','4':'f'})
for ln in open('c390_p139_v3.txt',encoding='utf-8'):
    if ln.startswith('#') or not ln.strip(): continue
    c=[A.get(t,'-').split('|') for t in ln.split()]
    r=decode(c,beam=2000)
    print(r[0][1]); print(r[1][1])
