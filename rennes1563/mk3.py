M=dict(yh='j|-',do='-',k='i',xy='e',lt='vous',gt='nous',d='e',La='d',u='v|u',c='o',tt='y',bs='e',mn='la',sc='lettre',qq='que',est='-',
maue='-|mais',R='r',t7='y|t',a1='n',cs='s',io='i',z='a',G='t',S='a',lam='u|v',r2='p',beta='l|g',tu='faict',g='m|et',x='e|z',
dd='nn|et',Y='d',tl='-|e',N='l',Yv='d',eps='e|t',b='e',Ls='-',ss='q|p',Lo='-',ll='-|n',eq='-',plus='-',sx='b|c',ca='faire',V='s',E='c',w='v|u',
piz='puis|h',ff='a',x8='d|b',st='c',fc='t|f',Fj='u|r',pi='h',Fl='f|s',Sl='a|s',sl='-',W='ss|b',at='par',pl='bien',f='f|s',
**{'3f':'o|s','3':'c','9':'n','5':'r|s','8':'luy','#':'i|est','6':'l','7':'y','+':'f','a-':'g|a'})
M['m']='i|c'; M['del']='com|dit|ont'
out=[]
for ln in open('c392_raw.txt',encoding='utf-8'):
    out.append(' '.join(f'{t}={M[t]}' for t in ln.split()))
open('c392_p231n3.txt','w',encoding='utf-8').write('\n'.join(out)+'\n')
