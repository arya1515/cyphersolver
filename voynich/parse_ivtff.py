"""parse_ivtff.py -- parse IVTFF 2.0 transliteration files (voynich.nu) into clean word lists.

Output (for each input file X.txt): data/X.words.tsv with columns
  folio  line_id  locus_type  lang  hand  illus  quire  para_start  para_end  line_words
where line_words is the space-separated list of words after cleaning:
  - inline comments <!...>, <%>, <$>, <~>, <->, {...} removed ({...} ligature/comment markers)
  - alternatives [a:b] -> first reading a;  uncertain glyph ? kept as ? (words containing ? are flagged)
  - '.' = word break; ',' = uncertain word break, treated as a break
Page metadata comes from the page header  <f1r> <! $Q=A $P=A $F=a $B=1 $I=T $L=A $H=1 ...>
usage: python parse_ivtff.py data/ZL3b-n.txt [more files]
"""
import re, sys, pathlib, collections
def parse(path):
    meta = {}; rows = []; cur = None
    for raw in pathlib.Path(path).read_text(encoding='utf-8', errors='replace').splitlines():
        if raw.startswith('#') or not raw.strip(): continue
        m = re.match(r'<(f\d+[rv]\d?|[a-z]\w*)>\s*<!([^>]*)>', raw)
        if m and '.' not in m.group(1):
            cur = m.group(1); vars_ = dict(re.findall(r'\$(\w)=(\w+)', m.group(2))); meta[cur] = vars_; continue
        m = re.match(r'<(f\d+[rv]\d?|\w+)\.(\d+),([@+*=])([A-Za-z])(\w*)>\s*(.*)$', raw)
        if not m: continue
        folio, ln, tag, ltype, sub, text = m.groups()
        pstart = '<%>' in text; pend = '<$>' in text
        t = re.sub(r'<![^>]*>', '', text)
        t = re.sub(r'<[^>]*>', '', t)
        t = re.sub(r'\{[^}]*\}', '', t)
        t = re.sub(r'\[([^\]:]*):[^\]]*\]', r'\1', t)
        t = t.replace(',', '.')
        words = [w for w in t.split('.') if w]
        v = meta.get(folio, {})
        rows.append((folio, f'{folio}.{ln}', ltype, v.get('L', '?'), v.get('H', '?'), v.get('I', '?'), v.get('Q', '?'), int(pstart), int(pend), ' '.join(words)))
    return rows
if __name__ == '__main__':
    for p in sys.argv[1:]:
        rows = parse(p); out = pathlib.Path(p).with_suffix('.words.tsv')
        with open(out, 'w', encoding='utf-8') as f:
            f.write('folio\tline_id\tlocus_type\tlang\thand\tillus\tquire\tpara_start\tpara_end\tline_words\n')
            for r in rows: f.write('\t'.join(map(str, r)) + '\n')
        nw = sum(len(r[9].split()) for r in rows); unc = sum(1 for r in rows for w in r[9].split() if '?' in w)
        print(f'{p}: {len(rows)} lines, {nw} words ({unc} with ?), langs {collections.Counter(r[3] for r in rows)}, locus types {collections.Counter(r[2] for r in rows)}')
