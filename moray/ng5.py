import numpy as np,re,sys
from lm import clean
def build(files,out='ng5.npy'):
    text=''
    for f in files: text+=clean(open(f,encoding='utf-8',errors='ignore').read())
    text=re.sub(r' +','',text)
    idx=np.frombuffer(text.encode(),dtype=np.uint8).astype(np.int64)-97
    n=len(idx)
    c5=np.bincount(idx[:-4]*456976+idx[1:-3]*17576+idx[2:-2]*676+idx[3:-1]*26+idx[4:],minlength=26**5).astype(np.float32)
    c4=np.bincount(idx[:-3]*17576+idx[1:-2]*676+idx[2:-1]*26+idx[3:],minlength=26**4).astype(np.float32)
    c3=np.bincount(idx[:-2]*676+idx[1:-1]*26+idx[2:],minlength=26**3).astype(np.float32)
    c2=np.bincount(idx[:-1]*26+idx[1:],minlength=26**2).astype(np.float32)
    # conditional probs with interpolation: p(x|ctx4)
    ctx4=c5.reshape(26**4,26).sum(1); ctx3=c4.reshape(26**3,26).sum(1); ctx2=c3.reshape(26**2,26).sum(1); ctx1=c2.reshape(26,26).sum(1)
    p1=(np.bincount(idx,minlength=26)+1)/(n+26)
    p2=(c2.reshape(26,26)+ 5*p1[None,:])/(ctx1[:,None]+5)
    p3=(c3.reshape(676,26)+5*np.tile(p2,(26,1)))/(ctx2[:,None]+5)
    p4=(c4.reshape(17576,26)+5*np.tile(p3,(26,1)))/(ctx3[:,None]+5)
    p5=(c5.reshape(456976,26)+5*np.tile(p4,(26,1)))/(ctx4[:,None]+5)
    lp=np.log(p5).astype(np.float32).reshape(-1)
    np.save(out,lp); print(len(text)); return lp
import os
def load(): return np.load(os.environ.get('NG5','ng5.npy'))
def score(tab,p):
    q=p[:-4]*456976+p[1:-3]*17576+p[2:-2]*676+p[3:-1]*26+p[4:]
    return float(tab[q].sum())
if __name__=='__main__':
    files=sys.argv[1:] or ['corpus/diurnalofremarka00thom.txt','corpus/registerprivyco01coungoog.txt','corpus/csp_scots.txt']
    tab=build(files)
    def s(t): return score(tab,np.frombuffer(t.encode(),dtype=np.uint8).astype(np.int64)-97)
    for t in ['i'*45,'thelordregentisgraceanduthernoblemenquhilkwe','quhilkwecouldnochtsuffernorthairisnafaltisin','tnesenantairneteneandertationentinthesteitta']: print(round(s(t),1),t)
