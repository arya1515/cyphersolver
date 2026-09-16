import solver, re, sys
key={}
for line in open('control_key.txt',encoding='utf-8'):
    x,u=line.rstrip('\n').split('\t'); key[int(x)]=('' if u.startswith('<null') else u)
segs=solver.parse('control.txt'); low,high=solver.inventory(); pri=solver.unit_prior(low+high)
S=solver.Solver(segs,low,high,pri); S.map={c:key[c] for c in S.codes}
S.segscore=[S.score_seg(i) for i in range(len(segs))]; S._struct=S.structural()
print('TRUE-KEY objective', round(S.total(),1), 'LAMBDA',solver.LAMBDA,'PRIORW',solver.PRIORW)
