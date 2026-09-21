# Cardinal Barberini to Nuncio Ceva, Paris, 1632–34

ASV, i. 1025, Segretario di Stato, Francia, doss. 346.
DECODE R74–R84 (eleven ciphertexts); the catalogue entry named five of them:
R75, R77, R78, R82, R84.

Status: read in part.

## What the catalogue expected, and what was actually there

The entry read this as a transcription job: DECODE says "Deciphered in original",
so the text was taken to have been read at the time and the work to be copying a
decipherment off the leaf.

That is only half right, and the other half changes the job:

* **George Lasry reconstructed the key of this dossier on 24 Oct 2020** and it is
  attached to every one of the eleven records (`DOC_R*_D32*.txt`, `#KEY:
  reconstructed`). So the system was already solved before this session.
* He also published aligned decipherments of **four** letters — 346:1 (R74),
  346/4 (R77), 346/5 (R78) and 346/9 (R82) — in a combined file replicated across
  the records (`DOC_R*_D322*.txt`, 29 050 bytes, identical everywhere).
* **Three of the five catalogue targets (R77, R78, R82) are therefore already
  read.** Two are not: **R75 (346-2, 25 Sept 1632, 3 128 digits)** and **R84
  (346-11, 18 Dec 1632, 2 110 digits)**. Those two carry only a raw ciphertext
  transcription and no decipherment.
* Lasry left **all 95 nomenclator elements unsolved**; every one is printed
  `<xxx>` in his readings.

So the work here is: read R75 and R84, and resolve what can be resolved of the
nomenclator.

## The system

Reconstructed by Lasry; re-derived and checked here against his four aligned
readings (`extract_gold.py` → `gold.json`, 104 line pairs, 179 distinct tokens).

| | |
|---|---|
| `6` | word separator |
| `2x` | null — no pair beginning 2 carries plaintext |
| `XY` | homophone or syllable, 61 codes (`cipher.py`) |
| `pXY` | nomenclator element: one prefix digit + a 2-digit code |

Three points that matter for decoding and that the DECODE key note gets only
partly right:

1. **`6` never occurs inside any code** — not in a key pair, not in any of the 95
   nomenclator elements. Word boundaries are therefore certain; only the
   two-versus-three-digit choice is not.
2. The note says nomenclator elements "have 4 digits starting with prefix 4".
   They are in fact **three** digits: the concatenated token stream of 346:1 is
   99.7% identical to the original transcription, with no dropped prefix. The
   prefix is 4 in 27 of the 95 elements but is also 0, 1, 3, 5, 7, 8 or 9.
3. The digit after the prefix is itself a valid key code in 91 of 95 elements, so
   the element is a prefix plus an ordinary code — which is why the parse is
   ambiguous and needed a language model.

29 of the 100 pairs are dead (`02 05 06 12 16 32 33 36 42 46 52 56 60–69 72 76 82
86 92 96 99`); meeting one forces a three-digit reading.

## Method

`decode.py` — a position-indexed beam search over the digit stream. Every `6` is
consumed as a separator; elsewhere the beam chooses between a 2-digit code, a
2-digit null and a 3-digit nomenclator element, scored by a character model.
Scoring is incremental: `lang`'s DenseLM is a flat table of log P(c | previous
order−1 chars), so each emitted character costs one lookup.

`indomain.py` — `it-cinquecento` stops around 1620 and knows nothing of this
clerk's spelling (v for u, doubled letters dropped). It is interpolated (w = 0.6)
with a model built on 7 693 characters from the dossier itself: the passages the
clerk wrote in clear, plus Lasry's plaintext of the letters not being tested.

## Calibration

`eval.py`, leave-one-document-out — the nomenclator inventory offered for a
document is built from the other three only, which is the situation of R75 and
R84. Token-level agreement with Lasry's own segmentation:

| model | tokens | nomenclator recall | precision |
|---|---|---|---|
| `it-cinquecento` alone | 0.945 | 0.52 | 0.70 |
| interpolated, w = 0.6 | **0.958** | **0.70** | **0.79** |

Per letter at w = 0.6: 346:1 0.871, 346/4 0.928, 346/5 0.905, 346/9 0.951.

