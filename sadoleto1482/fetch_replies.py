"""Fetch the public Vestigia reply records and their catalogued web images."""
import html
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parent

def fetch(url):
    with urllib.request.urlopen(url, timeout=40) as response:
        return response.read()

if __name__ == '__main__':
    for number in (1252, 1250, 1251):
        target = ROOT / 'vestigia' / f'v{number}.json'
        if target.exists():
            data = json.loads(target.read_text(encoding='utf-8'))
        else:
            page = fetch(f'https://www.vestigia.hu/documents/{number}').decode()
            match = re.search(r'data-page="(.*?)"', page)
            if match is None:
                raise ValueError(f'No public record JSON for {number}')
            data = json.loads(html.unescape(match.group(1)))
            target.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
        document = data['props']['document']
        print(number, document['date_from'], document['archive_ref'])
        for index, item in enumerate(document['files'], 1):
            image = ROOT / 'img' / 'v' / f'reply{number}_{index}.jpg'
            if not image.exists():
                image.write_bytes(fetch(item['web_url']))
            print(' ', index, item['name'], image.stat().st_size)
