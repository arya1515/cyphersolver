"""b2_longrange.py  --  higher-level literature statistics for the Voynich adjudication (task b2).

Pure Python 3.12, no numpy.  Run from anywhere:  python b2_longrange.py
Writes results/b2.json and results/b2.md next to this file.

Four analyses on data/ZL3b-n.words.tsv (paragraph text, locus_type P, words with '?' or non-letters dropped),
each with natural-language controls poured into the Voynich folio skeleton (same tokens per folio, same order):

  1. Montemurro & Zanette (2010, 2013) long-range keyword information, scales 50..3200 (+6400) tokens.
  2. Adjacent-page similarity (Jensen-Shannon divergence over the 300 most frequent words), stratified by
     Currier language, hand, hand+section, against all non-adjacent pairs in the same stratum.
  3. Mutual information section-label:word, marginal and conditional on hand / quire / language, against a
     within-hand label-permutation null, a within-hand label-rotation (contiguity-preserving) null, and
     natural-language pours with contiguous 'sections' as a positive control.
  4. Spherical k-means on TF-IDF folio vectors (words ranked 21-520), agreement with section, hand, language.

Method choices are stated in the Markdown report.  All output is unvalidated until user review.
"""
import sys, os, re, math, json, random, time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data', 'ZL3b-n.words.tsv')
RES = os.path.join(HERE, 'results')
SCR = r'C:\Users\DANIEL~1.BOU\AppData\Local\Temp\claude\C--Users-Daniel-Bourdeau-cipher\bfb7c2bf-254a-4a86-b088-f16d86b54a8f\scratchpad\t50'
CORPORA = {
    'latin': os.path.join(SCR, 'corp_la_33849.txt'),
    'english': os.path.join(SCR, 'corp_en_1342.txt'),
    'italian': r'C:\Users\Daniel.Bourdeau\cipher\cyphersolver\vatican5\corpus_it.txt',
}
SECTION_NAMES = {'H': 'herbal', 'A': 'astro', 'B': 'biological', 'C': 'cosmological', 'P': 'pharma',
                 'S': 'stars/recipes', 'T': 'text', 'Z': 'zodiac'}
T0 = time.time()
def log(*a):
    print('[%6.1fs]' % (time.time() - T0), *a, flush=True)

LOG2 = math.log(2)
def H_of_counts(counts):
    n = sum(counts)
    if n == 0:
        return 0.0
    return -sum(c / n * math.log(c / n) for c in counts if c) / LOG2

# ----------------------------------------------------------------------------------------------------------
# 1. Data
# ----------------------------------------------------------------------------------------------------------
def load_voynich():
    folios = []          # list of dicts in binding order: folio, tokens, lang, hand, illus, quire
    idx = {}
    dropped_q = dropped_nonalpha = 0
    with open(DATA, encoding='utf-8') as f:
        header = f.readline().rstrip('\n').split('\t')
        col = {c: i for i, c in enumerate(header)}
        for line in f:
            r = line.rstrip('\n').split('\t')
            if len(r) < len(header) or r[col['locus_type']] != 'P':
                continue
            fol = r[col['folio']]
            if fol not in idx:
                idx[fol] = len(folios)
                folios.append({'folio': fol, 'tokens': [], 'lang': Counter(), 'hand': Counter(),
                               'illus': Counter(), 'quire': Counter()})
            d = folios[idx[fol]]
            for w in r[col['line_words']].split():
                if '?' in w:
                    dropped_q += 1
                    continue
                if not w.isalpha():
                    dropped_nonalpha += 1
                    continue
                d['tokens'].append(w)
                for k in ('lang', 'hand', 'illus', 'quire'):
                    d[k][r[col[k]]] += 1
    for d in folios:
        for k in ('lang', 'hand', 'illus', 'quire'):
            d[k] = d[k].most_common(1)[0][0] if d[k] else '?'
    folios = [d for d in folios if d['tokens']]
    return folios, dropped_q, dropped_nonalpha

def gutenberg_body(path):
    t = open(path, encoding='utf-8', errors='replace').read()
    i = t.find('*** START OF')
    if i >= 0:
        t = t[t.find('\n', i) + 1:]
    j = t.find('*** END OF')
    if j >= 0:
        t = t[:j]
    t = re.sub(r'\[Sidenote:.*?\]', ' ', t, flags=re.S)       # Confessions editorial apparatus (multi-line)
    t = re.sub(r'\[Illustration:.*?\]', ' ', t, flags=re.S)
    return t

def load_corpus(name, n):
    path = CORPORA[name]
    if name == 'italian':
        t = open(path, encoding='utf-8', errors='replace').read()
    else:
        t = gutenberg_body(path)
    toks = re.findall(r"[^\W\d_]+", t.lower())
    if name == 'latin':
        toks = [w for w in toks if w != 'sidenote']
    return toks[:n]

