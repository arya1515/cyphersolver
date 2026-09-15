"""Transcription of the Debosnys 'monographe verse' (c4a.png lines 1-15, c4b.png lines 16-20).

Made 15 Sept 2026 from 4x half-line crops (glyphs/L??a.png, L??b.png). One token per glyph, read left to
right; punctuation as its own token (',', '.', '-'). A trailing '?' marks an uncertain identity. Line 12
lies under a water stain and is the least reliable.

Code key (descriptive; composites are written as parts joined by _):
  X        plain X                        XD      X with a dot or tick above
  XS2      X crossed by a double slash    XBAR    x with a bar above
  CX       handwritten cursive x          HX      'ℑ'-like curly glyph      BX  bold curly x ending in a ball
  SL(a,b)  slash with mark a at upper left and b at lower right (o circle, d dot, x cross, t tick,
           p plus, y y-hook, 22 the '22' hook)            BSL(a,b) the mirror image (backslash)
  N_*      tilde (Sektu's 'N') above the part named: N_O, N_OO, N_X, N_OX, N_W, N_SLO, N_SL2, N_COLON, N_DASH_X
  EQ_*     two bars above the part: EQ_O, EQ_X, EQ_CUP     EQ3_O three bars above o
  II_BAR_O two ticks, bar, o      ARCH_BAR_O arch, bar, o   ARCH_EQ arch over two bars   ARCH_EQ_X arch, bars, x
  CC_EQ    'cc' over two bars     CC_BAR_O cc, bar, o       CC_EQ_OO cc, bars, oo
  BARS_II  two bars over two ticks   BARS_O bar, o, bar     TICKS_BAR ticks above and below a bar
  U_EQ     cup over two bars      CUP_III cup with three ticks inside
  VENUS    ♀     ODOWN o over a down arrow    OX o with small cross at upper right (♂-like)
  OPLUS    o with a cross standing on top     MARS_II o with arrow at upper right and two ticks below
  UPARROW  up arrow standing on a filled dot  O_HOOK o with a hook rising from it   HOOK_O hook/§ over o
  O_STEM   o on a short stem      O_EQ_HOOK o, bar, hook   TARGET_J dotted o with a J-hook below
  T_O_II   cross over o with two ticks below  CARET_O ^ over o   PLUS_O + at upper left of o   Q o with tail
  DELTA Δ  DELTA_RING Δ with a ring on top  DELTA_BAR Δ underlined   SIGMA Σ   OMEGA Ω   THETA θ (long bar)
  ALPHA 'ɑ' fish-loop  GAM 'ɣ/ϑ' curl   Y  thin Y   YB bold Y on a base   UPS ϒ   V   V_RING V with ring
  VCURL 'ʋ' with a dot   DSMALL 'δ'   DCURL curled D   D_COLON d over two dots   Z3 '3' with underline
  TCURL lying S-curl with loops ('≈ᔕ')   LOOP 'ᘐ' loop   DBLWAVE '≋'   DBLWAVE_XX ≋ over xx   MTAIL 'ɱ'
  HEART dotted heart/ram's-horn   CHECK_DOT '√' with a dot   CRES_E crescent enclosing E   GATE ⊓ with slash
  NOTE ♪   TAURUS ♉   LEO ♌   STAR ✱   HASH #   GRID ⊞   OSLASH ∅ (long slash)   PM ±   EIGHT 8
  QBAR '?' over a bar   CHEV_O '≪o'   CHEV_DASH '≪-'   CHEV_O_CHEV '≪o≫'   O_SL2_EQ ring over // over =
  Pictograms: PIC_SUN PIC_FISH PIC_HOUSE PIC_ARROW PIC_LEAF PIC_ANCHOR
"""

