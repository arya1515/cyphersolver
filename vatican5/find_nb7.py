"""Find Nuntiaturberichte aus Deutschland I. Abt. Bd. 7 (Poggio 1541-44) on Internet Archive and grep for our letter."""
import requests, re, sys, pathlib
HERE = pathlib.Path(__file__).parent
ids = """nuntiaturberich00unkngoog nuntiaturberich03deugoog nuntiaturberich10romgoog nuntiaturberich13romgoog nuntiaturberich09romgoog
bub_gb_7zGxAAAAIAAJ nuntiaturberich00deugoog nuntiaturberich02romgoog bub_gb_kimxAAAAIAAJ nuntiaturberich14romgoog bub_gb_5zKxAAAAIAAJ
nuntiaturberich02deugoog bub_gb_IjWxAAAAIAAJ nuntiaturberich08romgoog nuntiaturberich00romgoog bub_gb_fTmxAAAAIAAJ bub_gb_yCqxAAAAIAAJ
nuntiaturberich03romgoog nuntiaturberich06romgoog nuntiaturberich01romgoog bub_gb_JjaxAAAAIAAJ bub_gb_VtBdAAAAIAAJ bub_gb_YTCxAAAAIAAJ
bub_gb_OzGxAAAAIAAJ_2 bub_gb_HjGxAAAAIAAJ nuntiaturberich05romgoog nuntiaturberich07romgoog nuntiaturberich04romgoog nuntiaturberich11romgoog
nuntiaturberich12romgoog nuntiaturberich01deugoog""".split()

def txt_url(id_):
    meta = requests.get(f'https://archive.org/metadata/{id_}', timeout=60).json()
    files = [f['name'] for f in meta.get('files', []) if f['name'].endswith('_djvu.txt')]
    return (f"https://archive.org/download/{id_}/{files[0]}" if files else None), meta.get('metadata', {})

for id_ in ids:
    try:
        url, md = txt_url(id_)
    except Exception as e:
        print(id_, 'ERR', e); continue
    vol = md.get('volume', ''); year = md.get('year', md.get('date', ''))
    if not url:
        print(id_, vol, year, 'no txt'); continue
    p = HERE / f'nb_{id_}.txt'
    if not p.exists():
        r = requests.get(url, timeout=300); p.write_bytes(r.content)
    t = p.read_text(encoding='utf-8', errors='ignore')
    head = re.sub(r'\s+', ' ', t[:3000])
    m = re.search(r'(Erster|Zweiter|Dritter|Vierter|F.nfter|Sechster|Siebenter|Siebter|Achter|Neunter|Zehnter|Elfter|Zw.lfter)\s+Band', head)
    poggio = len(re.findall(r'Poggio', t)); spira = len(re.findall(r'Spira|Speier|Speyer', t))
    a1542 = len(re.findall(r'April 1542|Aprile 1542|aprile 1542', t))
    print(f'{id_:28} vol={vol!s:10} {year!s:6} {m.group(0) if m else "?":16} Poggio={poggio:4} Speyer={spira:4} Apr1542={a1542:3} size={len(t)//1000}k')
