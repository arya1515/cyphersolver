"""Apply a glyph key to transcription CSVs.
  python decode.py <key.json> <trans.csv>...        -> decoded text per line, unknown tokens in [brackets]
  python decode.py --tokens <trans.csv>             -> token sequence per line (for alignment)
  python decode.py --freq <trans.csv>...            -> token frequency table
"""
import sys,csv,json,collections,re
def norm(t):
    t=t.strip()
    t=t.replace('‖','//').replace('||','//')
    t=re.sub(r'\?$','',t)     # drop uncertainty marks for decoding
    return t
def load(fn):
    lines=collections.OrderedDict()
    for r in csv.DictReader(open(fn,encoding='utf-8')):
        if not r.get('token'): continue
        ln=int(r['line']); lines.setdefault(ln,[]).append((r['idx'],r['token'].strip()))
    return lines
args=sys.argv[1:]
if args[0]=='--tokens':
    for fn in args[1:]:
        for ln,toks in load(fn).items():
            print(f'{fn} L{ln:02d} ({len(toks)}): '+' '.join(t for i,t in toks))
elif args[0]=='--freq':
    c=collections.Counter()
    for fn in args[1:]:
        for ln,toks in load(fn).items():
            for i,t in toks: c[norm(t)]+=1
    for t,n in c.most_common(): print(f'{n:4d} {t}')
else:
    key=json.load(open(args[0],encoding='utf-8'))
    for fn in args[1:]:
        for ln,toks in load(fn).items():
            out=[]
            for i,t in toks:
                if t.startswith('[clear'): out.append(' '+t+' '); continue
                v=key.get(norm(t))
                out.append(v if v is not None else '['+t+']')
            print(f'L{ln:02d}: '+''.join(out))