VERSE = [
    "DELTA_RING SL(o,o) GAM SL(t,d) N_O XS2 Y VENUS . SL(p,x) N_O? X TCURL ,",
    "HEART YB? BARS_II OSLASH CX NOTE DSMALL , VENUS XD N_O? SL(o,o) GAM TCURL",
    "DBLWAVE SL(p,d) HX XD XD CARET_RING PM ALPHA N_O STAR ODOWN XD -",
    "PIC_SUN OX ODOWN SL(o,d) XD N_OO BARS_II CC_BAR_O XS2 GAM ALPHA N_X XD -",
    "OMEGA SL(o,d) DELTA_BAR XD THETA CC_EQ VENUS TAURUS SL(t,d) TCURL CHEV_O X N_OX SL(y,o) ,",
    "V_RING EQ_O SL(t,d) TCURL II_BAR_O ARCH_BAR_O XD N_OO N_X ALPHA SL(o,x) UPS , SL(t,d) SL(y,o) .",
    "PLUS_O EQ_X CHEV_DASH DELTA_RING UPARROW XD XD VENUS MARS_II SL(o,o) CX THETA EQ3_O ,",
    "SL(o,o) BARS_O CHECK_DOT ODOWN SL(o,x) XD N_SL2 V VCURL OSLASH TCURL SL(t,d) EQ3_O ,",
    "SL(22,) OPLUS O_EQ_HOOK ALPHA XD BSL(o,o) TCURL PM XS2 UPS EQ_X BSL(x,x) N_O VENUS ,",
    "DBLWAVE_XX Y ODOWN . TAURUS NOTE DSMALL PIC_ARROW LEO N_O X N_X CC_EQ VENUS .",
    "XS2 O_STEM DSMALL SL(d,o) PIC_FISH XD CRES_E OX VENUS , XD ALPHA PIC_HOUSE SL(d,o) N_COLON XD XD DSMALL DELTA ,",
    "ARCH_EQ II_BAR_O OSLASH ODOWN XS2? CX? DBLWAVE ALPHA? SL(o,x)? LEO? PIC_? ? N_O SL(t,d) Q DELTA .",
    "PIC_LEAF Q D_COLON SL(d,d)? N_OX ARCH_EQ X TCURL V . N_X GAM O_SL2_EQ SIGMA QBAR QBAR XD OX",
    "PIC_ANCHOR XS2 O_EQ_HOOK HX ALPHA? GRID BX Y EQ_CUP SL(o,o) TCURL XD VENUS EQ_X II_EQ N_W OPLUS",
    "Z3 OPLUS VENUS XD XD DELTA_RING EQ_X N_SLO U_EQ GAM SIGMA VCURL DCURL DSMALL MARS_II",
    "CHEV_DASH HEART XD STAR HASH , UPARROW N_DASH_X CUP_III Y , DSMALL MARS_II",
    "DELTA TICKS_BAR O_HOOK CC_EQ_OO N_OX XD EQ_O SL(t,d) YB SL2_BAR_O HOOK_O CX CX SL(o,o) TCURL",
    "LOOP ARCH_EQ_X STAR CHEV_O_CHEV N_OX N_COLON NOTE ARCH_EQ CARET_O SL(t,d) TCURL .",
    "DELTA_RING SIGMA ARCH_BAR_O XD VENUS T_O_II OX . CHEV_O Y II_BAR_O N_OO THETA BX",
    "TARGET_J XD XD Q VCURL MTAIL Z3 Y TAURUS OMEGA HX GATE EIGHT XBAR BX",
]

PUNCT = {',', '.', '-'}


def lines(strip_punct=True, strip_q=True):
    out = []
    for l in VERSE:
        t = l.split()
        if strip_punct: t = [x for x in t if x not in PUNCT]
        if strip_q: t = [x.rstrip('?') or '?' for x in t]
        out.append(t)
    return out


if __name__ == '__main__':
    import collections
    L = lines()
    toks = [t for l in L for t in l]
    c = collections.Counter(toks)
    print('%d glyph tokens, %d types, %d hapax' % (len(toks), len(c), sum(1 for v in c.values() if v == 1)))
    print('per line:', [len(l) for l in L])
    print('final glyphs:', [l[-1] for l in L])
    for k, v in c.most_common(30): print('  %-12s %d' % (k, v))
