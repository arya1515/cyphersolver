"""Download the DECODE files listed in MANIFEST.md using a logged-in browser cookie.

Usage:  python fetch_decode.py 92 [91 93 94 ...]
Needs:  cookie.txt in this folder = the value of the Cookie: header of a de-crypt.org request made
        while logged in (copy from the browser dev tools, Network tab). Delete it when done.

Files land in this folder under their DECODE names. A download that comes back as the 17947-byte
"forbidden.png" placeholder (what the server returns without a valid session) is deleted and reported.
"""
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://de-crypt.org"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"

# from the public RecordsView pages, 2026-09-16
FILES = {
    92: ["IMG_R92_I%d_P%d.jpg" % (691 + i, i + 1) for i in range(8)]
        + ["DOC_R92_D1633_1633.txt", "DOC_R92_D1211_1211.png"],
    91: ["IMG_R91_I%d_P%d.jpg" % (682 + i, i + 1) for i in range(5)]
        + ["DOC_R91_D2341_2341.txt"] + ["DOC_R91_D%d_%d.png" % (d, d) for d in range(1207, 1211)],
    93: ["IMG_R93_I700_P1.jpg", "DOC_R93_D1664_1664.txt", "DOC_R93_D3287_3287.txt"]
        + ["DOC_R93_D%d_%d.png" % (d, d) for d in range(1212, 1220)],
    94: ["IMG_R94_I709_P1.jpg", "DOC_R94_D1665_1665.txt", "DOC_R94_D3285_3285.txt"]
        + ["DOC_R94_D%d_%d.png" % (d, d) for d in range(1220, 1238)],
}
FORBIDDEN_LEN = 17947


def load_cookie():
    p = os.path.join(HERE, "cookie.txt")
    if not os.path.exists(p):
        sys.exit("cookie.txt not found next to this script; see MANIFEST.md, option B")
    c = open(p, encoding="utf-8").read().strip()
    c = re.sub(r"^cookie:\s*", "", c, flags=re.I)
    return c


def fetch(name, cookie, rec):
    out = os.path.join(HERE, name)
    if os.path.exists(out) and os.path.getsize(out) not in (0, FORBIDDEN_LEN):
        return "have"
    req = urllib.request.Request(BASE + "/decrypt-custom/filesrv/?file=" + name, headers={
        "User-Agent": UA, "Cookie": cookie,
        "Referer": BASE + "/decrypt-web/RecordsView/%d" % rec,
    })
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
        disp = r.headers.get("Content-Disposition", "")
    if len(data) == FORBIDDEN_LEN or "forbidden" in disp:
        return "FORBIDDEN (cookie not accepted)"
    with open(out, "wb") as f:
        f.write(data)
    return "%d bytes" % len(data)


def main():
    recs = [int(a) for a in sys.argv[1:]] or [92]
    cookie = load_cookie()
    bad = 0
    for rec in recs:
        for name in FILES[rec]:
            try:
                res = fetch(name, cookie, rec)
            except Exception as e:  # noqa: BLE001
                res = "ERROR %s" % e
            print("R%d %-28s %s" % (rec, name, res))
            if res.startswith(("FORBIDDEN", "ERROR")):
                bad += 1
                if res.startswith("FORBIDDEN"):
                    sys.exit("session cookie rejected; copy a fresh Cookie header into cookie.txt")
            time.sleep(0.5)
    print("done, %d failures" % bad)


if __name__ == "__main__":
    main()
