"""Lossless, conservative DECODE token audit; does not infer missing separators.

Run from any directory. Originals and previous ct*.txt are left intact.
Marks are retained in JSON; numeric projections are hypotheses that ignore underlining.
"""
from pathlib import Path
import collections
import json
import re

ROOT = Path(__file__).resolve().parent


def tokens(text):
    page = None
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.startswith('#IMAGE NAME:'):
            page = line.partition(':')[2].strip()
        if line.startswith('#'):
            continue
        # Remove only tagged cleartext, retaining cipher on BOTH sides.
        line = re.sub(r'<[^>]*>', '', line)
        for raw in re.split(r'[.,:]', line):
            raw = raw.strip()
            if not raw:
                continue
            compact = re.sub(r'\s+', '', raw)
            digits = compact.replace('_', '').replace('^', '')
            status = 'numeric' if re.fullmatch(r'\d{1,4}', digits) else 'unresolved'
            # The untagged heading year is demonstrably not ciphertext.
            if page == '13447.png' and raw == '1752':
                status = 'clear-heading'
            yield dict(line=lineno, page=page, raw=raw, compact=compact,
                       value=int(digits) if status == 'numeric' else None,
                       status=status, marked=('_' in raw or '^' in raw))


def main():
    records = {}
    summary = {}
    out = ROOT / 'audit'
    out.mkdir(exist_ok=True)
    for path in sorted((ROOT / 'decode').glob('DOC_*.txt')):
        rid = re.search(r'R(\d+)', path.name)[1]
        rows = list(tokens(path.read_text(encoding='utf-8-sig')))
        records[rid] = rows
        numeric = [t['value'] for t in rows if t['status'] == 'numeric']
        summary[rid] = dict(segments=sum(t['status'] != 'clear-heading' for t in rows),
                            numeric=len(numeric), distinct_numeric=len(set(numeric)),
                            unresolved=sum(t['status'] == 'unresolved' for t in rows),
                            marked=sum(t['marked'] for t in rows),
                            most_common=collections.Counter(numeric).most_common(8))
        (out / f'R{rid}.txt').write_text(' '.join(
            t['compact'] for t in rows if t['status'] != 'clear-heading') + '\n', encoding='utf8')
    (out / 'tokens.json').write_text(json.dumps(records, indent=2), encoding='utf8')
    (out / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf8')
    (out / 'set1763.txt').write_text('\n'.join(
        (out / f'R{rid}.txt').read_text(encoding='utf8').strip()
        for rid in ('1045', '1046', '1047', '1048', '1060', '1061')) + '\n', encoding='utf8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
