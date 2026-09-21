"""Search authenticated DECODE record listings without exposing the cookie."""

from pathlib import Path
import re
import sys
import urllib.parse
import urllib.request


root = Path(__file__).parent
cookie = re.sub(
    r"^cookie:\s*", "", (root.parent / "bordeaux" / "decode" / "cookie.txt").read_text(encoding="utf-8").strip(), flags=re.I
)
query = " ".join(sys.argv[1:])
url = "https://de-crypt.org/decrypt-web/RecordsList?search=" + urllib.parse.quote(query)
request = urllib.request.Request(url, headers={"Cookie": cookie, "User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(request, timeout=60) as response:
    text = response.read().decode("utf-8", errors="replace")
for record, title in re.findall(r"RecordsView/(\d+)[^>]*>(.*?)</a>", text, flags=re.S):
    clean = re.sub(r"<[^>]+>", " ", title)
    clean = re.sub(r"\s+", " ", clean).strip()
    print(record, clean)
