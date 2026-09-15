"""Fetch Warburton vol.3 OCR and extract the Maurice->Rupert cipher letter (7 July 1645) and nearby cipher material."""
import urllib.request, re, os
H = {'User-Agent': 'Mozilla/5.0'}
fn = 'warburton3.txt'
if not os.path.exists(fn):
    data = urllib.request.urlopen(urllib.request.Request('https://archive.org/download/memoirsofprincer03warbuoft/memoirsofprincer03warbuoft_djvu.txt', headers=H), timeout=300).read()
    open(fn, 'wb').write(data)
t = open(fn, encoding='utf-8', errors='ignore').read()
print(len(t))
for m in re.finditer(r'By your cipher|your cypher|in cipher|in cypher|decypher|decipher', t):
    s = max(0, m.start() - 300); print('----', m.start()); print(t[s:m.start() + 700].replace('\n', ' '))
