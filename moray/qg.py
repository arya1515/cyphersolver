import numpy as np,re,pickle,os,math
from lm import clean
AL='abcdefghijklmnopqrstuvwxyz'
def build(files,out='qg4.npy'):
    text=''
    for f in files: text+=clean(open(f,encoding='utf-8',errors='ignore').read())
    text=re.sub(r' +','',text)
    idx=(np.frombuffer(text.encode(),dtype=np.uint8).astype(np.int64)-97)
    q=idx[:-3]*17576+idx[1:-2]*676+idx[2:-1]*26+idx[3:]
    c=np.bincount(q,minlength=26**4).astype(np.float64)
    lp=np.log((c+0.05)/(c.sum()+0.05*26**4)).astype(np.float32)
    np.save(out,lp); return lp
def load(): return np.load('qg4.npy')
def score(tab,p):
    # p: int array of letters
    q=p[:-3]*17576+p[1:-2]*676+p[2:-1]*26+p[3:]
    return float(tab[q].sum())
if __name__=='__main__':
    tab=build(['corpus/diurnalofremarka00thom.txt','corpus/registerprivyco01coungoog.txt','corpus/csp_scots.txt'])
    def s(t): return score(tab,np.frombuffer(t.encode(),dtype=np.uint8).astype(np.int64)-97)
    print(s('i'*40),s('thelordregentisgraceanduthernoblemenquhilk'),s('quhilkwecouldnochtsuffernorthairisnafaltis'))
