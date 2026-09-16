"""Boswell cipher (1643): the numerical alphabet as reconstructed by R. Pitt (Sept 2026), re-implemented here.

Core: 20..115 -> row[(n-20) % 24], row = odd then even positions of the 24-letter alphabet abcdefghiklmnopqrstuwxyz.
Supplementary homophones 116..159 (frequent letters in alphabetical blocks), nulls 0..19 and 361..386,
word codes and the four graphic signs are hypotheses; see NOTES.md.
"""
import re

ALPHA24 = "abcdefghiklmnopqrstuwxyz"
ROW = ALPHA24[0::2] + ALPHA24[1::2]          # acegilnprtwybdfhkmoqsuxz
assert ROW == "acegilnprtwybdfhkmoqsuxz"

def core(n):
    if 20 <= n <= 115:
        return ROW[(n - 20) % 24]
    return None

SUPP = {116:'a',117:'d',118:'e',120:'m',121:'n',122:'o',123:'r',124:'s',125:'t',126:'y',
        127:'a',128:'d',129:'e',131:'n',132:'o',134:'t',135:'u',
        138:'e',141:'r',142:'s',
        145:'a',146:'e',147:'i',148:'o',149:'r',150:'s',151:'u',
        153:'a',154:'e',158:'u',159:'y'}
NULLS = set(range(0, 20)) | {361, 362, 364, 374, 376, 377, 380, 381, 386}
WORDS = {170:'Ambassadors', 185:'assistance', 188:'armes', 190:'are', 205:'assure', 223:'by', 228:'Bristol',
         291:'Duke', 303:'two', 406:'gener', 484:'his Majesty', 516:'letter', 539:'musket', 588:'of',
         591:'our', 629:'pray', 636:'pro', 639:'powder', 640:'port', 746:'secret', 749:'selves', 750:'send',
         755:'store', 800:'to', 835:'un', 851:'which', 854:'will', 873:'your'}
SIGNS = {'△':'good', '中':'Cousin', '□':'Master', '+':'us', '＋':'us'}

TOKEN = re.compile(r"\d+_?|[△中□+＋]|[A-Za-z\^\[\]\?\.&≪→≫\*]+|[,.;:()]")

def tokens(text):
    return TOKEN.findall(text)

def decode(text, words=True, signs=True, supp=True, nulls=True):
    out = []
    for t in tokens(text):
        if t.isdigit():
            n = int(t)
            c = core(n)
            if c: out.append(c.upper()); continue
            if supp and n in SUPP: out.append(SUPP[n].upper()); continue
            if nulls and n in NULLS: out.append('·'); continue
            if words and n in WORDS: out.append('{%s}' % WORDS[n]); continue
            out.append('[%d]' % n)
        elif t in SIGNS:
            out.append(('{%s}' % SIGNS[t]) if signs else t)
        else:
            out.append(t)
    return out
