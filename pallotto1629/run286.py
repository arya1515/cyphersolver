from solve import *
C,meta=load_doc('decode/R286.txt')
print('digits',len(C))
crib="Ho ricevuta la risposta datami in scritto all'instanza fatta da me col viglietto del quale mandai copia con le passate Non solo persistono ne primi sensi ma mostrano essersi affatto dimenticati di quello che"
P=norm_plain(crib)
print('plain',len(P),P[:60])
table={}
for it in range(6):
    sc,ops,used=align(C[:len(P)*2+60],P,table)
    table,conf=build_table(ops)
    good=sum(1 for k,_,_,_ in ops if k=='S')
    print('iter',it,'score %.1f'%sc,'digits used',used,'subs',good,'table',len(table))
dec=''.join(l if k=='S' else ('['+c+']' if k=='N' else l.lower()) for k,c,l,_ in ops)
print(dec)
print(sorted(table.items()))
