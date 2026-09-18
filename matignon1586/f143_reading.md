# fr. 15572 f. 143 (Mayenne to Henri III), the cipher block

> **Correction (18 Sept): f. 143 is not 21 lines of cipher.** The verso, f. 143v (canvas 151 left), is
> a **second full page of cipher, about 33 lines**, ending in three lines of clear and the close. The
> 21 lines treated below as "the cipher block" are the **recto only**. Every "about two thirds read"
> said of f. 143 in this repository refers to the recto: of the whole leaf's ~54 cipher lines, roughly
> **a quarter** is read. f. 143v has not been transcribed at all.

Canvas 150 right page of ark `btv1b9061879d`. The leaf opens in clear — Marmande, Sainte-Bazeille,
Castets, the march of the army and the capitulation — and the last 21 lines are in
Mayenne–Forget's Cipher-1, with no decipherment on the leaf.

`cipher_f143.txt` holds the glyph transcription, one line per manuscript line, in the token
alphabet of `key.json`. `reading_f143.txt` is the decoder's output. What follows is the reading,
with `…` where the transcription is still too uncertain to stand.

## Read

> **[lines 1–7]** … m'estant laissé entendre [49] il se vouloit départir du **[roi de Navarre]**,
> duquel je scai qu'il est très malcontant; et ayant considéré que je l'ay tousjours ou y tenir
> pour le meilleur, comme de [49] commandement qu'il ayt, et que ce ne seroit [une] petite faveur
> pour ses affaires que de … [t]raicté avec luy, et en considération d'une …

> **[lines 9–13]** … pour … il m'a promis de vous … faire pendant ce temps; et … où, à la vérité,
> il s'est résolu … à tout ce que … sçavons voulu … la composition de sa place, laquelle estoit
> encore …

> **[lines 14–19]** … pour nous retenir … ce que … encore … [i]l eust importé … de séjour qui nous
> est très … parce qu'il m'eust fallu passer … empê[cher] … me passer … pour ce … pour tous …

> **[lines 20–21]** … premier … ay verbalement … ne promeu de …

Tomokiyo's published fragment of this page is
"s'estant laisse entendre 49 il se voulloit de partir du 76 duquel je scai quil est tres
malcontant et ayant considere que je lai tousjours ou y tenir pour le meilleur …", so the reading
above reproduces his opening and runs about three times as far, besides the later stretches.

## Confidence

Lines 1–7, 9–14 and 17 are read; the rest give clauses but not continuous text. Two passes at
five tiles a line were needed; lines 8, 14–15 and 19–21 carry glyph errors and are given only
where the French is unambiguous. Line 7 closed on a second pass at five tiles per line, which
also settled two more confusable pairs: the two long-s figures (one **c**, one **u**) and the two
double-stroke figures (one **n**, one **o**) — *consideration* forces the second of each. The residue is a transcription problem, not a cryptanalytic one:
the key resolves every glyph whose shape is correctly identified, and the confusable set
(three "6"-like shapes for **i**, **n** and **s**; two round shapes for **a** and **m**; the
**e** family) is exactly where the errors fall.

## Code groups

`12` il · `13` qui · `14` que · `17` car · `25` nous · `26` vous/leur · `35` parce que ·
`47` tous · `49` **unidentified, occurs four times on this page** · `76` le roi de Navarre.


## A visual key for this hand (18 Sept)

`key143_a.png` / `key143_b.png`: every letter's figures as actually drawn by f. 143's secretary, cut
from forced alignments of lines 1–5 with the code groups pinned by eye. Most rows are clean,
consistent families — *a* ơ/Δ, *n* ·v·, *r* £, *t* Ƶe/m, *o* 7, *p* c, *s* Ɗ/∂, and the codes 13, 14,
47, 49, 76 — and are the reference for transcribing the rest of the leaf by eye. Two rows (*m*, *i*)
visibly contain mislabels and are not to be trusted until cleaned.

Comparison of the two readers on this leaf, all 21 lines: the **token transcription + key + language
model** reads about two thirds; the **image pipeline with f. 143's own figure set** reads fragments
(*ne seroit*, *mal con tant et ayant*, *tenir pour le me[il]leur*). Transcription by eye against the
visual key is therefore the way to finish this leaf; the image set's job is to supply that key.

Lines 14–15 re-transcribed against it give *"a[s]ses bo[n]e pour nous reten[ir]…"* — close to what
the earlier pass had, which says the residue on the weak lines is not naming inconsistency alone.


## f. 144 checked as a possible clear copy — it is not

f. 144r (canvas 151 right) is a clear letter in a heavily corrected hand, beginning *"Sire, Combien
que Vostre Majesté…"*, and running onto f. 144v with its own signature. The opening does not repeat
f. 143's (*"Sire, j'ay mandé…"*), so it is a separate letter — a draft or minute from another hand —
and not a decipherment of f. 143.
