"""Forster 13 May 1644: tokenizer and the homophonic key as published by R. Pitt (forster-cipher, 14 Sept 2026),
who reports that G. Lasry and N. Biermann had reached the same reading earlier (per K. Britland). See NOTES.md."""
import re
CLEAR = ["ie vous en responds et mesmes dans", "et mesurer a cela sil est meilleur d’agir, ou\nde soupir 13. de may. 1644"]
KEY = {'0':'e','2':'e','4':'a','5':'g','7':'d','8':'t','12':'c','14':'z','16':'i','19':'n','20':'r','30':'u',
       '40':'s','50':'t','70':'f','80':'l','88':'q','90':'p',
       'a':'d','b':'t','c':'l','d':'i','e':'g','f':'b','g':'y','l':'r','n':'f','p':'a','q':'c','s':'o','t':'n',
       'u':'m','x':'s','y':'p'}
def load(path='ciphertext.txt'):
    t = open(path, encoding='utf-8').read()
    for c in CLEAR: t = t.replace(c, ' | ')
    return t
def groups(path='ciphertext.txt'):
    """Comma-separated cipher groups (word-ish units), cipher-only; '|' marks the clear passages."""
    out = []
    for seg in load(path).split('|')[:-1]:
        for g in seg.split(','):
            toks = re.findall(r"\d+|[a-z]", g)
            if toks: out.append(toks)
        out.append(['|'])
    return out
def tokens(path='ciphertext.txt'):
    return [t for g in groups(path) for t in g if t != '|']
def decode(toks, key=KEY):
    return ''.join(key.get(t, '?') for t in toks)
if __name__ == '__main__':
    gs = groups()
    print(' '.join('|' if g == ['|'] else decode(g) for g in gs))
