import urllib.request, re, sys
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0"
url = "https://www.british-history.ac.uk/thurloe-papers/vol1"
req = urllib.request.Request(url, headers={"User-Agent": UA})
html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
links = sorted(set(re.findall(r'thurloe-papers/vol1/(pp\d+-\d+)', html)))
for l in links:
    a, b = map(int, l[2:].split("-"))
    if a <= 440 and b >= 425:
        print("TARGET", l)
print(len(links), "links; sample:", links[:5], links[-5:])
