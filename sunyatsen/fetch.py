"""Fetch resources for the Sun Yat-sen 1916 telegram problem."""
import urllib.request, os
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(here, 'img'), exist_ok=True)
items = {
    'tw.csv': 'https://raw.githubusercontent.com/kirklin/chinese-telegraph-code/main/data/tw.csv',
    'cn.csv': 'https://raw.githubusercontent.com/kirklin/chinese-telegraph-code/main/data/cn.csv',
    'img/condenser3.png': 'https://cryptiana.web.fc2.com/code/chinesecrypto3.png',
    'img/condenser3b.png': 'https://cryptiana.web.fc2.com/code/chinesecrypto3b.png',
    'img/sun_telegram.png': 'https://cryptiana.web.fc2.com/code/chinesecrypto4.png',
    'img/huang_xing.png': 'https://cryptiana.web.fc2.com/code/chinesecrypto5.png',
}
for name, url in items.items():
    p = os.path.join(here, name)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=60).read()
        open(p, 'wb').write(data)
        print('ok', name, len(data))
    except Exception as e:
        print('FAIL', name, e)
