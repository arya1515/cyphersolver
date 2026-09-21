# Assign each word-group to a crib word (or leave unassigned) with a consistent homophonic map sign->letter.
import re,sys
tr=open(r'C:/Users/dbour/cypher/norreys1567/transcription.txt',encoding='utf8').read()
groups=[];cur=None
for l in tr.splitlines():
    m=re.match(r'\[(N\d+)',l)
    if m: cur=m.group(1);continue
    m=re.match(r'(\d+): (.*)',l)
    if m and not m.group(2).startswith('#') and cur not in ('N670604','N670710','N670706'):
        toks=m.group(2).split()
        if len(toks)>=3: groups.append((cur+'.'+m.group(1),toks))
crib={
'N680206':"lesley brother earl rothes papists scotland letters french king realms england conspired enterprise regent queen scots liberty stayed answer pension governor calais victuals catholic footmen horse gascony navarre territories towns garrison siege blois chatillon prisoners captain frenchmen scots prince conde camp servant post dieppe hamiltons",
'N680209':"determined controversy battle calais expedient peace protestants ruin prince conde admiral marseilles queen mother strozzi neighbour close garden door fields key house lease king sister",
'N680224':"intelligence practised houses controversy marriage guise marry prince eldest daughter andelot son duke sister cecil faithful favourer protestants france admiral friendship suitor queen money pay almains",
'N680309':"peace concluded soldiers hope war hostility prisoners durance executed montmorency treaty longjumeau king gentlemen pope emperor catholic swiss determination secret town payment reiters francs cardinal bourbon dukes longueville caution attempt scotland delivery queen letters marseilles poor men galleys",
}
words={k:sorted(set(v.split())) for k,v in crib.items()}
best=[0,None]
order=sorted(range(len(groups)),key=lambda i:-len(groups[i][1]))
def rec(k,mp,asg,score):
    if score+sum(1 for j in order[k:])<=best[0]: return
    if k==len(order):
        best[0]=score;best[1]=dict(asg);print(score,asg,flush=True);return
    i=order[k];gid,toks=groups[i];let=gid.split('.')[0]
    for w in words[let]:
        if len(w)!=len(toks): continue
        new={};ok=True
        for t,c in zip(toks,w):
            v=mp.get(t,new.get(t))
            if v is None: new[t]=c
            elif v!=c: ok=False;break
        if ok:
            mp.update(new);asg[gid]=w
            rec(k+1,mp,asg,score+1)
            for t in new: del mp[t]
            del asg[gid]
    rec(k+1,mp,asg,score)
rec(0,{},{},0)