def pour(tokens, skeleton):
    """Distribute a token list into the folio skeleton: same number of tokens per folio, same order/labels."""
    out, pos = [], 0
    for d in skeleton:
        n = len(d['tokens'])
        e = dict(d)
        e['tokens'] = tokens[pos:pos + n]
        pos += n
        out.append(e)
    return out

def contiguous_sections(skeleton):
    """Section labels for a poured book: contiguous blocks of folios with the same folio counts as the real
    sections (ordered by first appearance).  Gives a real book real 'topic' sections (positive control)."""
    order = []
    for d in skeleton:
        if d['illus'] not in order:
            order.append(d['illus'])
    sizes = Counter(d['illus'] for d in skeleton)
    labels = []
    for s in order:
        labels += [s] * sizes[s]
    return labels

# ----------------------------------------------------------------------------------------------------------
# 2. Montemurro-Zanette
# ----------------------------------------------------------------------------------------------------------
SCALES = [50, 100, 200, 400, 800, 1600, 3200, 6400]
def mz_curve(tokens, rng, n_shuf=20, minfreq=20, top_words_at=None):
    N = len(tokens)
    freq = Counter(tokens)
    words = [w for w, c in freq.items() if c >= minfreq]
    wid = {w: i for i, w in enumerate(words)}
    ids = [wid.get(w, -1) for w in tokens]
    shufs = []
    for _ in range(n_shuf):
        s = ids[:]
        rng.shuffle(s)
        shufs.append(s)

    def block_entropies(seq, s):
        P = N // s
        counts = [dict() for _ in range(len(words))]
        for j in range(P):
            base = j * s
            for k in range(base, base + s):
                i = seq[k]
                if i >= 0:
                    c = counts[i]
                    c[j] = c.get(j, 0) + 1
        return [H_of_counts(c.values()) for c in counts]

    curve = {}
    perword = {}
    for s in SCALES:
        if N // s < 2:
            continue
        H = block_entropies(ids, s)
        Hs = [0.0] * len(words)
        for sq in shufs:
            hh = block_entropies(sq, s)
            for i in range(len(words)):
                Hs[i] += hh[i]
        Hs = [h / n_shuf for h in Hs]
        info = [(freq[w] / N) * (Hs[i] - H[i]) for i, w in enumerate(words)]
        curve[s] = {'blocks': N // s, 'info_bits_per_token': sum(info),
                    'info_unweighted_sum_bits': sum(Hs[i] - H[i] for i in range(len(words))),
                    'n_word_types': len(words)}
        perword[s] = [(w, freq[w], H[i], Hs[i], info[i]) for i, w in enumerate(words)]
    peak = max(curve, key=lambda s: curve[s]['info_bits_per_token'])
    top = sorted(perword[peak], key=lambda t: -t[4])[:20]
    return {'N': N, 'curve': curve, 'peak_scale': peak, 'peak_info': curve[peak]['info_bits_per_token'],
            'top20_at_peak': [{'word': w, 'n': n, 'H_blocks': round(h, 3), 'H_shuffled': round(hs, 3),
                               'info_bits_per_token': round(i, 5)} for w, n, h, hs, i in top]}

# ----------------------------------------------------------------------------------------------------------
# 3. Adjacent-page similarity
# ----------------------------------------------------------------------------------------------------------
def jsd(p, q):
    keys = set(p) | set(q)
    d = 0.0
    for k in keys:
        a = p.get(k, 0.0); b = q.get(k, 0.0); m = 0.5 * (a + b)
        if a:
            d += 0.5 * a * math.log(a / m)
        if b:
            d += 0.5 * b * math.log(b / m)
    return d / LOG2

def folio_dists(folios, topk=300):
    freq = Counter(w for d in folios for w in d['tokens'])
    top = set(w for w, _ in freq.most_common(topk))
    dists = []
    for d in folios:
        c = Counter(w for w in d['tokens'] if w in top)
        n = sum(c.values())
        dists.append({w: v / n for w, v in c.items()} if n else {})
    return dists

def pair_matrix(dists):
    n = len(dists)
    M = {}
    for i in range(n):
        for j in range(i + 1, n):
            M[(i, j)] = jsd(dists[i], dists[j])
    return M

