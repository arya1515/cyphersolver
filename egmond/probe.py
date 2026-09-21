"""Exploratory substitution probe, not a verified transcription or reading."""
import pathlib, json, sys, numpy as np
ROOT=pathlib.Path(__file__).resolve().parent
ALPHA='abcdefghiklmnopqrstuvxyz'
language=sys.argv[3] if len(sys.argv)>3 else 'fr'
model_path=ROOT.parent/'gallica_sweep/mondoucet/f1573/fr5.npy'
if language=='de':
    ALPHA='abcdefghiklmnopqrstuwxyz'
    model_path=ROOT.parent/'kurtz1639/de_early5.npy'
elif language=='it':
    ALPHA=json.loads((ROOT.parent/'pallotto1629/it_clean5.json').read_text())['alpha']
    model_path=ROOT.parent/'pallotto1629/it_clean5.npy'
K=len(ALPHA)
homophones=len(sys.argv)>4 and sys.argv[4]=='homophones'
input_name=sys.argv[2] if len(sys.argv)>2 else 'opening_provisional.txt'
raw=(ROOT/input_name).read_text()
variant=sys.argv[1] if len(sys.argv)>1 else 'separate'
if variant in ('dd','both'): raw=raw.replace('dd','D')
if variant in ('ee','both'): raw=raw.replace('ee','E')
if variant=='reverse': raw=raw[::-1]
if variant=='ce': raw=raw.replace('ee','ce')
if variant=='composites':
    raw='\n'.join(''.join(line.split()).replace('DD','J').replace('CE','M') for line in raw.splitlines())
if variant=='address_composites': raw=raw.replace('jj','U').replace('mm','W')
if variant=='ligatures':
    raw='\n'.join(''.join(line.split()).replace('DD','J').replace('CE','M').replace('FA','U').replace('F+','U').replace('O','') for line in raw.splitlines())
if variant in ('nullD','nullDCE'):
    raw='\n'.join(''.join(line.split()).replace('DD','') for line in raw.splitlines())
    if variant=='nullDCE': raw=raw.replace('CE','')
symbols=sorted(set(raw)-set(' \n\r\t'))
ct=np.array([symbols.index(x) for x in raw if x in symbols],dtype=np.int64)
lp=np.load(model_path).reshape(-1)
assert len(lp)==K**5
prior=np.exp(lp.reshape(-1,K)).mean(axis=0)
prior/=prior.sum()
def score(ct,key,lp):
    p=key[ct]
    q=((((p[:-4]*K+p[1:-3])*K+p[2:-2])*K+p[3:-1])*K+p[4:])
    value=float(lp[q].sum())
    if homophones:
        freq=np.bincount(p,minlength=K).astype(float)/len(p)
        positive=freq>0
        value-=2*len(p)*float((freq[positive]*np.log(freq[positive]/prior[positive])).sum())
    return value
def solve(ct,lp,ns,seed):
    np.random.seed(seed)
    key=np.random.permutation(K)
    cur=score(ct,key,lp); best=cur; bk=key.copy()
    for it in range(40000):
        a=np.random.randint(K); b=np.random.randint(K)
        x=key[a]; y=key[b]
        key[a]=y; key[b]=x
        if homophones and np.random.random()<0.5:
            key[a]=np.random.randint(K);key[b]=y
        new=score(ct,key,lp)
        temp=5*(1-it/40000)+0.15
        if new>cur or np.random.random()<np.exp((new-cur)/temp): cur=new
        else: key[a]=x; key[b]=y
        if cur>best: best=cur; bk=key.copy()
    return best,bk
best=-1e20
for seed in range(12):
    s,k=solve(ct,lp,len(symbols),seed)
    if s>best:
        best=s
        key={x:ALPHA[int(v)] for x,v in zip(symbols,k)}
        reading=''.join(key.get(c,c) for c in raw)
        result={'score':float(s),'tokens':len(ct),'symbols':len(symbols),'key':key,'reading':reading,'caution':'Unverified exploratory solver result on provisional transcription.'}
        result['input_file']=input_name
        result['variant']=variant
        result['language']=language
        suffix='' if language=='fr' else '_'+language
        if homophones: suffix+='_homophones'
        (ROOT/('probe_result_'+pathlib.Path(input_name).stem+'_'+variant+suffix+'.json')).write_text(json.dumps(result,indent=2))
        print(seed,s,reading,flush=True)
