M=dict(yh='j|i|y|-',do='-',k='i|-',xy='e',lt='vous',gt='nous',d='e',La='d',u='u|v|n|c',c='o',tt='y|n|i|-',bs='e|p',mn='la',sc='lettre',qq='que',est='-|est',
maue='-|mais|a',R='r|b|-',t7='y|t',a1='n|g',cs='s|c|f|-',io='i',z='a|p',G='t',S='a|ont|e|-',lam='u|v|-',r2='r|-',beta='g|l|-',tu='faict',g='m|g|y|-',x='e|z|d|r',
dd='n|q|s|-',Y='d|y',m='i|c',**{'3f':'o|s','3':'c|o','9':'n','5':'r|s','8':'luy|b|d','#':'i|est','6':'l','7':'y|t'},tl='e|-',N='m|p',Yv='s|v|u',eps='e|t',b='e|p',Ls='-',ss='q|p|-',Lo='-',ll='g|n|u|-',eq='-',
plus='-|plus',sx='s|x',ca='faire',V='s',E='c',w='u|v',piz='puis|h',a_='a',ff='a',x8='d|b|luy',st='x|c|s',fc='t|f',Fj='f|t|s|r',pi='h',Fl='f|t|s',Sl='a|s|-',sl='-',W='b|p|d',at='par',pl='bien',f='f|s',gt_='nous',
**{'+':'vostre','a-':'g|a|n'},dl='-')
M['del']='com|dit|ont|-'
out=[]
for ln in open('c392_raw.txt',encoding='utf-8'):
    t=[]
    for tok in ln.split():
        v=M[tok]; t.append(f'{tok}={v}')
    out.append(' '.join(t))
open('c392_p231.txt','w',encoding='utf-8').write('\n'.join(out)+'\n')
