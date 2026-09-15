"""Convert fetched BHO HTML to plain text (thurloe/html/*.txt) and list cipher-heavy paragraphs."""
import os, re, glob, html as H
HERE = os.path.dirname(os.path.abspath(__file__))
def to_text(raw):
    m = re.search(r'<div[^>]*class="[^"]*(?:field--name-body|inner-content|node__content)[^"]*"[^>]*>(.*)', raw, re.S)
    body = m.group(1) if m else raw
    body = re.sub(r'<script.*?</script>|<style.*?</style>', '', body, flags=re.S)
    body = re.sub(r'<(p|div|br|h\d|li|tr)[^>]*>', '\n', body)
    body = re.sub(r'<[^>]+>', '', body)
    body = H.unescape(body)
    body = re.sub(r'[ \t\xa0]+', ' ', body)
    body = re.sub(r'\n\s*\n+', '\n\n', body)
    return body.strip()
for f in glob.glob(os.path.join(HERE, "html", "*.html")):
    raw = open(f, encoding="utf-8", errors="replace").read()
    txt = to_text(raw)
    out = f[:-5] + ".txt"
    open(out, "w", encoding="utf-8").write(txt)
    paras = txt.split("\n\n")
    print("=" * 70, os.path.basename(out), len(paras), "paras")
    for i, p in enumerate(paras):
        nums = re.findall(r'\b\d{1,4}\b', p)
        if len(nums) >= 25:
            print(f"  para {i}: {len(nums)} numbers | {p[:110]!r}")
