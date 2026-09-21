"""Fetch the authorized DECODE text transcriptions without exposing the cookie."""

from pathlib import Path
import re
import urllib.request


ROOT = Path(r"rakoczi1704").resolve()
BASE = "https://de-crypt.org"
COOKIE_PATH = Path(r"C:/Users/dbour/cypher/bordeaux") / "decode" / "cookie.txt"
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
        if len(data) == 17947 or "forbidden" in response.headers.get(
            "Content-Disposition", ""
        ).lower():
            raise RuntimeError("Stored DECODE cookie was rejected")
        return data


for record_id in (483, 852, 912, 922):
    record_url = f"{BASE}/decrypt-web/RecordsView/{record_id}"
    html = get(record_url)
    names = sorted(
        set(re.findall(rb"filesrv/\?file=(DOC_[A-Za-z0-9_.]+)", html))
    )
    print(f"R{record_id}: {len(names)} transcription(s)")
    for raw_name in names:
        name = raw_name.decode("ascii")
        data = get(f"{BASE}/decrypt-custom/filesrv/?file={name}", record_url)
        output = ROOT / name
        output.write_bytes(data)
        print(f"  {output.name}: {len(data)} bytes")
