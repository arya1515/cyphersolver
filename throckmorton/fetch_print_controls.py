"""Fetch two public-domain printed pages for visual checks, without any cookie."""
import pathlib, urllib.request
root=pathlib.Path(__file__).resolve().parent/'sources'
for item,leaf,name in [
    ('bim_eighteenth-century_a-full-view-of-the-publi_1740_1',386,'forbes1_p355.jpg'),
    ('AFullViewofthePublicTransa007',44,'forbes2_p12.jpg')]:
    url=f'https://archive.org/download/{item}/page/n{leaf}.jpg'
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=30) as r:
        data=r.read()
    assert data[:3]==b'\xff\xd8\xff', 'Not JPEG'
    (root/name).write_bytes(data)
    print(name,len(data),url,flush=True)
