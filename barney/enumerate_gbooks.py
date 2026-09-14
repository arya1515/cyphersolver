"""Enumerate candidate Webster dictionary editions (1840-1863) via Google Books API."""
import requests, time, json, sys

QUERIES = [
    'intitle:dictionary inauthor:webster pocket',
    'intitle:"pocket dictionary" webster',
    'intitle:dictionary webster "army and navy"',
    'intitle:dictionary inauthor:webster abridged',
    'intitle:dictionary inauthor:webster "primary school"',
    'intitle:dictionary inauthor:webster "counting-house"',
    'intitle:dictionary inauthor:webster pronouncing',
    'intitle:dictionary inauthor:webster "high school"',
    'intitle:dictionary inauthor:webster "common school"',
    'intitle:dictionary inauthor:webster academic',
    'intitle:dictionary inauthor:webster university',
]

seen = {}
for q in QUERIES:
    for start in (0, 40, 80, 120):
        r = requests.get('https://www.googleapis.com/books/v1/volumes',
                         params={'q': q, 'maxResults': 40, 'startIndex': start, 'printType': 'books'})
        if r.status_code != 200:
            print('ERR', r.status_code, q, file=sys.stderr); break
        items = r.json().get('items', [])
        if not items: break
        for it in items:
            v = it['volumeInfo']; d = v.get('publishedDate', '')
            y = int(d[:4]) if d[:4].isdigit() else 0
            if 1835 <= y <= 1863:
                seen[it['id']] = dict(year=y, pages=v.get('pageCount'), title=v.get('title', '')[:80],
                                      subtitle=(v.get('subtitle') or '')[:80], publisher=v.get('publisher', ''),
                                      view=it['accessInfo'].get('viewability'))
        time.sleep(0.3)

rows = sorted(seen.items(), key=lambda x: (x[1]['pages'] or 0))
for k, v in rows:
    print(f"{k:14} {v['year']} {str(v['pages']):>5}p {v['view']:<10} {v['title']} | {v['subtitle']} | {v['publisher']}")
json.dump(seen, open('candidates_gbooks.json', 'w'), indent=1)
print(len(seen), 'candidates')
