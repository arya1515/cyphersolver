import json,re,collections
seq=json.load(open('seq.json'))
extra=dict(l.split(' = ') for l in open('key_extra.txt').read().strip().splitlines())
nom=[c for _,c,p in seq if re.fullmatch(r'1\d{3}',c)]
two=[(c,p) for _,c,p in seq if not re.fullmatch(r'1\d{3}',c)]
unread2=sum(1 for c,p in two if (not p or p.endswith('?')) and c!='7')
res=sum(1 for c in nom if c in extra)
print('tokens',len(seq),'nomenclator tokens',len(nom),'distinct',len(set(nom)))
print('valued here',res,'tokens',len(set(c for c in nom if c in extra)),'groups')
print('two-digit tokens unread',unread2)
print('read before %.1f%%  now %.1f%%'%(100*(len(seq)-len(nom)-unread2)/len(seq),100*(len(seq)-len(nom)+res-unread2)/len(seq)))
