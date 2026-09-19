# Carpio (Rome) to Fuenmayor (Copenhagen), 1677 — DECODE R1002–R1011

Status: read

Ten ciphered despatches of Gaspar Méndez de Haro, 7th Marqués del Carpio, Spanish ambassador in Rome, to Baltasar de
Fuenmayor, Spanish envoy in Denmark, 4 Sept – 11 Dec 1677. Archives générales du Royaume, Brussels, Secrétairerie
d'État et de Guerre, inv. nr. 2559. Images and DECODE's ciphertext transcriptions: DECODE R1002–R1011, fetched
19 Sept 2026 with the cookie in `bordeaux/decode/cookie.txt` (images in `img/`, git-ignored).

**Result.** The key was reconstructed from the letters themselves and reads all ten. DECODE lists R1004 (13 Nov) and
R1005 (20 Nov) as "non-decrypted". Both read in full with the key. Both leaves also carry a faint contemporary
decipherment in the left margin that DECODE's transcriber missed, and the key reading agrees with it. The other eight
letters have the decipherment written in the margin. The key reproduces each one, so the margins can be checked and
their illegible words recovered.

## The key

This is a syllabic nomenclator. Every token is separated by a point. There are four kinds of token:

1. **Plain numbers 9–30: single letters.**
   a 9, b 10, c 11, d 12, e 13, f 14, g 15, h 16, i 17, l 18, m 19, n 20, o 21, p 22, q 23, r 24, s 25, t 26, u 27,
   x 28, y 29, z 30.
   In practice these mostly spell closing consonants: n 20, r 24 and s 25 are the three commonest tokens.
2. **Plain numbers 31–60: consonant + vowel syllables, in rows of five (a e i o u).**
   m 31–35, n 36–40, p 41–45, r 46–50, s 51–55, t 56–60.
   Examples: 33 mi, 36 na (also ña), 39 no, 41 pa, 44 po, 48 ri, 51 sa, 52 se.
3. **Struck-through numbers: a second syllable table** (DECODE marks the stroke with "+").
   - t row 15–19 (ta te ti to tu)
   - f row 20–24 (fa … fu)
   - vowel + l 30–34 (al el il ol ul)
   - vowel + s 35–39 (as es is os us)
   - vowel + n 40–44 (an en in on un)
   - vowel + r 45–49
   - que 50, qua 51, qui 52
   - 14 is a word not yet fixed. It comes before -s/-sta, as in "[14]sta mente" and "[14]ticia", so possibly "ju".

   Struck N, R, g and 4 are nulls. They sit mainly at the start and end of each cipher block.
4. **Letter pairs: syllables with the consonant disguised, vowel kept.** Cipher → plain:
   b→c, c→b/v, g→d, l→g, m→l, d→m.
   So ge = de, gi = di, go = do, ma = la, mo = lo, me = le, bo = co, bi = ci, ca = va/ba, ci = vi, la = ga, lu = gu,
   lo = go.
   Special cases: ag = ha, eg = he, e (a separate sign) = lle.
   116 = V.S. (Vuestra Señoría). 8 is used for o.
5. **Three-letter words (code names), read from context:**

   | code | meaning |
   |---|---|
   | sen | el Rey |
   | gin / jin / jen | S.M. / el Rey |
   | gus / mus | Príncipe (de Orange) |
   | quol | Inglaterra |
   | ana | Nápoles |
   | ten / den | Francia |
   | pon | armada |
   | san | Bruselas |
   | tan | Flandes (?) |
   | gon | señor(es) |
   | ran / xan | gobernador |
   | xon | guerra |
   | cun iles | españoles (?) |
   | lun | cart(as) |
   | men / Jen (R1010) | Reino |

   R1010's "gus de s ra n ge s" is Príncipe de Orange, spelled out.

Scripts: `parse.py` reads DECODE's transcription files and `dec.py <record>` prints a reading. The raw machine
readings are in `read/R*.raw.txt`. They inherit DECODE's transcription slips: a few misread numbers show up as
`{..}` or as nonsense syllables.

## The two letters DECODE lists as unread

**R1004, Rome, 13 Nov 1677** (normalised, reading confirmed by the faint marginal decipherment):

> … [y al mesmo tiempo devo] lamentarme con V.S. de lo que en todas partes nos persigue nuestra mala fortuna, pues
> con la llegada del Cardenal de Estrées a Turín se teme alguna gran novedad en Italia; y las cosas de [Flandes] se
> hallan en el estado que V.S. sabe. Si bien en las materias del Congreso parece debemos suspender el juicio hasta ver
> lo que resulte del abocamiento del Príncipe de Orange con el Rey de Inglaterra. En los embarazos de esta corte no se
> me ofrece qué añadir a lo que diré a V.S. en mis antecedentes, sino que, si bien aguardaba este correo las órdenes
> de S.M., no las he recibido; pero no dudo las traerá el siguiente, pues de Madrid me avisan que habían llegado allá
> las cartas en que di los primeros avisos sobre estas dependencias.

**R1005, Rome, 20 Nov 1677:**

> … más de que nos tienen con gran cuidado las apariencias y evidentes señales de que la próxima campaña habrá
> guerra en Milán, pues el Cardenal de Estrées, que está en Turín, no se descuida.

## What the ten letters say (in date order)

- **R1010, 4 Sept.** The French fleet (la armada de Francia) has left Messina. It was rumoured to be bound for
  Brindisi, but its design is Catania. Carpio is dismayed by news from Brussels that the Prince of Orange raised the
  siege of Charleroi "intempestivamente".
- **R1011, 18 Sept.** Rome's reaction to Charleroi. Anti-Spanish rumours are stirring the populace. Carpio has had no
  satisfaction from the Pope or his ministers. The militia of the district was called out, and guns were mounted
  ("encabalgado … más piezas") on Castel Sant'Angelo.
- **R1009, 25 Sept.** The false rumours spread against the Spaniards. Carpio pressed the Pope for remedy and got
  neither remedy nor an inquiry. He has referred the matter to the viceroy of Naples and the governor of Milan.
- **R1006, 2 Oct.** The offences to the Spanish nation continue. He has asked the governor of Milan and the cardinals
  of the Spanish party for advice. The French fleet and galleys kept station off Catania and then returned to Toulon,
  much battered.
- **R1007, 9 Oct.** Still no satisfaction. He stays away from papal audiences on the cardinals' advice, awaiting the
  viceroy of Naples' answer.
- **R1008, 16 Oct.** No news at this court. He stands firm and awaits orders on how to proceed.
- **R1004, 13 Nov** and **R1005, 20 Nov.** Above.
- **R1002, 4 Dec.** In the matter of the pending disputes he asked for an audience of Innocent XI on the King's
  orders. The Pope refused it twice and would receive business "del Rey" only through a cardinal. Carpio declines to
  treat the principal business until the point is settled.
- **R1003, 11 Dec.** The loss of Freiburg ("el sitio de Fri[bur]go", taken by Créqui on 16 Nov 1677): its
  consequences may force the imperial troops back over the Rhine. He also writes of the miserable state of [Flanders]. The Pope refused audience again. He is awaiting the Marqués de
  los Vélez (viceroy of Naples).

These are working summaries of the machine readings. A line-by-line edition of the eight margin-deciphered letters
would need each DECODE ciphertext transcription checked against the image.
