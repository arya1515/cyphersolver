"""Measured baseline for the figures-to-French pipeline.

Truths are f. 19r's plaintext as corrected by the code-group landmarks (see f18_f19_crib.md): line 3
carries only "re et conseil d'assembler d" - earlier baselines scored it against a longer, wrong
truth - and line 4 opens "e castillebourg" and reads "j'avois", not "je n'avois".

Lines 4 and 5 are partly circular: their exemplars were cut from them, albeit labelled by the
code-14 anchor rather than by hand. Line 2 is the honest control - its exemplars have not changed
since it was hand-labelled, so movement there comes from the rest of the set.
"""
import difflib, subprocess, sys, re
TRUTH = {2: "ste fust aduertie et plustost que nous eussions uictoi",
         3: "re et conseil dassembler d",
         4: "e castillebourg ou lon feist que iauois",
         5: "plus dinstructions"}
CIRCULAR = {4, 5}
def read_lines():
    out = subprocess.run([sys.executable, 'readleaf.py', 'hi/f18rflat.png', 'f18r_lines.txt', '14',
                          ','.join(map(str, TRUTH))], capture_output=True, text=True).stdout
    return {int(m.group(1)): m.group(2) for m in re.finditer(r'line\s+(\d+) \(\d+ figures\): (.*)', out)}
def score():
    got = read_lines(); tr = tn = 0; hr = hn = 0
    for ln, t in TRUTH.items():
        g = got.get(ln, '').replace(' ', ''); tt = t.replace(' ', '')
        g = g[:len(tt) + 6]                              # do not credit text past the truth's end
        m = sum(b.size for b in difflib.SequenceMatcher(None, g, tt).get_matching_blocks())
        tr += m; tn += len(tt)
        if ln not in CIRCULAR: hr += m; hn += len(tt)
        flag = '  (partly circular)' if ln in CIRCULAR else ''
        print(f'  f.18r l{ln}: {m:3d}/{len(tt):3d} = {100*m/len(tt):5.1f} %   {got.get(ln,"")}{flag}')
    print(f'  all lines        {tr}/{tn} = {100*tr/tn:.1f} %')
    print(f'  non-circular     {hr}/{hn} = {100*hr/hn:.1f} %   <- the number to watch')
if __name__ == '__main__':
    score()
