import re, unicodedata, pickle, numpy as np, collections
ALPHA = 'abcdefghilmnopqrstuxyz'
IDX = {c:i for i,c in enumerate(ALPHA)}
SUB = str.maketrans({'v':'u','j':'i','k':'c','w':'u','ñ':'n','ç':'c'})
def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')
    s = s.translate(SUB)
    return re.sub('[^%s]+' % ALPHA, '', s)
def build(path, N=5, out='lm5.pkl'):
    raw = open(path, encoding='utf-8', errors='replace').read()
    i = raw.find('DON QUIJOTE'); raw = raw[i:] if i > 0 else raw
    t = norm(raw)
    print('corpus letters', len(t))
    cnt = [collections.Counter() for _ in range(N+1)]
    for n in range(1, N+1):
        c = cnt[n]
        for k in range(len(t)-n+1): c[t[k:k+n]] += 1
    pickle.dump(dict(cnt=cnt, N=N, alpha=ALPHA), open(out,'wb'))
    print('ngram types', [len(c) for c in cnt[1:]])
if __name__ == '__main__':
    build('lit/quijote.txt')
