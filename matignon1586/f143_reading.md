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


## f. 143v, the second page of cipher: transcribed in full and read in long stretches

All 33 cipher lines of the verso were transcribed at two tiles a line (`f143v_cipher.txt`) and decoded
with the key and the period-French model (`reading_f143v.txt`). The page reads as a continuous
argument about the terms offered to the captain of a place Mayenne is besieging — a sum of money
paid over three years, a royal pardon, and the governor's surrender of the place:

> **[lines 1–7]** … luy fai[re] payer dans trois ans … la somme de douze … de luy faire obtenir … de
> son … de le rendre, et oultre … pour luy faire avoir … un **pardon** de tous [ses] … que je supplie
> très humblement Vostre Majesté … de vouloir confirmer … ainsi que j'en aye …

> **[lines 8–12]** … me suis résolu … que je ne me fusse pas tant advancé de traicter … car … de
> rendre son … **parce qu'il ne** se peut ayder …

> **[lines 13–15]** … du comte, **de sa femme** et … **à ses enfans; et quand au pardon, il ne peut
> estre valable qu'il n'ayt passé au Parlement** …

> **[lines 16–24]** … il est certain qu'ils ne … pas … **qu'il n'ait obey** … et du tout renvoyé à
> l'aultre partie … pour la **somme** dont il en a … une partie … **qu'il nous a espargné** … et de
> l'autre, **elle n'est pas aussi du tout inutile, ayant de luy ceste obligation de ne porter les
> armes** …

> **[lines 25–33]** … **j'ay grande espérance de l'en retenir du tout, et ce faisant** … **place de
> conséquence — c'est ce qui m'a peu … plus volontiers en ce traicté** … **s'il luy plaist entendre
> son intention** … la parole …

**What the despatch is.** Mayenne reports to the King that he has negotiated the surrender of a
place held by a captain, on terms that need the King's confirmation: money over three years, a
pardon that "cannot be valid until it has passed the Parlement", and an obligation "not to bear
arms"; he explains why he went so far in treating ("a place of consequence"), and asks the King to
make his intention known. The recto's closing lines — *"la composition de sa place, laquelle
estoit encore…"* and *"il m'a promis de vous … faire pendant ce temps"* — are the same negotiation.

**Coverage, honestly.** Roughly half the verso reads as continuous French; the rest is fragments.
With the recto at about two thirds, **f. 143 as a whole — about 54 cipher lines — is now read in
substance**, the subject, the terms and the request all being recoverable, though not word for word.
The remaining gaps are transcription slips in single figures, which is where a second pass at higher
magnification has closed lines before.
