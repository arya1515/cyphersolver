"""R2232 decoder. Key R2233 (Wolff, 8 Sept 1801): row N lists four consecutive values of the sequence S;
group N with superscript k (written N.k, bare N = N.1) is the k-th value of row N, i.e. S[N+k-6]."""
import re, sys
S = ['0', '1/8', '1/4', '1/2'] + list('12345678') + ['9', 'à'] + list('abcdefghijklmn') + ['ô', 'o', 'p', 'q', 'r', 's', 't', 'û', 'u'] + list('vwxyzaeioua')
# rows 1-4 carry 0 and the fractions 1/8, 1/4, 1/2 (row 1 = 0 1/8 1/4 1/2).
def d(tok):
    m = re.fullmatch(r'(\d+)(?:\.(\d))?', tok)
    if not m: return tok
    i = int(m[1]) + int(m[2] or 1) - 2
    return S[i] if 0 <= i < len(S) else '?'
if __name__ == '__main__':
    for l in open(sys.argv[1] if len(sys.argv) > 1 else 'ct.txt', encoding='utf8'):
        if l.startswith('#'): continue
        print(' '.join(''.join(d(t) for t in w.split()) for w in l.strip().split('|')))
