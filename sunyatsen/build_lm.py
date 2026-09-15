"""Build a traditional-Chinese character unigram/bigram model from jieba's word list + OpenCC S->T map."""
import urllib.request, os, json, math, collections
here = os.path.dirname(os.path.abspath(__file__))
def get(url, name):
    p = os.path.join(here, name)
    if not os.path.exists(p):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        open(p, 'wb').write(urllib.request.urlopen(req, timeout=120).read())
    return p
dic = get('https://raw.githubusercontent.com/fxsjy/jieba/master/jieba/dict.txt', 'jieba_dict.txt')
st = get('https://raw.githubusercontent.com/BYVoid/OpenCC/master/data/dictionary/STCharacters.txt', 'STCharacters.txt')
s2t = {}
for line in open(st, encoding='utf-8'):
    parts = line.rstrip('\n').split('\t')
    if len(parts) < 2: continue
    a, b = parts[0], parts[1]
    s2t[a] = b.split()[0]
uni = collections.Counter(); bi = collections.Counter()
for line in open(dic, encoding='utf-8'):
    w, f, *_ = line.split()
    f = int(f)
    t = ''.join(s2t.get(c, c) for c in w)
    for c in t: uni[c] += f
    for a, b in zip(t, t[1:]): bi[a+b] += f
json.dump({'uni': uni, 'bi': {k: v for k, v in bi.items() if v >= 20}}, open(os.path.join(here, 'lm_zh.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(len(uni), len(bi), uni.most_common(20))