def adjacency_stats(folios, M, order, strata, rng, n_boot=1000):
    """order: list of folio indices in the sequence considered adjacent.  strata: name -> predicate(i, j)."""
    adj_pairs = set()
    for a, b in zip(order, order[1:]):
        adj_pairs.add((min(a, b), max(a, b)))
    out = {}
    for name, pred in strata.items():
        adj = [M[p] for p in adj_pairs if pred(*p)]
        rnd = [M[p] for p in M if p not in adj_pairs and pred(*p)]
        if len(adj) < 3 or len(rnd) < 10:
            out[name] = {'n_adjacent': len(adj), 'n_random': len(rnd)}
            continue
        rs = sorted(rnd)
        med = rs[len(rs) // 2]
        ma = sum(adj) / len(adj)
        mr = sum(rnd) / len(rnd)
        # bootstrap: mean of len(adj) random pairs drawn from the stratum, P(mean_random_sample <= mean_adj)
        k = len(adj)
        cnt = 0
        for _ in range(n_boot):
            if sum(rng.choice(rnd) for _ in range(k)) / k <= ma:
                cnt += 1
        out[name] = {'n_adjacent': len(adj), 'n_random': len(rnd), 'mean_adjacent': round(ma, 4),
                     'mean_random': round(mr, 4), 'median_random': round(med, 4),
                     'frac_adjacent_below_random_median': round(sum(1 for x in adj if x < med) / k, 3),
                     'ratio_adj_over_random': round(ma / mr, 3),
                     'p_boot_adjacent_as_similar': round((cnt + 1) / (n_boot + 1), 4)}
    return out

def make_strata(folios):
    L = [d['lang'] for d in folios]; Hd = [d['hand'] for d in folios]
    S = [d['illus'] for d in folios]; Q = [d['quire'] for d in folios]
    st = {
        'all': lambda i, j: True,
        'both_currier_A': lambda i, j: L[i] == 'A' and L[j] == 'A',
        'both_currier_B': lambda i, j: L[i] == 'B' and L[j] == 'B',
        'same_hand': lambda i, j: Hd[i] == Hd[j] and Hd[i] != '?',
        'same_hand_and_section': lambda i, j: Hd[i] == Hd[j] and Hd[i] != '?' and S[i] == S[j],
        'same_section': lambda i, j: S[i] == S[j],
        'same_quire': lambda i, j: Q[i] == Q[j],
        'same_hand_same_section_same_quire': lambda i, j: Hd[i] == Hd[j] and Hd[i] != '?' and S[i] == S[j] and Q[i] == Q[j],
        'different_hand': lambda i, j: Hd[i] != Hd[j] and '?' not in (Hd[i], Hd[j]),
    }
    for h in sorted(set(Hd) - {'?'}):
        st['hand_%s' % h] = (lambda h: (lambda i, j: Hd[i] == h and Hd[j] == h))(h)
    for s in sorted(set(S)):
        st['section_%s' % s] = (lambda s: (lambda i, j: S[i] == s and S[j] == s))(s)
    return st

# ----------------------------------------------------------------------------------------------------------
# 4. Mutual information section : word
# ----------------------------------------------------------------------------------------------------------
def mi_from_folio_counts(fc, labels, strata=None):
    """fc: per-folio Counter of frequent words.  labels: per-folio section label.
    strata: per-folio stratum label or None.  Returns MI(S;W) (bits/token) pooled over strata by weight."""
    groups = defaultdict(list)
    for i in range(len(fc)):
        groups[None if strata is None else strata[i]].append(i)
    total = sum(sum(c.values()) for c in fc)
    mi = 0.0
    for g, members in groups.items():
        sw = defaultdict(Counter)
        for i in members:
            sw[labels[i]].update(fc[i])
        ns = {s: sum(c.values()) for s, c in sw.items()}
        n = sum(ns.values())
        if n == 0 or len(sw) < 2:
            continue
        nw = Counter()
        for c in sw.values():
            nw.update(c)
        m = 0.0
        for s, c in sw.items():
            for w, v in c.items():
                m += v / n * math.log(v * n / (ns[s] * nw[w]))
        mi += (n / total) * m / LOG2
    return mi

def mi_analysis(folios, labels, rng, n_perm=200, minfreq=20, tag=''):
    freq = Counter(w for d in folios for w in d['tokens'])
    fw = set(w for w, c in freq.items() if c >= minfreq)
    fc = [Counter(w for w in d['tokens'] if w in fw) for d in folios]
    hands = [d['hand'] for d in folios]; quires = [d['quire'] for d in folios]; langs = [d['lang'] for d in folios]
    def all_mi(lab):
        return {'marginal': mi_from_folio_counts(fc, lab),
                'given_hand': mi_from_folio_counts(fc, lab, hands),
                'given_quire': mi_from_folio_counts(fc, lab, quires),
                'given_language': mi_from_folio_counts(fc, lab, langs),
                'given_hand_and_quire': mi_from_folio_counts(fc, lab, [h + '/' + q for h, q in zip(hands, quires)])}
    obs = all_mi(labels)
    # null (a): permute section labels among folios of the same hand
    by_hand = defaultdict(list)
    for i, h in enumerate(hands):
        by_hand[h].append(i)
    nullA = defaultdict(list)
    nullB = defaultdict(list)
    for _ in range(n_perm):
        lab = labels[:]
        for h, members in by_hand.items():
            vals = [labels[i] for i in members]
            rng.shuffle(vals)
            for i, v in zip(members, vals):
                lab[i] = v
        for k, v in all_mi(lab).items():
            nullA[k].append(v)
        # null (b): rotate the label sequence within each hand (binding order) by a random offset:
        # preserves contiguity/run structure, moves the boundaries relative to the drawings
        lab = labels[:]
        for h, members in by_hand.items():
            vals = [labels[i] for i in members]
            if len(members) > 1:
                r = rng.randrange(1, len(members))
                vals = vals[r:] + vals[:r]
            for i, v in zip(members, vals):
                lab[i] = v
        for k, v in all_mi(lab).items():
            nullB[k].append(v)
    def summ(o, null):
        m = sum(null) / len(null)
        sd = (sum((x - m) ** 2 for x in null) / max(1, len(null) - 1)) ** 0.5
        p = (sum(1 for x in null if x >= o) + 1) / (len(null) + 1)
        return {'null_mean': round(m, 4), 'null_sd': round(sd, 4), 'z': round((o - m) / sd, 1) if sd else None,
                'p': round(p, 4), 'excess_bits': round(o - m, 4)}
    res = {'n_tokens_frequent_words': sum(sum(c.values()) for c in fc), 'n_word_types': len(fw),
           'n_folios': len(folios), 'sections': dict(Counter(labels)), 'n_perm': n_perm}
    for k, o in obs.items():
        res[k] = {'observed': round(o, 4), 'null_shuffle_within_hand': summ(o, nullA[k]),
                  'null_rotate_within_hand': summ(o, nullB[k])}
    # per-hand breakdown of the observed conditional MI
    per_hand = {}
    for h, members in sorted(by_hand.items()):
        sub_fc = [fc[i] for i in members]; sub_lab = [labels[i] for i in members]
        ntok = sum(sum(c.values()) for c in sub_fc)
        per_hand[h] = {'n_folios': len(members), 'n_tokens': ntok, 'sections': dict(Counter(sub_lab)),
                       'MI_bits': round(mi_from_folio_counts(sub_fc, sub_lab), 4) if len(set(sub_lab)) > 1 else 0.0}
    res['per_hand'] = per_hand
    return res

# ----------------------------------------------------------------------------------------------------------
# 5. k-means on TF-IDF
# ----------------------------------------------------------------------------------------------------------
def tfidf_vectors(folios, skip=20, keep=500):
    freq = Counter(w for d in folios for w in d['tokens'])
    vocab = [w for w, _ in freq.most_common(skip + keep)][skip:]
    vid = {w: i for i, w in enumerate(vocab)}
    df = Counter()
    for d in folios:
        for w in set(d['tokens']):
            if w in vid:
                df[w] += 1
    n = len(folios)
    idf = {w: math.log(n / df[w]) for w in vocab}
    vecs = []
    for d in folios:
        c = Counter(w for w in d['tokens'] if w in vid)
        tot = len(d['tokens'])
        v = {vid[w]: (k / tot) * idf[w] for w, k in c.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({i: x / norm for i, x in v.items()})
    return vecs, vocab

def dot(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(i, 0.0) for i, x in a.items())

def kmeans(vecs, k, rng, restarts=10, iters=60):
    best = None
    n = len(vecs)
    for _ in range(restarts):
        # k-means++ seeding on cosine distance
        cents = [dict(vecs[rng.randrange(n)])]
        while len(cents) < k:
            d2 = [min(max(0.0, 1 - dot(v, c)) for c in cents) ** 2 for v in vecs]
            tot = sum(d2)
            r = rng.random() * tot
            acc = 0.0
            for i, x in enumerate(d2):
                acc += x
                if acc >= r:
                    cents.append(dict(vecs[i])); break
            else:
                cents.append(dict(vecs[-1]))
        assign = [-1] * n
        for it in range(iters):
            new = []
            for v in vecs:
                sims = [dot(v, c) for c in cents]
                new.append(max(range(k), key=lambda j: sims[j]))
            if new == assign:
                break
            assign = new
            cents = []
            for j in range(k):
                acc = defaultdict(float)
                for i in range(n):
                    if assign[i] == j:
                        for key, x in vecs[i].items():
                            acc[key] += x
                if not acc:      # empty cluster: reseed with the worst-fitting point
                    acc = defaultdict(float, vecs[rng.randrange(n)])
                norm = math.sqrt(sum(x * x for x in acc.values())) or 1.0
                cents.append({key: x / norm for key, x in acc.items()})
        inertia = sum(1 - dot(vecs[i], cents[assign[i]]) for i in range(n))
        if best is None or inertia < best[0]:
            best = (inertia, assign)
    return best[1], best[0]

def purity(clusters, labels):
    tab = defaultdict(Counter)
    for c, l in zip(clusters, labels):
        tab[c][l] += 1
    return sum(max(v.values()) for v in tab.values()) / len(labels)

def nmi(a, b):
    n = len(a)
    ca, cb, cab = Counter(a), Counter(b), Counter(zip(a, b))
    mi = sum(v / n * math.log(v * n / (ca[x] * cb[y])) for (x, y), v in cab.items())
    ha = -sum(v / n * math.log(v / n) for v in ca.values())
    hb = -sum(v / n * math.log(v / n) for v in cb.values())
    return mi / math.sqrt(ha * hb) if ha and hb else 0.0

def ari(a, b):
    n = len(a)
    cab = Counter(zip(a, b)); ca = Counter(a); cb = Counter(b)
    comb = lambda x: x * (x - 1) / 2
    idx = sum(comb(v) for v in cab.values())
    sa = sum(comb(v) for v in ca.values()); sb = sum(comb(v) for v in cb.values())
    exp = sa * sb / comb(n)
    mx = 0.5 * (sa + sb)
    return (idx - exp) / (mx - exp) if mx != exp else 0.0

def agreement(clusters, labels, rng, n_perm=200):
    p = purity(clusters, labels)
    base = []
    lab = labels[:]
    for _ in range(n_perm):
        rng.shuffle(lab)
        base.append(purity(clusters, lab))
    bm = sum(base) / len(base)
    return {'purity': round(p, 3), 'purity_permutation_baseline': round(bm, 3),
            'adjusted_purity': round((p - bm) / (1 - bm), 3) if bm < 1 else None,
            'NMI': round(nmi(clusters, labels), 3), 'ARI': round(ari(clusters, labels), 3),
            'n_labels': len(set(labels))}

def cluster_analysis(folios, sections, rng, tag):
    vecs, vocab = tfidf_vectors(folios)
    k = len(set(sections))
    clusters, inertia = kmeans(vecs, k, rng)
    hands = [d['hand'] for d in folios]; langs = [d['lang'] for d in folios]
    tab = defaultdict(Counter)
    for c, s, h in zip(clusters, sections, hands):
        tab[c]['%s/%s' % (s, h)] += 1
    return {'tag': tag, 'k': k, 'n_folios': len(folios), 'inertia': round(inertia, 3),
            'vs_section': agreement(clusters, sections, rng),
            'vs_hand': agreement(clusters, hands, rng),
            'vs_language': agreement(clusters, langs, rng),
            'cluster_table_section/hand': {str(c): dict(v.most_common()) for c, v in sorted(tab.items())}}

# ----------------------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------------------
def main():
    os.makedirs(RES, exist_ok=True)
    rng = random.Random(20260915)
    folios, dq, dna = load_voynich()
    voy_tokens = [w for d in folios for w in d['tokens']]
    N = len(voy_tokens)
    log('Voynich: %d folios, %d tokens (dropped %d with ?, %d non-alpha), %d types' %
        (len(folios), N, dq, dna, len(set(voy_tokens))))
    out = {'data': {'folios': len(folios), 'tokens': N, 'types': len(set(voy_tokens)), 'dropped_qmark': dq,
                    'dropped_nonalpha': dna,
                    'sections_folios': dict(Counter(d['illus'] for d in folios)),
                    'hands_folios': dict(Counter(d['hand'] for d in folios)),
                    'lang_folios': dict(Counter(d['lang'] for d in folios)),
                    'hand_x_section_folios': {h: dict(Counter(d['illus'] for d in folios if d['hand'] == h))
                                              for h in sorted(set(d['hand'] for d in folios))}}}
    corp = {}
    for name in CORPORA:
        corp[name] = load_corpus(name, N)
        log('%s: %d tokens, %d types; first words: %s' % (name, len(corp[name]), len(set(corp[name])),
                                                            ' '.join(corp[name][:8])))
        out['data'][name] = {'tokens': len(corp[name]), 'types': len(set(corp[name])), 'source': CORPORA[name]}
    pours = {name: pour(toks, folios) for name, toks in corp.items()}
    contig = contiguous_sections(folios)
    shuf_tokens = voy_tokens[:]
    rng.shuffle(shuf_tokens)

    # ---- 1. Montemurro-Zanette
    log('MZ curves')
    mz = {}
    for name, toks in [('voynich', voy_tokens), ('voynich_shuffled', shuf_tokens)] + list(corp.items()):
        mz[name] = mz_curve(toks, random.Random(1 + len(name)))
        log('  %s peak scale %d, %.4f bits/token' % (name, mz[name]['peak_scale'], mz[name]['peak_info']))
    # Voynich by language: A folios only and B folios only (token sequences in binding order)
    for L in ('A', 'B'):
        toks = [w for d in folios if d['lang'] == L for w in d['tokens']]
        mz['voynich_currier_%s' % L] = mz_curve(toks, random.Random(7))
        log('  Currier %s (%d tokens) peak scale %d, %.4f' % (L, len(toks), mz['voynich_currier_%s' % L]['peak_scale'],
                                                                mz['voynich_currier_%s' % L]['peak_info']))
    out['montemurro_zanette'] = mz

    # ---- 2. Adjacent-page similarity
    log('adjacency')
    MINTOK = 30
    keep = [i for i, d in enumerate(folios) if len(d['tokens']) >= MINTOK]
    kf = [folios[i] for i in keep]
    strata = make_strata(kf)
    adjres = {'min_tokens_per_folio': MINTOK, 'folios_kept': len(kf), 'top_words': 300}
    order = list(range(len(kf)))
    M_voy = None
    for name, fl in [('voynich', kf)] + [(n, [p[i] for i in keep]) for n, p in pours.items()]:
        dists = folio_dists(fl)
        M = pair_matrix(dists)
        if name == 'voynich':
            M_voy = M
        adjres[name] = adjacency_stats(fl, M, order, strata, rng)
        log('  %s all: adj %.4f rand %.4f frac<med %.3f' % (name, adjres[name]['all']['mean_adjacent'],
            adjres[name]['all']['mean_random'], adjres[name]['all']['frac_adjacent_below_random_median']))
    # Voynich with folio order shuffled (20 shuffles), same pair matrix
    acc = defaultdict(lambda: defaultdict(float))
    NS = 20
    for _ in range(NS):
        o = order[:]
        rng.shuffle(o)
        r = adjacency_stats(kf, M_voy, o, strata, rng, n_boot=100)
        for st, v in r.items():
            for key in ('mean_adjacent', 'frac_adjacent_below_random_median', 'ratio_adj_over_random'):
                if key in v:
                    acc[st][key] += v[key] / NS
    adjres['voynich_folio_order_shuffled_mean_of_%d' % NS] = {st: {k: round(x, 4) for k, x in v.items()} for st, v in acc.items()}
    # Voynich with folio order shuffled within hand (keeps hand runs, breaks page-to-page topic continuity)
    acc2 = defaultdict(lambda: defaultdict(float))
    for _ in range(NS):
        # permute folios among the binding positions occupied by the same hand (hand runs kept, page order broken)
        pos_by_hand = defaultdict(list)
        for p_, i in enumerate(order):
            pos_by_hand[kf[i]['hand']].append(p_)
        o = order[:]
        for h, ps in pos_by_hand.items():
            vals = [order[p_] for p_ in ps]
            rng.shuffle(vals)
            for p_, v in zip(ps, vals):
                o[p_] = v
        r = adjacency_stats(kf, M_voy, o, strata, rng, n_boot=100)
        for st, v in r.items():
            for key in ('mean_adjacent', 'frac_adjacent_below_random_median', 'ratio_adj_over_random'):
                if key in v:
                    acc2[st][key] += v[key] / NS
    adjres['voynich_folio_order_shuffled_within_hand_mean_of_%d' % NS] = {st: {k: round(x, 4) for k, x in v.items()} for st, v in acc2.items()}
    out['adjacent_page_similarity'] = adjres

    # ---- 3. Mutual information
    log('MI')
    sections = [d['illus'] for d in folios]
    mires = {'voynich': mi_analysis(folios, sections, rng, tag='voynich')}
    log('  voynich MI %.4f | hand %.4f' % (mires['voynich']['marginal']['observed'], mires['voynich']['given_hand']['observed']))
    for name, p in pours.items():
        mires[name + '_contiguous_sections'] = mi_analysis(p, contig, rng, tag=name)
        mires[name + '_voynich_section_labels'] = mi_analysis(p, sections, rng, tag=name)
        log('  %s MI contiguous %.4f | hand %.4f ; voynich labels %.4f | hand %.4f' % (
            name, mires[name + '_contiguous_sections']['marginal']['observed'],
            mires[name + '_contiguous_sections']['given_hand']['observed'],
            mires[name + '_voynich_section_labels']['marginal']['observed'],
            mires[name + '_voynich_section_labels']['given_hand']['observed']))
    # Voynich with the folio order shuffled (tokens stay with folios, labels stay with folios: identical MI)
    # so instead: Voynich with tokens re-poured in shuffled folio order = the within-hand permutation null already.
    out['mutual_information'] = mires
    out['contiguous_section_labels_for_pours'] = contig

    # ---- 4. k-means
    log('k-means')
    km = {}
    km['voynich_all'] = cluster_analysis(kf, [d['illus'] for d in kf], rng, 'voynich all folios >= %d tokens' % MINTOK)
    log('  voynich all: purity sec %.3f hand %.3f lang %.3f' % (km['voynich_all']['vs_section']['purity'],
        km['voynich_all']['vs_hand']['purity'], km['voynich_all']['vs_language']['purity']))
    for h in ('1', '2', '3'):
        sub = [d for d in kf if d['hand'] == h]
        secs = [d['illus'] for d in sub]
        big = {s for s, c in Counter(secs).items() if c >= 3}
        sub = [d for d in sub if d['illus'] in big]
        if len(big) >= 2:
            km['voynich_hand_%s' % h] = cluster_analysis(sub, [d['illus'] for d in sub], rng, 'voynich hand %s only' % h)
    for L in ('A', 'B'):
        sub = [d for d in kf if d['lang'] == L]
        secs = [d['illus'] for d in sub]
        big = {s for s, c in Counter(secs).items() if c >= 3}
        sub = [d for d in sub if d['illus'] in big]
        km['voynich_currier_%s' % L] = cluster_analysis(sub, [d['illus'] for d in sub], rng, 'voynich Currier %s only' % L)
    kcontig = [contig[i] for i in keep]
    for name, p in pours.items():
        km[name + '_contiguous_sections'] = cluster_analysis([p[i] for i in keep], kcontig, rng, name + ' pour, contiguous sections')
    out['kmeans'] = km
    out['runtime_seconds'] = round(time.time() - T0, 1)
    with open(os.path.join(RES, 'b2.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    write_md(out)
    log('done')

def write_md(out):
    L = []
    d = out['data']
    L.append('# b2: long-range keyword information, page adjacency, illustration-text MI, topic clustering')
    L.append('')
    L.append('Script `b2_longrange.py`, pure Python, seed 20260915, runtime %.0f s. All output unvalidated until user review.' % out['runtime_seconds'])
    L.append('')
    L.append('Data: ZL3b-n paragraph text (locus P), %d folios, %d tokens, %d types; dropped %d words with `?` and %d with non-letters. '
             'Folio sections (P text): %s. Hands: %s. Currier: %s.' % (d['folios'], d['tokens'], d['types'], d['dropped_qmark'],
             d['dropped_nonalpha'], d['sections_folios'], d['hands_folios'], d['lang_folios']))
    L.append('Hand x section (folios): %s' % d['hand_x_section_folios'])
    L.append('Controls cut to %d tokens: Latin Confessions (Gutenberg 33849, header/footer and [Sidenote] stripped), English Pride and Prejudice (1342), '
             'period Italian OCR corpus (vatican5/corpus_it.txt, first %d tokens). Pours: same tokens per folio as the Voynich skeleton, in order, '
             'inheriting the skeleton folio\'s hand/quire/language labels.' % (d['tokens'], d['tokens']))
    L.append('')
    # 1
    L.append('## 1. Montemurro-Zanette long-range information')
    L.append('')
    L.append('Method: word types with frequency >= 20; text cut into floor(N/s) consecutive blocks of s tokens (tail dropped); '
             'per word, entropy (bits) of its distribution over blocks minus the same entropy averaged over 20 random shuffles of the token sequence; '
             'weighted by p(w) = n/N and summed = information in bits per token (MZ 2010 decomposition). Scale 6400 added beyond the requested set '
             '(only 5 blocks). Shuffled Voynichese = one fixed shuffle of the token sequence, measured the same way (noise floor).')
    L.append('')
    mz = out['montemurro_zanette']
    names = ['voynich', 'voynich_shuffled', 'latin', 'english', 'italian', 'voynich_currier_A', 'voynich_currier_B']
    L.append('| scale s | ' + ' | '.join(names) + ' |')
    L.append('|---|' + '---|' * len(names))
    for s in SCALES:
        row = []
        for n in names:
            c = mz[n]['curve'].get(s)
            row.append('%.4f' % c['info_bits_per_token'] if c else '-')
        L.append('| %d | ' % s + ' | '.join(row) + ' |')
    L.append('| peak scale | ' + ' | '.join(str(mz[n]['peak_scale']) for n in names) + ' |')
    L.append('| peak height | ' + ' | '.join('%.4f' % mz[n]['peak_info'] for n in names) + ' |')
    L.append('| N tokens / types >= 20 | ' + ' | '.join('%d / %d' % (mz[n]['N'], mz[n]['curve'][SCALES[0]]['n_word_types']) for n in names) + ' |')
    L.append('')
    for n in ('voynich', 'latin', 'english'):
        L.append('Top 20 words by information at the %s peak scale (%d):' % (n, mz[n]['peak_scale']))
        L.append('')
        L.append('| word | n | H blocks | H shuffled | bits/token |')
        L.append('|---|---|---|---|---|')
        for t in mz[n]['top20_at_peak']:
            L.append('| %s | %d | %.3f | %.3f | %.5f |' % (t['word'], t['n'], t['H_blocks'], t['H_shuffled'], t['info_bits_per_token']))
        L.append('')
    # 2
    L.append('## 2. Adjacent-page similarity')
    L.append('')
    a = out['adjacent_page_similarity']
    L.append('Method: folios with >= %d tokens (%d kept); per-folio distribution over the %d most frequent words of that text; Jensen-Shannon divergence (bits) '
             'for consecutive folio pairs in current binding order against all non-adjacent folio pairs in the same stratum ("random"). '
             '"frac<med" = fraction of adjacent pairs with JSD below the random median (0.5 under no adjacency effect); p_boot = probability that a random '
             'sample of the same number of stratum pairs has mean JSD <= the adjacent mean (1000 draws). '
             'Pours inherit the skeleton\'s hand/section/language labels, so their strata are contiguous ranges of a real book.' % (
                 a['min_tokens_per_folio'], a['folios_kept'], a['top_words']))
    L.append('')
    texts = ['voynich', 'latin', 'english', 'italian']
    shufk = [k for k in a if k.startswith('voynich_folio_order_shuffled_mean')][0]
    shufk2 = [k for k in a if k.startswith('voynich_folio_order_shuffled_within')][0]
    L.append('| stratum | n adj / n rand (voy) | ' + ' | '.join('%s adj / rand / ratio / frac<med / p' % t for t in texts) + ' | voy order shuffled ratio / frac<med | voy shuffled within hand ratio / frac<med |')
    L.append('|---|---|' + '---|' * len(texts) + '---|---|')
    for st in a['voynich']:
        v = a['voynich'][st]
        if 'mean_adjacent' not in v:
            L.append('| %s | %d / %d | too few pairs |' % (st, v['n_adjacent'], v['n_random']))
            continue
        cells = []
        for t in texts:
            x = a[t][st]
            cells.append('%.3f / %.3f / %.2f / %.2f / %.3f' % (x['mean_adjacent'], x['mean_random'], x['ratio_adj_over_random'],
                                                             x['frac_adjacent_below_random_median'], x['p_boot_adjacent_as_similar']))
        s1 = a[shufk].get(st, {}); s2 = a[shufk2].get(st, {})
        L.append('| %s | %d / %d | %s | %s / %s | %s / %s |' % (st, v['n_adjacent'], v['n_random'], ' | '.join(cells),
                 '%.2f' % s1['ratio_adj_over_random'] if s1 else '-', '%.2f' % s1['frac_adjacent_below_random_median'] if s1 else '-',
                 '%.2f' % s2['ratio_adj_over_random'] if s2 else '-', '%.2f' % s2['frac_adjacent_below_random_median'] if s2 else '-'))
    L.append('')
    # 3
    L.append('## 3. Illustration-to-text mutual information')
    L.append('')
    L.append('Method: tokens of word types with frequency >= 20; MI(section; word) in bits per token, plug-in. Conditional versions: MI computed within each '
             'stratum (hand, quire, Currier language, hand x quire) and averaged with token weights. Null (a): section labels permuted among folios of the same hand, '
             '200 permutations (removes the section-hand confound and gives the finite-sample bias). Null (b): section-label sequence rotated by a random offset '
             'within each hand in binding order (keeps the run structure of the labels, moves the boundaries off the drawings; tests "any contiguous partition '
             'would do"). Positive controls: the three pours with contiguous section blocks of the same folio counts (real topic change), and with the '
             'Voynich section labels as they fall on the skeleton.')
    L.append('')
    mi = out['mutual_information']
    keys = ['marginal', 'given_hand', 'given_quire', 'given_language', 'given_hand_and_quire']
    L.append('| text | ' + ' | '.join('%s obs / null-a mean / excess / z / p ; null-b mean / z' % k for k in keys) + ' |')
    L.append('|---|' + '---|' * len(keys))
    for t, r in mi.items():
        cells = []
        for k in keys:
            x = r[k]; na = x['null_shuffle_within_hand']; nb = x['null_rotate_within_hand']
            cells.append('%.4f / %.4f / %.4f / %s / %.3f ; %.4f / %s' % (x['observed'], na['null_mean'], na['excess_bits'], na['z'], na['p'], nb['null_mean'], nb['z']))
        L.append('| %s | ' % t + ' | '.join(cells) + ' |')
    L.append('')
    L.append('Per-hand MI(section; word) within the hand, Voynich: ' + '; '.join('hand %s: %d folios, %d tokens, sections %s, MI %.4f' % (
        h, v['n_folios'], v['n_tokens'], v['sections'], v['MI_bits']) for h, v in mi['voynich']['per_hand'].items()))
    L.append('')
    # 4
    L.append('## 4. Topic clustering (spherical k-means on TF-IDF)')
    L.append('')
    L.append('Method: folio vectors over words ranked 21-520 by frequency, TF = count/folio tokens, IDF = ln(folios/df), L2-normalised; k-means with cosine '
             'similarity, k-means++ seeding, 10 restarts, best inertia; k = number of section labels present in the subset (labels with < 3 folios dropped '
             'in subsets). Agreement: purity, purity under 200 label permutations, adjusted purity = (purity - baseline)/(1 - baseline), NMI, ARI.')
    L.append('')
    L.append('| run | folios | k | vs section: purity / baseline / adjusted / NMI / ARI | vs hand: same | vs Currier: same |')
    L.append('|---|---|---|---|---|---|')
    for name, r in out['kmeans'].items():
        def cell(x):
            return '%.3f / %.3f / %s / %.3f / %.3f' % (x['purity'], x['purity_permutation_baseline'], x['adjusted_purity'], x['NMI'], x['ARI'])
        L.append('| %s | %d | %d | %s | %s | %s |' % (r['tag'], r['n_folios'], r['k'], cell(r['vs_section']), cell(r['vs_hand']), cell(r['vs_language'])))
    L.append('')
    L.append('Cluster composition (section/hand counts), Voynich all folios: %s' % out['kmeans']['voynich_all']['cluster_table_section/hand'])
    for k in ('voynich_hand_1', 'voynich_hand_2', 'voynich_hand_3'):
        if k in out['kmeans']:
            L.append('')
            L.append('%s: %s' % (k, out['kmeans'][k]['cluster_table_section/hand']))
    L.append('')
    with open(os.path.join(RES, 'b2.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')

if __name__ == '__main__':
    main()
