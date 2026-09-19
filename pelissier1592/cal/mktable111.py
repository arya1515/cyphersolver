import json, subprocess
counts = subprocess.run(['python', 'table111.py'], capture_output=True, text=True).stdout
refs = json.load(open('refs111.json'))


def R(tok, let, k=6):
    v = refs.get(f'{tok}|{let}', [])
    return (' '.join(v[:k]) + (' ...' if len(v) > k else '')) or '-'


legend = '''# f.111r (no. 45) token -> letter table, from cal/align_111.txt (R1-R10 top half, R11-R23 bottom half to "conserver").
# Regenerate: python table111.py (counts) ; python mktable111.py (this file).  "_" = null, "?" = unresolved.
#
# TOKEN LEGEND (tokens beyond TOKENS.md, and splits of its merged families)
#  dp   delta with a straight/looped ascender and a round closed bowl (the "o" of TOKENS)      -> o
#  dc   delta whose top curls back over to the left in a hook (key c column, 1st cell)       -> c
#  D    small open-curl delta / backward-6, no ascender loop                                  -> e (once c)
#  Q    big open upper loop over a closed bowl (the r-glyph)                                   -> r
#  Q8   delta with a CLOSED loop on top of the bowl (8-like)                                   -> r  (8o, same family: o once)
#  rho  small p-loop (top half only)                                                            -> o / l
#  qo   ring sitting on a straight descender (female-sign shape)                               -> a (11), o (1, "volonte")
#  q9   9-shaped: open bowl + descender                                                        -> f
#  q    top-half transcription of the ring-on-stem family (not split there)                    -> a
#  T    flat-topped T                                                                          -> a
#  Tr   small T whose bar ends in a hook to the right (tau)                                    -> s
#  Tp   T with hooked top (top half, "par")                                                    -> p
#  T~   top-half name for pi/T with a tail                                                     -> s
#  T+   T whose stem is crossed (dagger-like)                                                  -> a
#  f    tall long-s crossed by a bar (reaching well above the line)                            -> a (once e)
#  t    small crossed t / epsilon-with-tail                                                    -> e
#  t4   small t with a tail (only in "que", R20)                                               -> q?
#  4    plain 4                                                                                -> n (24), m (5), t (2)
#  4_   4 with a base / cross foot (top half)                                                  -> m
#  4y   4 whose cross-stroke ends in a curl/loop                                               -> t
#  z4   z joined to 4                                                                          -> t
#  8    plain 8                                                                                -> n (19), q (3)
#  8o   8 with an open looped ascender                                                         -> o ("honnestete")
#  B8   8 crossed by a slanting stroke                                                         -> u ("une")
#  Z    8/x in a box                                                                           -> s ("use"), z ("hazard")
#  X    x whose lower-left stroke has a loop / bar                                             -> u / v
#  #x   bold plain X-cross (the null form)                                                     -> null
#  x    small plain x                                                                          -> a
#  Hh   slanted H preceded by a 6-shaped lead-in loop                                          -> q ("que") and g ("guelle", "longuement")
#  H    plain slanted H                                                                        -> q
#  hb   h with a bar through the stem ("m'est")                                                -> s?
#  7    y-shape / 7 with crossbar                                                              -> h (top half), b ("bonne"); 7b = b ("tumber")
#  eL   loop-l                                                                                 -> u
#  u    small cursive u                                                                        -> d (4x)
#  n    top-half cursive n                                                                     -> d
#  d    looped-ascender d                                                                      -> u
#  s6c / s6   flourished 56: the 5 is a long s-like stroke with a hook, the 6 sits high       -> c
#  56   compact plain "56"                                                                     -> y (Ducroy, jay) ; c in R17 "indiscretement" (flourished form, see atlas c_56)
#  6^   6/8 with a flat bar on top                                                             -> i
#  lam  lambda-like cross with long ascending stroke                                           -> null
#  V    v-shape (R20 "grandeur")                                                               -> g?
#  Fo/Fu top-half split of F (double-barred) read o / u;  F (bottom half)                      -> o
#  K / k                                                                                       -> s
#  dz   delta over z ligature                                                                  -> s
#  J    tall double long-s                                                                     -> ss (once s, "sieur")
#  II   box-like double bar -> l ;  I plain barred I -> l ;  Lo bold-footed inverted T -> o
#  tt   pi with an s-like hook on top                                                          -> i ("mettrois"), s (top half)
#  Other tokens as in TOKENS.md.
'''

dis = '''
# DISAGREEMENTS with Tomokiyo's key (league2_key.png) / TOKENS.md, with row refs (Rn.i = row n, i-th token)
- 4  = m: %s  [me, commettre, on m'a, tement]. Plain 4 = t: %s.
     Shape check (atlas m_4_*, n_4_*): m-4s are not visibly different from n-4s; the n-4 of "pardon" even has a foot bar.
- 8  = q: %s ("que" x3).
- X  = null: %s (bold plain cross; the looped/barred X is always u/v).
- A  = v: %s ; A read i? once in "prejudice" (R20).
- 6  = i: %s ; = y: %s ; = d: %s.
- 56 = y: %s (compact 56: Ducroy, jay); the flourished s6/s6c = c. TOKENS says 56 = c always.
- qo (ring-on-stem, key a) = o: %s ("volonte").
- 36 = o: %s ("volonte", key u).
- Hh = g: %s ("guelle", "longuement"); = q in "que": %s.
- Tr (tau) = s: %s.
- f (tall crossed long-s, key a) = e once: %s.
- E: square E = p %s ; round epsilon (e3) = e; E read e: %s.
- pi = j: %s ; 33 = j: %s (i/j same letter).
- tt = i (key s): %s.
- hb = s (not in key) %s ; t4 = q? %s.
- 7 = b (key h): %s ; 7b %s.
- B8 = u (not in key): %s.
- Z = s: %s ; Z = z: %s.
- 44 = y, 60 = y, 24 = o, 26 = p, 28 = q, 19 = f, 33 = i/j: as in the key.
- Signs not in the key/TOKENS: hb, B8, T+, Hh (as q/g), t4, V; lighter-ink corrections (Lo/8/pi/4 in R21, dc in R16).
''' % (R('4', 'm'), R('4', 't'), R('8', 'q'), R('X', '_'), R('A', 'v'), R('6', 'i'), R('6', 'y'), R('6', 'd'),
       R('56', 'y'), R('qo', 'o'), R('36', 'o'), R('Hh', 'g'), R('Hh', 'q'), R('Tr', 's'), R('f', 'e'), R('E', 'p'),
       R('E', 'e'), R('pi', 'j'), R('33', 'j'), R('tt', 'i'), R('hb', 's'), R('t4', 'q'), R('7', 'b'), R('7b', 'b'),
       R('B8', 'u'), R('Z', 's'), R('Z', 'z'))

open('table_111.txt', 'w', encoding='utf-8').write(legend + '\n# COUNTS  token  n  letter:count ...\n' + counts + dis)
