"""Fetch the three authorized DECODE records without printing the session cookie."""
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
BASE = "https://de-crypt.org"
COOKIE_PATH = ROOT.parent / "bordeaux" / "decode" / "cookie.txt"
cookie = re.sub(
    r"^cookie:\s*", "", COOKIE_PATH.read_text(encoding="utf-8").strip(), flags=re.I
)


def get(url: str, referer: str | None = None) -> bytes:
    headers = {"User-Agent": "Mozilla/5.0", "Cookie": cookie}
    if referer:
        headers["Referer"] = referer
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
        if (
            len(data) == 17947
            or "forbidden" in response.headers.get("Content-Disposition", "").lower()
        ):
            raise RuntimeError("Stored DECODE cookie was rejected")
        return data


record_ids = tuple(map(int, sys.argv[1:])) or (1026, 1027, 1893)
for record_id in record_ids:
    record_url = f"{BASE}/decrypt-web/RecordsView/{record_id}"
    html = get(record_url)
    (ROOT / "decode").mkdir(exist_ok=True)
    (ROOT / "decode" / f"record_{record_id}.html").write_bytes(html)
    text = html.decode("utf-8", errors="replace")
    names = sorted(
        set(
            re.findall(
                r"filesrv/\?file=(?:TH_)?((?:IMG|DOC)_[A-Za-z0-9_.]+)", text
            )
        )
    )
    print(f"R{record_id}: {len(names)} files")
    for name in names:
        output = ROOT / "decode" / name
        if output.exists():
            continue
        data = get(f"{BASE}/decrypt-custom/filesrv/?file={name}", record_url)
        output.write_bytes(data)
        print(f"  {name}: {len(data)} bytes")
