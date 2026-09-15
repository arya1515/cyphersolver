"""Run the two-stage pipeline on every text file given (all modes, all ciphers) and print a summary."""
import sys, glob, os
import bookcipher as bc
lm = bc.LM()
C = {n: bc.load_cipher(n) for n in ['b1', 'b2', 'b3']}
B = {n: bc.range_bands(C[n]) for n in C}
files = [f for a in sys.argv[1:] for f in glob.glob(a)]
for f in files:
    text = bc.strip_gutenberg(open(f, encoding='utf-8', errors='ignore').read())
    words = bc.words_of(text)
    print(f"\n### {os.path.basename(f)}  ({len(words)} words)")
    for mode in ['first', 'last', 'second', 'letter']:
        key = bc.letters_stream(text) if mode == 'letter' else bc.key_letters(words, mode)
        for cn in ['b1', 'b3', 'b2']:
            r = bc.stage1(key, C[cn], lm, B[cn], cn)
            if not r:
                print(f"  {mode:6s} {cn}: n/a"); continue
            best = None
            for o, mean, cv, z in r:
                q, d, pt = bc.stage2(key, C[cn], lm, B[cn], o)
                if best is None or q > best[0]:
                    best = (q, o, mean, z, d, pt)
            q, o, mean, z, d, pt = best
            flag = ' <== HIT' if q > {'first': -13.8, 'letter': -13.5, 'last': -12.8, 'second': -13.5}[mode] else ''
            print(f"  {mode:6s} {cn}: quad {q:.2f} mean {mean:.3f} z {z:.1f} off {o} d={d}{flag}  {pt[:60]}")