The figure to keep in view is the nomenclator recall. About three in ten elements
are still missed, and a missed element is not rendered as a gap — it is rendered
as two or three plausible Italian letters. Wrong readings in the text below will
be concentrated at those points.

## Control: the 1632 decipherment on the leaf

R75 carries a contemporary interlinear decipherment, and the DECODE transcriber
copied what was legible of it above each cipher line. It was used for nothing —
not the key, not the model, not the decoder — so it is an independent witness.

`control.py`, on the 24 lines where enough of the interlinear was legible:
**1 105 letters, 77.5% agreement**, ignoring word division. The last line agrees
at 100%. The residue is shared between this reading and the witness's own
illegibility: the transcriber flagged much of it `?` and `*`.

## Nomenclator elements resolved here

Aligning the reading of R75 against the interlinear shows which word of the 1632
decipherment stands where the decoder placed an element (`resolve.py`). Twenty-two
elements caught a witness fragment; six survive checking against Lasry's four
letters, where they were not fitted:

| code | reading | evidence |
|---|---|---|
| `474` | **mente** | `piena~`, `principal~`, `non sola~ per il solo proprio`, `malacomoda~`; witness fragment `met` |
| `495` | **quanto** | `e ~ al proporre arbitrare`; pairs with 498 |
| `498` | **tanto** | `che ~ in <347> quanto in <857> si sappia la cagione` |
| `830` | **Francia** | 4/4 in Lasry's letters after a feminine article: `render la ~ piu poderosa`, `valere a danno quella ~`, `hoggi la ~ in a di dar legge` |
| `854` | **guerra** | R75 interlinear, twice (`gurra`, `urrap`) |
| `149` | **piazza** | R75 interlinear, `acquisto d'una ~` |

Adding the six raised the control agreement from 0.737 to 0.775. That test is
partly circular for `854` and `149`, which came from the witness itself; the
independent evidence for `474`, `495`, `498` and `830` is their fit in the four
letters Lasry read.

`491` drew the witness fragment `goto` — "pensieri di goto natione", i.e. Sweden —
but it does not fit its four contexts in Lasry's letters, where it stands before
`unione` and after `conferito con`. Left open.

## The two letters

Rendering conventions: the cipher writes one sign for u and v (printed `v`), the
clerk drops doubled letters, and word division is his, not modern. Gaps are
unresolved nomenclator elements or transcription noise.

### R75 — 346-2, "Di Roma li 25 di Settembre 1632", 2 pp., 3 128 digits

Barberini on the consequences of the Swedish victories for the French alliance.
The argument: the victories make *l'accomodamento* easier but *l'unione* far
harder; the nuncio is to make the French court see the danger to itself.

> …le vittorie di […] e quella forza renderanno per avventura più facile […]
> quell'accomodamento, di […] ma più difficile assai […] quell'unione …
> per […] interessi **di Francia** …
> è tempo che se cominci a conoscere **quanto** sia pericolosa **alla Francia** la
> potenza d[i …] che cominciano [hor]mai a pensar a cose [grandi] et ad indrizar
> la [mira] loro a […]; consideri **quanto** sia oportuno alli vastissimi
> pens[ieri] di […] natione estendere il loro dominio sino al Mediterraneo con
> acquisto d'una **piazza**, e con **quanto** buon fonda**mente** lo possono
> sperare in una [rivoluzione] … **di Francia** … hanno **tanto** forze marittime
> e terrestri; consideri … che la vittoria […] è altret**anto** formidabile **alla
> Francia quanto** alla […] …
> [non si] sarà sempre al medesimo, darà sempre orecchie a[l] torbidi, et haverà
> chi li suggerisca; et un successor[e] … restringer in maniera che sempre non
> habbi libertà di [salvarsi] in campagna … [bisogna] cercar di compor[re gli]
> esterni, che cagioneranno e fo[men]teranno li domestici …
> [è] gia … arrivata a tal … di gloria … che può con ragion temere che la […]
> fortuna non si rivolti; cerchi dunque d'augumentarla con l'arti … pur vuol
> seguitar … indrizi le cose per intraprender **guerra** contro …
> quel[li] che sola parte manca alla gloria di […]. In somma … le congiunture
> presenti sono più contrarie alla s[ua] … quell'unione, **tanto** più deve …
> pensar a ritrovar ragioni che la persuadano.

