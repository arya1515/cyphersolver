"""Queue a target's DECODE edits in decode_updates/queue.json.

  python decode_updates/queue.py add <folder>        add the target's DECODE records, pre-filled from profile.json
  python decode_updates/queue.py status [<folder>]   what is queued, what still says TODO
  python decode_updates/queue.py skip <folder> "<why>"  record that the target needs no DECODE edit

`add` takes the record numbers (R1234) from the profile's documents, fetches each record's current DECODE status
when bordeaux/decode/cookie.txt still logs in, and writes TODO wherever a judgement is needed: the proposed
status, the note, the key source and the reading file. Fill those in by hand, then run build.py.
"""
import json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = os.path.join(ROOT, 'decode_updates', 'queue.json')
SITE = 'https://dbourdeau.github.io/cyphersolver/'
STATUS = {'1': 'Decrypted', '2': 'Non-decrypted', '3': 'Partially decrypted', '4': 'N/A'}


def load():
    return json.load(open(Q, encoding='utf-8'))


def save(data):
    with open(Q, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write('\n')


def decode_ids(folder):
    p = json.load(open(os.path.join(ROOT, folder, 'profile.json'), encoding='utf-8'))
    ids = []
    for d in p['documents']:
        for n in re.findall(r'\bR ?(\d{2,5})\b', d['id'] + ' ' + d['shelfmark']):
            if n not in ids:
                ids.append(n)
    return p, ids


def current_status(ids):
    """Current DECODE status per record, or {} when the cookie no longer logs in."""
    try:
        # the cookie is git-ignored, so a worktree reads the main checkout's copy
        common = os.path.dirname(os.path.abspath(os.popen(f'git -C "{ROOT}" rev-parse --git-common-dir').read().strip()))
        path = next(p for p in (os.path.join(r, 'bordeaux', 'decode', 'cookie.txt') for r in (ROOT, common))
                    if os.path.exists(p))
        cookie = open(path, encoding='utf-8').read().strip()
        h = {'Cookie': cookie, 'User-Agent': 'Mozilla/5.0'}
        page = urllib.request.urlopen(urllib.request.Request(
            f'https://de-crypt.org/decrypt-web/RecordsView/{ids[0]}', headers=h), timeout=30).read().decode('utf-8', 'replace')
        jwt = re.search(r'"API_JWT_TOKEN":"([^"]+)"', page).group(1)
        out = {}
        for n in ids:
            r = urllib.request.urlopen(urllib.request.Request(
                f'https://de-crypt.org/decrypt-web/api/view/Records/{n}',
                headers={**h, 'X-Authorization': f'Bearer {jwt}'}), timeout=30).read()
            rec = json.loads(r)['records']
            out[n] = STATUS.get(rec.get('status'), 'blank') + (' (key record)' if rec.get('record_type') == '2' else '')
        return out
    except Exception as e:
        print(f'  (could not read DECODE statuses: {e}; filling TODO)')
        return {}


def guess_reading(folder, n):
    for f in (f'read/R{n}.txt', f'read/R{n}.md', f'reading_R{n}.txt', f'read_r{n}.md', f'r{n}.read.txt'):
        if os.path.exists(os.path.join(ROOT, folder, f)):
            return [{'file': f'{folder}/{f}'}]
    return 'TODO'


def add(folder):
    data = load()
    p, ids = decode_ids(folder)
    if not ids:
        print(f'{folder}: the profile names no DECODE record; nothing to queue (use skip if that is right)')
        return
    st = current_status(ids)
    t = data['targets'].setdefault(folder, {
        'writeup': SITE + folder + '.html', 'key': {'decode': 'TODO: DECODE id of the key, or replace with file/lang/how'},
        'cite': 'TODO or null', 'fields': {}, 'records': {}})
    added = []
    for n in ids:
        rec = 'R' + n
        if rec in t['records']:
            continue
        t['records'][rec] = {'decode_status': st.get(n, 'TODO'), 'proposed': 'TODO', 'note': 'TODO',
                             'reading': guess_reading(folder, n), 'sent': False}
        added.append(rec)
    save(data)
    print(f'{folder}: queued {len(added)} record(s): {", ".join(added) or "none new"}. Outcome in profile: '
          f'{p["outcome"].get("class")}. Fill the TODO fields (drop records that are only keys or siblings), '
          f'then run python decode_updates/build.py {folder}')


def todos(t):
    return [f'{k}' for k in ('key', 'cite') if 'TODO' in json.dumps(t.get(k))] + \
           [f'{r}.{k}' for r, v in t.get('records', {}).items() for k, x in v.items() if 'TODO' in json.dumps(x)]


def status(folder=None):
    data = load()
    for name, t in data['targets'].items():
        if folder and name != folder:
            continue
        if t.get('skip'):
            print(f'{name}: skipped ({t["skip"]})')
            continue
        recs = t.get('records', {})
        sent = sum(1 for v in recs.values() if v.get('sent'))
        td = todos(t)
        print(f'{name}: {len(recs)} records, {sent} sent' + (f'; TODO in {", ".join(td[:6])}' + (' …' if len(td) > 6 else '') if td else ''))


def skip(folder, why):
    data = load()
    data['targets'].setdefault(folder, {})['skip'] = why
    save(data)
    print(f'{folder}: marked as needing no DECODE edit ({why})')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['add'] and len(a) == 2:
        add(a[1])
    elif a[:1] == ['status']:
        status(a[1] if len(a) > 1 else None)
    elif a[:1] == ['skip'] and len(a) == 3:
        skip(a[1], a[2])
    else:
        print(__doc__)
