"""Expand the key with the confusions the eye actually makes on this hand.

Each token keeps its own letters and gains the letters of the shapes it is confusable with, at a
cost: the decoder pays `PEN` nats for choosing a confusion letter, so it only does so when the
French demands it. The confusion sets are the ones the crib exposed on f. 196 (three '6'-like
shapes for i/n/s, two round shapes for a/m, the e/r pair, u/v spellings).
"""
import json
base=json.load(open('key.json'))
CONF=[set('ins'),set('am'),set('er'),set('iy'),set('ul'),set('td'),set('cp'),set('gy'),set('ae')]
def expand(path='key_exp.json'):
    out={}
    for tok,vals in base.items():
        if vals and not vals[0].isalpha():
            out[tok]=[[v,0.0] for v in vals]; continue
        if len(vals[0])>1 and vals[0].isalpha() and tok in ('12','13','14','47','17','25','26','34','35','40','43','48','51','52','24'):
            out[tok]=[[v,0.0] for v in vals]; continue
        prim=set(v for v in vals if len(v)==1)
        extra=set()
        for s in CONF:
            if prim & s: extra |= s
        extra -= prim
        out[tok]=[[v,0.0] for v in vals]+[[v,2.2] for v in sorted(extra)]
    json.dump(out,open(path,'w'),indent=0)
    return out
if __name__=='__main__':
    o=expand(); print('tokens',len(o))
