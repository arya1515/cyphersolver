import re
t = open(r'c:\Users\dbour\cypher\rupert\warburton3.txt', encoding='utf-8', errors='ignore').read()
for pat in [r'Maurice', r'Worcester,\s*7', r'your\s+cipher', r'you\s+may\s+observe']:
    for m in re.finditer(pat, t):
        ctx = t[max(0, m.start() - 200): m.start() + 200].replace('\n', ' ')
        if re.search(r'\d{2,3}\s+\d{2,3}\s+\d{2,3}', ctx):
            print('====', pat, m.start()); print(t[max(0, m.start() - 1500): m.start() + 2500]); break
