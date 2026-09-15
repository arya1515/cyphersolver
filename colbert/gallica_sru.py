"""Query Gallica SRU for Mélanges de Colbert volumes and print ark identifiers."""
import urllib.request, urllib.parse, re, sys
qs = sys.argv[1:] or ['Mélanges de Colbert 172', 'Mélanges de Colbert 168', 'Mélanges de Colbert 127']
for q in qs:
    url = ('https://gallica.bnf.fr/SRU?operation=searchRetrieve&version=1.2&maximumRecords=15&query='
           + urllib.parse.quote('(dc.title all "%s")' % q))
    try:
        d = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read().decode('utf-8', 'ignore')
    except Exception as e:
        print(q, 'ERR', e); continue
    print(q, re.findall(r'numberOfRecords>(\d+)', d))
    for rec in re.findall(r'<srw:record>(.*?)</srw:record>', d, re.S):
        i = re.findall(r'<dc:identifier>(.*?)</dc:identifier>', rec)
        t = re.findall(r'<dc:title>(.*?)</dc:title>', rec)
        print('  ', i[0] if i else '?', '|', (t[0] if t else '?')[:140])