### R84 — 346-11, "Roma li 18 di Xbre 1632", 2 pp., 2 110 digits

Written a month after Lützen (16 Nov 1632), and the whole page turns on "quella
vittoria". The first folio is largely in clear — Barberini acknowledging Ceva's
despatch of the 8th and referring him to Mons. Bichi at court — and the cipher
carries the analysis.

> ricordando a […] che si […] quella vittoria contro […] con la sua consueta
> **prudenza**, ad indur[re] … a facilitar il […] …
> […] che bollivano **in Francia** dopo la mia partenza; pure de[…] li torbidi di
> […] furono cagione che li […] concludessero la […] …
> le gelosie [che] quella potenza **di Francia** cerca di […]; e li spiriti
> inquieti […] fanno pastura su li impegni che il […] tiene con […] potenti, e si
> muovono più facil**mente** con speranza di fo[men]**mente** e diversione.
> Per stabilire et assicurar le cose […] bisogna levarsi le inimicitie esterne …
> nascerà l'alt[r]o in mano **di Francia**. Posso dire che stia […] se vo[gliono]
> ridur a termini ragionevoli le pretensioni …
> non […] entrar in […] cose, non lascierà di andar [f]acilitando le v[…] maniera
> che a lei s[i] accenna …
> la fuga di […] non so **quanto** sia a proposito con ins[o]liti rigori … **[in]
> Francia** metter in disperatione … potendo da[…] conseguenze che tengano
> disunita per un lungo pezzo **la Francia**, e sotto giogo alle esterne violenze,
> o almeno impotente a soccorrer li suoi alleati.

That last clause is the point of the despatch, and it is new: the Roman reading
of Lützen is that the danger is now a France held disunited and unable to help
her allies.

## What is open

* **The nomenclator.** 89 of the 95 elements Lasry met remain unread, plus 28 more
  that appear only in R75 and R84 (21 and 7). The people and places of both
  letters are inside them. A key for this dossier, if one survives in the ASV,
  would close it at a stroke.
* **The transcriptions are DECODE's, not re-checked against the images.** R75's
  transcriber flagged doubtful digits throughout. Several stretches that read
  badly here (`quzper cavsevc`, `l v osts sevom`) are more likely transcription
  than decipherment. The images are R75 I589/I590 and R84 I639/I640.
* **R74, R76, R79, R80, R81, R83** — the other six of the eleven — were read by
  Lasry and are not touched here.

## Files

| | |
|---|---|
| `decode/` | the DECODE transcriptions, key and combined decipherment |
| `cipher.py` | key, nulls, separator, the six elements read here |
| `extract_gold.py` → `gold.json` | Lasry's aligned readings, parsed |
| `streams.py` → `r75.digits`, `r84.digits` | ciphertext digit streams |
| `decode.py` | the beam-search decoder |
| `indomain.py` | the interpolated character model |
| `eval.py` | leave-one-out calibration |
| `control.py` | check against the 1632 interlinear |
| `resolve.py` | nomenclator proposals from the interlinear |
| `run.py` → `r75.read.txt`, `r84.read.txt` | the readings |

## Remaining gaps

- 117 nomenclator elements of R75/R84 (89 of Lasry's 95 plus 28 new) - blocker: open-codes; people and places sit inside them; interlinear on R75 fixed 6; 491 contradicts its contexts
- R75/R84 doubtful stretches - blocker: not-attempted; transcriptions are DECODE's and were not re-checked against images R75 I589/I590, R84 I639/I640
- dossier key with nomenclator - blocker: needs-physical-access; none on DECODE; would need the ASV

## Escalation

- [x] siblings: all eleven records R74-R84 opened; Lasry key and four readings on them
- [x] clear-pages: R75 interlinear 1632 decipherment used as control and to resolve 6 elements
- [ ] known-keys: not done - other Barberini-period ASV nunciature keys on DECODE (e.g. Pallotto 1629 R215, Paris nunciature) not tried for the nomenclator
- [ ] print: not done - Nuntiaturberichte / Acta Nuntiaturae Gallicae for Ceva 1632-34 not searched
- [x] key-rebuild: LM beam decoder, interpolated in-domain model; alphabetical proposals (nomen_proposals.json)
- [ ] retry: not done - re-check the transcriptions against the images and rerun with the six new elements
