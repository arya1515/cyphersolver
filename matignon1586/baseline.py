"""Measured baseline for the figures-to-French pipeline, so a later pass can tell whether it helped.

Character overlap against the crib's known plaintext on three lines of f. 18r. The measure is
generous (longest-common-subsequence blocks) but it is the same measure every time, which is the
point: a number to beat rather than an impression of the output.
"""
import difflib
CASES = [
 ("f.18r l2", "ste f est a bert ie e plustost que es sions ueue et",
              "ste fust aduertie et plustost que nous eussions uictoi"),
 ("f.18r l3", "re et conseil des sembler de castille bour",
              "re et conseil dassembler de castillebourg"),
 ("f.18r l4", "que ou lon feis tel lon ou loit ie quels i est",
              "g ou lon feist que ie nauois plus dinstruction"),
]
def score(cases=CASES):
    tot_r = tot_n = 0
    for name, got, truth in cases:
        g, t = got.replace(' ',''), truth.replace(' ','')
        m = sum(b.size for b in difflib.SequenceMatcher(None, g, t).get_matching_blocks())
        tot_r += m; tot_n += len(t)
        print(f'  {name}: {m:3d}/{len(t):3d} = {100*m/len(t):5.1f} %')
    print(f'  overall {tot_r}/{tot_n} = {100*tot_r/tot_n:.1f} %')
    return tot_r/tot_n
if __name__ == '__main__':
    print('2026-09-17  79 exemplars / 17 of 22 letters / gap 14, bonus 1.6, code floor 0.93')
    score()
