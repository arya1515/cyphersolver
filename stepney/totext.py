"""Convert an HTML file to plain text: python totext.py in.htm out.txt"""
import re, html, sys

def totext(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8", "shift_jis", "cp1252"):
        try:
            s = raw.decode(enc)
            break
        except Exception:
            continue
    s = re.sub(r"(?is)<(script|style).*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h\d>|</li>|</tr>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s

if __name__ == "__main__":
    t = totext(sys.argv[1])
    open(sys.argv[2], "w", encoding="utf-8").write(t)
    print(len(t), "chars")
