"""Scan the HMC Ormonde OCR text for runs of comma-separated numbers (cipher figures)."""
import re, sys
txt = open('ormonde1_djvu.txt', encoding='utf-8', errors='replace').read()
lines = txt.split('\n')
# join lines into paragraphs but remember line numbers
pat = re.compile(r'(\b\d{1,3}\b[,.]?\s+){3,}')
seen = set()
for i, ln in enumerate(lines):
    s = ln.strip()
    if pat.search(s + ' '):
        # ignore index-like lines (many numbers) : keep lines with few words
        nums = re.findall(r'\b\d{1,3}\b', s)
        if len(nums) >= 3 and not re.search(r'\b(1[5-7]\d\d)\b', s):
            print(i + 1, s)
