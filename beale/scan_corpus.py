"""Scan a gutenberg_english parquet shard against the Beale ciphers (two-stage, multiprocessing).
Row per (book, mode, cipher): id, title, author, nwords, mode, cipher, offset, s1mean, cover, s1z, quad, shifts"""
import sys, json, re, time, os
import numpy as np, pyarrow.parquet as pq
from multiprocessing import Pool
import bookcipher as bc

COMBOS = [('first', 'b1'), ('first', 'b2'), ('first', 'b3'), ('last', 'b1'), ('letter', 'b1')]
# stage-2 trigger thresholds on stage-1 mean (from null runs on novels: first b1 0.10, b2 0.20, letter 0.62/0.75)
THR = {('first', 'b1'): 0.10, ('first', 'b2'): 0.17, ('first', 'b3'): 0.10, ('last', 'b1'): None, ('letter', 'b1'): 0.60}
HITTHR = {'first': -13.8, 'letter': -13.5, 'last': -12.8}
lm = None; C = None; B = None

def init():
    global lm, C, B
    lm = bc.LM()
    C = {n: bc.load_cipher(n) for n in ['b1', 'b2', 'b3']}
    B = {n: bc.range_bands(C[n]) for n in C}

def work(item):
    text, meta = item
    try:
        md = json.loads(meta)
    except Exception:
        md = {}
    bid = md.get('text_id', '?'); title = str(md.get('title', ''))[:60].replace('\t', ' ').replace('\n', ' ')
    auth = str(md.get('authors', ''))[:40].replace('\t', ' ').replace('\n', ' ')
    text = bc.strip_gutenberg(text)
    words = bc.words_of(text)
    if len(words) < 300:
        return []
    keys = {}
    rows = []
    for mode, cn in COMBOS:
        if mode not in keys:
            keys[mode] = bc.letters_stream(text) if mode == 'letter' else bc.key_letters(words, mode)
        key = keys[mode]
        r = bc.stage1(key, C[cn], lm, B[cn], cn)
        if not r:
            continue
        o, mean, cv, z = r[0]
        q = ''; d = ''
        thr = THR[(mode, cn)]
        if (thr is not None and mean >= thr) or z >= 6.0:
            best = (-99, None, None, None)
            for oo, mm, cc, zz in r:
                if thr is not None and mm < thr and zz < 6.0:
                    continue
                qq, dd, pt = bc.stage2(key, C[cn], lm, B[cn], oo)
                if qq > best[0]:
                    best = (qq, dd, pt, oo)
            q = '%.3f' % best[0]; d = ','.join(map(str, best[1])); o = best[3]
            if best[0] > HITTHR[mode]:
                rows.append(f"HIT\t{bid}\t{mode}\t{cn}\t{o}\t{q}\t{d}\t{best[2]}\n")
        rows.append(f"{bid}\t{title}\t{auth}\t{len(words)}\t{mode}\t{cn}\t{o}\t{mean:.4f}\t{cv:.3f}\t{z:.2f}\t{q}\t{d}\n")
    return rows

if __name__ == '__main__':
    shard = sys.argv[1]; out = sys.argv[2]; nproc = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    pf = pq.ParquetFile(shard)
    cols = pf.schema_arrow.names
    tcol, mcol = ('TEXT', 'METADATA') if 'TEXT' in cols else ('text', 'id')
    t0 = time.time(); nb = 0
    with Pool(nproc, initializer=init) as pool, open(out, 'a', encoding='utf-8') as fo, open(out + '.hits', 'a', encoding='utf-8') as fh:
        for batch in pf.iter_batches(batch_size=256, columns=[tcol, mcol]):
            metas = batch.column(mcol).to_pylist()
            if mcol == 'id':
                metas = [json.dumps({'text_id': m, 'title': os.path.basename(shard)[:12]}) for m in metas]
            items = list(zip(batch.column(tcol).to_pylist(), metas))
            for rows in pool.imap_unordered(work, items, chunksize=4):
                nb += 1
                for r in rows:
                    (fh if r.startswith('HIT') else fo).write(r)
            fo.flush(); fh.flush()
            print(f"  {nb} books, {time.time()-t0:.0f}s", flush=True)
    print(f"{shard}: {nb} books in {time.time()-t0:.0f}s", flush=True)
