#!/usr/bin/env python3
"""Decode the published Forster passage using a supplied proposed key.

This is a decoder, not an autonomous solver or proof of historical accuracy.
It uses no candidate plaintext and applies no editorial letter repairs.
Python 3.9+; standard library only. Run:
    python decode_forster.py
    python decode_forster.py --alignment
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

CLEAR_ONE = "ie vous en responds et mesmes dans"
CLEAR_TWO = "et mesurer a cela sil est meilleur"
TOKEN = re.compile(r"\d+|[a-z]")


def decode(source: str, key: dict[str, str]) -> dict:
    if source.count(CLEAR_ONE) != 1 or source.count(CLEAR_TWO) != 1:
        raise ValueError("Expected exactly the two declared existing-plaintext spans")
    first, rest = source.split(CLEAR_ONE)
    second, last = rest.split(CLEAR_TWO)
    if not all(isinstance(k, str) and isinstance(v, str)
               and re.fullmatch(r"[a-z]", v) for k, v in key.items()):
        raise ValueError("Key entries must map string tokens to one lowercase letter")
    groups, split_at = [], None
    for block_no, block in enumerate((first, second)):
        # Validate each dot/comma-separated element, rather than silently
        # interpreting an unexpected word as individual cipher symbols.
        for element in re.split(r"[.,\s]+", block.strip()):
            if element and not TOKEN.fullmatch(element):
                raise ValueError(f"Unexpected cipher element: {element!r}")
        for group in block.split(','):
            tokens = TOKEN.findall(group)
            if tokens:
                unknown = set(tokens) - key.keys()
                if unknown:
                    raise ValueError("Unmapped symbols: " + ', '.join(sorted(unknown)))
                groups.append({'tokens': tokens,
                               'literal': ''.join(key[token] for token in tokens)})
        if block_no == 0:
            split_at = len(groups)
    all_tokens = [t for g in groups for t in g['tokens']]
    return {'groups': groups, 'split_at': split_at,
            'clear_one': CLEAR_ONE, 'clear_two': CLEAR_TWO + last.rstrip(),
            'token_count': len(all_tokens), 'frequencies': Counter(all_tokens)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--alignment', action='store_true')
    args = parser.parse_args()
    try:
        key = json.loads((args.data_dir/'recovered_key.json').read_text('utf-8'))['mapping']
        source = (args.data_dir/'ciphertext_source.txt').read_text('utf-8')
        result = decode(source, key)
        print('LITERAL DECODING WITH THE SUPPLIED PROPOSED KEY')
        print(f"{result['token_count']} cipher tokens; "
              f"{len(result['frequencies'])} distinct symbols")
        print('No editorial repairs; f -> b is a tentative lexical assignment.\n')
        split = result['split_at']
        groups = result['groups']
        print(', '.join(g['literal'] for g in groups[:split]))
        print('[ALREADY PLAINTEXT] ' + result['clear_one'])
        print(', '.join(g['literal'] for g in groups[split:]))
        print('[ALREADY PLAINTEXT] ' + result['clear_two'])
        if args.alignment:
            print('\nCOMPLETE CIPHER GROUP ALIGNMENT')
            offset = 0
            for i, group in enumerate(groups, 1):
                n = len(group['tokens'])
                print(f"{i:2}. {offset+1:3}-{offset+n:3}: "
                      f"{' '.join(group['tokens'])} -> {group['literal']}")
                offset += n
                if i == split:
                    print('[ALREADY PLAINTEXT] ' + result['clear_one'])
            print('[ALREADY PLAINTEXT] ' + result['clear_two'])
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'Decoding failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
