# -*- coding: utf-8 -*-
"""Decode an ASCII-alias transcription of Gramont's cipher (1529) (Lasry key, BnF fr. 3040 f. 16).

Usage: python decode.py "alias string"   (or pipe lines on stdin)
Spaces are ignored; text inside [brackets] is copied through (clear text / notes).
"""
import sys, re

KEY = {
    # A
    'o': 'a', 'A': 'a', 'H': 'a',
    'B': 'b', 'C': 'c', '+': 'd',
    'L': 'e', 'R': 'e', 'W': 'e',
    'F': 'f', 'G': 'g', '7': 'h',
    '4': 'i', 'J': 'i', 'i': 'i', 'Y': 'i',
    'l': 'l', '#': 'm', '8': 'n',
    'q': 'o', 'g': 'o', 'X': 'o',
    'v': 'p', 'b': 'q', 'r': 'r', 's': 's',
    't': 't', 'd': 't',
    'k': 'v', 'n': 'v', 'e': 'v',
    'z': 'x', 'y': 'z',
    '=': 'll', 'M': 'mm', 'N': 'nn', 'P': 'pp', 'U': 'rr', 'S': 'ss', 'E': 'tt',
    'T': '&', '&': '<P>', 'c': 'con',
    '|': '', ')': '', '~': '', 'f': '',
    '!': '?', '?': '?',
}

def decode(s):
    out = []
    for part in re.split(r'(\[[^\]]*\])', s):
        if part.startswith('['):
            out.append(part); continue
        for ch in part:
            if ch.isspace(): continue
            out.append(KEY.get(ch, '{%s}' % ch))
    return ''.join(out)

if __name__ == '__main__':
    src = sys.argv[1:] and [' '.join(sys.argv[1:])] or sys.stdin.read().splitlines()
    for line in src:
        print(decode(line))
