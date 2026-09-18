"""Decode the figure runs in transcription.txt with the 1565 Toledo key."""
import re, sys
KEY = {}
for letter, codes in [('a',[12,13,14]),('b',[15]),('c',[16]),('d',[17]),('e',[18,19,20]),('f',[21]),
                      ('g',[22]),('h',[23]),('i',[24,25,26]),('l',[27]),('m',[28]),('n',[29]),
                      ('o',[30,31,32]),('p',[33]),('q',[34]),('r',[35]),('s',[36]),('t',[37]),
                      ('u',[38,39,40]),('x',[41]),('y',[42]),('z',[43])]:
    for c in codes: KEY[c] = letter

def dec(run):
    if run == '1565': return run  # the date, not cipher
    d = run.replace(' ', '')
    out = []
    for i in range(0, len(d) - 1, 2):
        out.append(KEY.get(int(d[i:i+2]), '?'))
    if len(d) % 2: out.append('|odd')
    return ''.join(out).upper()

pat = re.compile(r'(?<![\w])(?!15[0-9]{2})\d{2,}(?: \d+)*')
for line in open(sys.argv[1] if len(sys.argv) > 1 else 'transcription.txt', encoding='utf-8'):
    line = line.rstrip('\n')
    if line.startswith('#'): continue
    if line.startswith('=='): print(line); continue
    print(pat.sub(lambda m: '<' + ' '.join(dec(t) for t in m.group(0).split()) + '>', line))
