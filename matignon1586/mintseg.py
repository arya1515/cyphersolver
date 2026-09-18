"""Mint one-to-one pairs from a pinned (segalign) alignment into a hand's set, then ablate.

The held-out test for f. 143 is lines 6 and 7 (never minted from): their known text is scored before
and after, and any letter whose new exemplars lower that score is rejected.
"""
import os, sys, json, re, subprocess, difflib
from PIL import Image

HELD = {6: "ueurpoursesaffairesquede", 7: "raicteaueclyetenconsideration"}

def held_score(manifest):
    env = dict(os.environ, EXMAN=manifest)
    o = subprocess.run([sys.executable, 'readleaf.py', 'hi/f143flat.png', 'f143_lines.txt', '10',
                        ','.join(map(str, HELD))], capture_output=True, text=True, env=env).stdout
    got = {int(m.group(1)): m.group(2).replace(' ', '')
           for m in re.finditer(r'line\s+(\d+) \(\d+ figures\): (.*)', o)}
    r = n = 0
    for ln, t in HELD.items():
        g = got.get(ln, '')[:len(t)+6]
        r += sum(b.size for b in difflib.SequenceMatcher(None, g, t).get_matching_blocks()); n += len(t)
    return 100 * r / n

def mint(out, bs, a, line, tag, hand_man='exemplars/manifest_f143.json', mix='exemplars/manifest_mix.json'):
    base = json.load(open('exemplars/manifest.json'))
    man = json.load(open(hand_man))
    def write(m):
        json.dump(m, open(hand_man, 'w'), indent=1); json.dump(base + m, open(mix, 'w'), indent=1)
    write(man); before = held_score(mix)
    im = Image.fromarray(a); new = []
    for b0, b1, t, op in out:
        if op != '1': continue
        lab = t.strip('<>'); x0, x1, y0, y1 = bs[b0-1]
        fn = f'exemplars/f143/{tag}_{b0:02d}_{lab}.png'
        im.crop((x0-4, y0-6, x1+4, y1+6)).save(fn)
        new.append({'file': fn, 'letter': lab, 'src': f'f143 {tag}', 'box': [x0, x1, y0, y1],
                    'crib': f'segalign line {line}, codes pinned by eye'})
    write(man + new); with_all = held_score(mix)
    harmful = []
    for L in sorted({m['letter'] for m in new}):
        write(man + [m for m in new if m['letter'] != L])
        if held_score(mix) - with_all > 1.0: harmful.append(L)
    keep = [m for m in new if m['letter'] not in harmful]
    for m in new:
        if m not in keep and os.path.exists(m['file']):
            os.replace(m['file'], 'exemplars/rejected/f143_' + os.path.basename(m['file']))
    write(man + keep); after = held_score(mix)
    from collections import Counter
    c = Counter(m['letter'] for m in man + keep if len(m['letter']) == 1)
    print(f'  minted {len(new)}, rejected {len(new)-len(keep)} {harmful or ""}; held-out {before:.1f} -> {after:.1f} %;'
          f' f.143 set {sum(c.values())} over {len(c)} letters')
