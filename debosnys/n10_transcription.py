"""Transcription of the 4 cipher lines on page No. 10 (c3.png), above the clear French poem.

Same conventions as verse_transcription.py; codes new to this page:
  PIC_FIGURE flying human figure   PIC_TREE   PIC_HORSE   PIC_GRAVE tombstone marked M   STAR2 rayed sun without a face
  ARCH_COLON arch over dots   PHI ϕ   II_EQ_O ticks, bars, o   UPS_BAR_O ϒ with bar and ring   II_O ticks over o
  CARET_RING caret with ring above (and dot)   N2_X double tilde over x   BOX_O rhombus with o/dot   XDD X dotted above and below
  CROSS +   O_BAR_II o, bar, two ticks   PAREN_SLO bracket with +/o   DELTA_BAR Δ with bar above   N_DASH_D tilde over -.-
  X_DOTBELOW X with dot below   SL2_O double slash with o   N_BAR_O tilde, bar, o   Z_CROSS 2 over double cross
  II_BAR_U ticks, bar, cup   V_X V with x above   ARCH_O arch over o   Z_X ℨ-like x   Y_VENUS chevron with small ♀
  UPS_BAR ϒ with bar   V_LOOP looped v   O_BAR_U ring, bar, cup   N2_COLON double tilde over two dots   AMPER 8-like curl
  EQ3_X three bars over x   CRES_DOT small crescent with dot   CHEV_DOT dot with chevron   CX_BAR underlined cursive x
  ARCH_TO arch with t and o   TAURUS_PLUS ♉ with cross   Y_RING_O Y with ring above and o below
"""

N10 = [
    "PIC_FIGURE N_OX SL(o,d) ARCH_COLON PHI II_EQ_O SL(o,x) UPS_BAR_O XD II_O BSL(x,x) CARET_RING N2_X BOX_O XDD CROSS "
    "PIC_TREE CHEV_DASH O_BAR_II SL(y,o) N_OX ARCH_BAR_O PIC_HORSE XD N_OX O_BAR_II PAREN_SLO",
    "PIC_SUN DELTA_BAR N_DASH_D SL(o,x) UPS_BAR_O X_DOTBELOW OSLASH II_EQ ARCH_EQ DSMALL N_COLON SL2_O N_BAR_O XD SL(y,o) "
    "Z_CROSS OSLASH II_BAR_U V_X ARCH_O CX Z_X XD N_OX SL(o,x) II_BAR_O BSL(x,o) TCURL XD PIC_GRAVE",
    "Y_VENUS N_X BSL(d,o) UPS_BAR V_LOOP O_BAR_U XD SL(o,o) II_BAR_O SL(x,x) N_O , BOX_O N2_COLON SL(y,o) XS2 AMPER , ALPHA "
    "EQ3_X CRES_DOT STAR2 DSMALL N_OX SL(o,o) CC_BAR_O XD HX CHEV_DOT CX_BAR XD OPLUS",
    "ARCH_TO SL(o,t) II_BAR_O CARET_RING TCURL OPLUS CHEV_DASH VENUS X TAURUS_PLUS Y_RING_O ARCH_EQ_X ?",
]


def tokens(drop_pictograms=False):
    out = []
    for l in N10:
        for t in l.split():
            if t in (',', '?', '.'): continue
            if drop_pictograms and (t.startswith('PIC') or t == 'STAR2'): continue
            out.append(t)
    return out


if __name__ == '__main__':
    import collections
    t = tokens(); c = collections.Counter(t)
    print(len(t), 'glyphs;', len(tokens(True)), 'without pictograms;', len(c), 'types')
    print(c.most_common(15))
