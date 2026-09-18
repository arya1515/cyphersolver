# Dictionary coverage of a spaceless text: DP over positions, words of length>=3 from the lexicon score len^1.5, else 0.
import pickle, re, math
class WordScorer:
    def __init__(self, path='catinat1691/lex2.pkl', minlen=4, extra=()):
        lex=pickle.load(open(path,'rb'))
        self.words=set(w for w,c in lex.items() if len(w)>=minlen and c>=2 and re.fullmatch(r'[a-z]+',w))
        self.words|=set(extra)
        self.maxlen=max(len(w) for w in self.words); self.minlen=minlen
    def score(self, text):
        n=len(text); best=[0.0]*(n+1)
        for i in range(1,n+1):
            b=best[i-1]
            for L in range(self.minlen,min(self.maxlen,i)+1):
                w=text[i-L:i]
                if w in self.words:
                    v=best[i-L]+L**1.3
                    if v>b: b=v
            best[i]=b
        return best[n]/max(1,n)
if __name__=='__main__':
    import sys
    ws=WordScorer()
    for t in ['depuismaderniereonnousaproposelarchiducnousenauonsfaictrefus','eeraeneeratnerentearrerenenerrar','lesauoidispositiossueembrunetantibesleducdenoaillesaagoesprise']:
        print(round(ws.score(t),3), t)
