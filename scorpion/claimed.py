"""claimed.py -- test the 2018 'Rubislaw32' claimed solutions of Scorpion S1 and S5 (zodiackillermystery forum).
A homophonic key maps each cipher symbol to ONE letter, so every repeated symbol must decode to the same letter.
Also reports the implied key, the number of symbols per plaintext letter, and the English LM score per letter."""
import sys, collections, itertools, pathlib
sys.stdout.reconfigure(encoding='utf-8')
S1_PT = "APICTUREIN COLLECTION OFPEOPLEBA GELBOBSOLD DAIRYFROTH YLATECOFEE POURACTION".replace(' ', '')
S5_PT = ("IAMSENDINGOT HERPICTUREOF PEOPLEFORTHE COLLECTIONOF RECENTHYBRID GENDERSWITHE DGEKEPTFROMA RTISTICFEEIF "
         "PERSONOFAGEH ASTOPURCHASE PICKOFUNIVER SITYUGLIESES PRESSONYPCOF EEFORCESACOL DENEMAREVIEW").replace(' ', '')
s1 = [s for l in open('s1.txt', encoding='utf-8') if l.strip() and not l.startswith('#') for s in l.split()]
s5 = [int(x) for l in open('s5.txt') if not l.startswith('#') for x in l.split()]
assert len(s1) == 70 == len(S1_PT) and len(s5) == 180 == len(S5_PT)
UNCERTAIN1 = {'circL', 'sqnotchBR', 'sqbarT', 'flag'}     # identifications flagged uncertain in s1.txt
def check(name, syms, pt, uncertain=()):
    pos = collections.defaultdict(list)
    for i, s in enumerate(syms): pos[s].append(i)
    key = {s: sorted(set(pt[i] for i in p)) for s, p in pos.items()}
    rep = {s: p for s, p in pos.items() if len(p) > 1}
    bad = {s: key[s] for s in rep if len(key[s]) > 1}
    print(f'== {name}: {len(syms)} symbols, {len(pos)} distinct, {len(rep)} repeated symbols, '
          f'{sum(len(p)*(len(p)-1)//2 for p in rep.values())} repeat pairs')
    for s, p in sorted(rep.items(), key=lambda kv: -len(kv[1])):
        flag = ' (uncertain identification)' if s in uncertain else ''
        print(f'   {str(s):12} positions {p} -> letters {[pt[i] for i in p]} {"OK" if len(key[s])==1 else "CONFLICT"}{flag}')
    print(f'   consistent repeated symbols: {len(rep)-len(bad)}/{len(rep)}; conflicts: {bad}')
    # implied homophone counts per letter
    per_letter = collections.Counter()
    for s, ls in key.items():
        if len(ls) == 1: per_letter[ls[0]] += 1
    lc = collections.Counter(pt)
    print('   letters in plaintext (count, symbols used):', ' '.join(f'{l}:{lc[l]}/{per_letter[l]}' for l, _ in lc.most_common()))
    return key
k1 = check('S1 (this repo transcription)', s1, S1_PT, UNCERTAIN1)
k5 = check('S5 (forum numeric transcription)', s5, S5_PT)
# LM score of the claimed plaintexts
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'copenhagen'))
argv = sys.argv; sys.argv = [sys.argv[0]]
import solve as cp
cp.CORPUS = pathlib.Path(r'C:/Users/DANIEL~1.BOU/AppData/Local/Temp/claude/C--Users-Daniel-Bourdeau-cipher/bfb7c2bf-254a-4a86-b088-f16d86b54a8f/scratchpad/t50')
lm = cp.build_lm('en')
for name, pt in [('S1 claimed', S1_PT), ('S5 claimed', S5_PT)]:
    t = pt.lower(); print(f'{name}: English 5-gram score {lm.score([t])/len(t):.3f} nats/letter; dictionary coverage {lm.coverage([t]):.2f}')
ref = "itwasthebestoftimesitwastheworstoftimesitwastheageofwisdomitwastheageoffoolishness"
print(f'reference English: {lm.score([ref])/len(ref):.3f} nats/letter; coverage {lm.coverage([ref]):.2f}')
