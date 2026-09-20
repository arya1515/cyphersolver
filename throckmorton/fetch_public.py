"""Cache public reference pages; no authentication is sent."""
import pathlib, urllib.request, sys
root = pathlib.Path(__file__).resolve().parent / 'sources'
root.mkdir(exist_ok=True)
sources = list(zip(sys.argv[1::2], sys.argv[2::2])) if len(sys.argv)>1 else [
    ('elizabeth.html', 'https://cryptiana.web.fc2.com/code/elizabeth.htm'),
    ('csp2.html', 'https://www.british-history.ac.uk/cal-state-papers/foreign/vol2'),
]
for name, url in sources:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=40) as r:
            data=r.read()
        (root/name).write_bytes(data)
        print(name, len(data), flush=True)
    except Exception as e:
        print(name, type(e).__name__, str(e), flush=True)
