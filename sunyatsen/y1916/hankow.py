"""Hankow -> 'Nakayama, 109 Aoyama Harajuku' (Sun), No. 4571, 13 Apr 1916 (JACAR B03050088400, frame 0517).
Ten-digit groups = standard telegraph code + 111 on every four-digit code (the scheme Consul Segawa reported
on 11 May 1916 for Sun's Hankow traffic, here without the digit reversal). Found by brute force of
additive 0..9999 x digit reversal x offset: -111 is 175 log-points clear of the next."""
import sys, io, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from family import code2ch
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
CT = ("3087346342 1006310168 2591019762 9373471930 0174561301 1966976724 7304723107 5004686863 2828022166 "
      "2228616774 6662104972 9201223745 2625014705 7701971911 1680368933 0072311082 2700011405 4402210117 "
      "2272237001 1656130779 5998300501 1907796752 2709675431 9373044466 0448")
s = CT.replace(' ', '')
codes = ['%04d' % ((int(s[i:i+4]) - 111) % 10000) for i in range(0, len(s), 4)]
print(' '.join(codes))
print(''.join(code2ch.get(c, '□') for c in codes))
