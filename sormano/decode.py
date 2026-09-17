# -*- coding: utf-8 -*-
"""Decode Sormano cipher transcriptions (Lasry key, fr. 3096).

Transcription alphabet (ASCII aliases, space-separated tokens or compact):
  v u w 3 -> a   (w = square-topped n-like 'a' glyph)
  b        -> b   (tau)
  c        -> c   (triangle up)
  C        -> cc  (double-crossed slash)
  d        -> d   (e with left tail)
  e k g 7  -> e   (n-tail, k, gamma-tick, seven-with-foot)
  f        -> f   (ff ligature)
  S        -> g   (S)
  h        -> h   (capital E serifed)
  y o p 4  -> i   (forked Y, dotted circle, p, four)
  L        -> ll  (dotted lozenge)
  9        -> l   (ring with straight descender)
  m        -> m   (B with lead-in stroke)
  n        -> n   (pi, overhanging bar)
  U 1 5    -> o   (u with descender, one, delta-with-ring-below)
  6        -> p
  q        -> q   (triangle down)
  r        -> r   (ring with SE tail)
  z s      -> s   (double-crossed z, dotted open square)
  t        -> t   (light x)
  T a Y H  -> v   (heavy-T, alpha, gamma-tick-v, H)
  X        -> x   (bold saltire)
  .        -> (word sep guess)
"""
import sys
M = {
 'v':'a','u':'a','w':'a','3':'a',
 'b':'b','c':'c','C':'cc','d':'d',
 'e':'e','k':'e','g':'e','7':'e',
 'f':'f','S':'g','h':'h',
 'y':'i','o':'i','p':'i','4':'i',
 'L':'ll','9':'l','m':'m','n':'n',
 'U':'o','1':'o','5':'o',
 '6':'p','q':'q','r':'r',
 'z':'s','s':'s','t':'t',
 'T':'v','a':'v','Y':'v','H':'v',
 'X':'x',
 ' ':' ', '.':' ', '|':'|','-':'?','\n':'\n'
}
def dec(s):
    return ''.join(M.get(ch,'['+ch+']') for ch in s)
if __name__=='__main__':
    txt = sys.stdin.read() if not sys.argv[1:] else ' '.join(sys.argv[1:])
    print(dec(txt))
