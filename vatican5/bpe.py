"""Recover the code units of IA-2 without a key, by compression, and calibrate against a control.

The repetition in this text is extreme. Against a shuffle of its own digits it has 441 repeated
7-grams where the shuffle gives 5, and 244 repeated 8-grams where the shuffle gives none. A
letter-level cipher of 6549 symbols does not do that. A codebook does: the same groups recur because
the same words recur.

So stop guessing the unit length and let the text say what its units are. Greedy byte-pair encoding
merges the most frequent adjacent pair over and over; if the stream really is a concatenation of
fixed code groups, BPE rediscovers those groups, because merging inside a real unit pays and merging
across a unit boundary does not.

The result means nothing on its own - BPE compresses any string. Everything here is therefore run in
parallel on three streams:

    real      the ciphertext
    shuffle   the same digits in random order (kills all structure, keeps frequencies)
    italian   real period Italian, enciphered nothing, just mapped to 10 symbols by a random
              polyphonic assignment - what a genuine single-digit polyphonic cipher would look like

If the real text is a codebook and the Italian control is not, the two will separate. If real and
italian behave alike, the repetition is just language and there is no codebook to find.

Usage: python bpe.py [merges]
"""
import collections, math, random, re, sys

import escape as E


def bpe(seq, merges):
    """Greedy byte-pair encoding. Returns (tokens, vocabulary, description length trace)."""
    toks = list(seq)
    vocab = {}
    trace = []
    for step in range(merges):
        pairs = collections.Counter(zip(toks, toks[1:]))
        if not pairs:
            break
        (a, b), n = pairs.most_common(1)[0]
        if n < 3:
            break
        new = a + b
        out, i = [], 0
        while i < len(toks):
            if i + 1 < len(toks) and toks[i] == a and toks[i + 1] == b:
                out.append(new)
                i += 2
            else:
                out.append(toks[i])
                i += 1
        toks = out
        vocab[new] = n
        trace.append((step + 1, new, n, len(toks)))
    return toks, vocab, trace


def desc_len(toks):
    """Bits to code the token stream under its own unigram distribution, plus the vocabulary."""
    c = collections.Counter(toks)
    n = len(toks)
    H = -sum(v / n * math.log2(v / n) for v in c.values())
    body = n * H
    vocab_bits = sum(len(t) * math.log2(10) for t in c if len(t) > 1)
    return body + vocab_bits, H, n


def italian_control(n, rnd):
    """Period Italian mapped to 10 digits by a random polyphonic assignment."""
    txt = open('corpus_it.txt', encoding='utf-8', errors='ignore').read().lower()
    txt = re.sub(r'[^a-z]', '', txt)
    txt = re.sub('[jkwxy]', '', txt)
    start = rnd.randrange(0, len(txt) - n * 2)
    letters = 'abcdefghilmnopqrstuvz'
    assign = {c: str(rnd.randrange(10)) for c in letters}
    out = []
    for ch in txt[start:]:
        if len(out) >= n:
            break
        if ch in assign:
            out.append(assign[ch])
    return out


def report(name, seq, merges):
    toks, vocab, trace = bpe(seq, merges)
    dl, H, n = desc_len(toks)
    base_dl, base_H, base_n = desc_len(list(seq))
    print('\n%-9s %d symbols -> %d tokens, %d merged units' % (name, len(seq), n, len(vocab)))
    print('          entropy %.3f bits/token, description length %.0f bits (was %.0f), gain %.1f%%'
          % (H, dl, base_dl, 100.0 * (base_dl - dl) / base_dl))
    top = sorted(collections.Counter(toks).items(), key=lambda kv: -kv[1])[:16]
    print('          top tokens: %s' % ', '.join('%s:%d' % (t, c) for t, c in top))
    lens = collections.Counter(len(t) for t in toks)
    print('          token length profile: %s'
          % ' '.join('%d:%.0f%%' % (k, 100.0 * v / n) for k, v in sorted(lens.items())))
    return dl, base_dl


def main():
    merges = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    seq = E.load()
    R = E.runs(seq)
    s = [d for r in R for d in r]
    rnd = random.Random(19)

    print('greedy BPE, %d merges' % merges)
    a = report('real', s, merges)

    sh = list(s)
    rnd.shuffle(sh)
    b = report('shuffle', sh, merges)

    it = italian_control(len(s), rnd)
    c = report('italian', it, merges)

    print("""
=== READING
Compression gain is the number to compare. A codebook stream compresses far better than the same
digits shuffled, and also better than genuine Italian pushed through a polyphonic single-digit
cipher, because in the codebook case the recurring units are real objects and in the Italian case
they are only letter statistics.""")
    print('   gain real %.1f%% | shuffle %.1f%% | italian %.1f%%'
          % (100 * (a[1] - a[0]) / a[1], 100 * (b[1] - b[0]) / b[1], 100 * (c[1] - c[0]) / c[1]))


if __name__ == '__main__':
    main()
