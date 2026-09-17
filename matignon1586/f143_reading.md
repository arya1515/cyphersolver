# fr. 15572 f. 143 (Mayenne to Henri III), the cipher block

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
> pour ses affaires que de … traicté avec luy, et en considé[ration] …

> **[lines 10–13]** … le et service; il m'a promis de vous … faire pendant ce temps … ou à la
> vérité il s'est résolu … à tout ce qu'en … la composition de sa place, laquelle estoit encore …

> **[lines 16–19]** … eust importé … de séjour qui nous est très … parce qu'il m'eust fallu passer
> … mon cousin … passer … couru en ennemi …

> **[lines 20–21]** … premier … ay verbalement … ne promeu de …

Tomokiyo's published fragment of this page is
"s'estant laisse entendre 49 il se voulloit de partir du 76 duquel je scai quil est tres
malcontant et ayant considere que je lai tousjours ou y tenir pour le meilleur …", so the reading
above reproduces his opening and runs about three times as far, besides the later stretches.

## Confidence

Lines 1–7 and 10–13 are read; lines 8–9, 14–15 and 19–21 carry glyph errors and are given only
where the French is unambiguous. The residue is a transcription problem, not a cryptanalytic one:
the key resolves every glyph whose shape is correctly identified, and the confusable set
(three "6"-like shapes for **i**, **n** and **s**; two round shapes for **a** and **m**; the
**e** family) is exactly where the errors fall.

## Code groups

`12` il · `13` qui · `14` que · `17` car · `25` nous · `26` vous/leur · `35` parce que ·
`47` tous · `49` **unidentified, occurs four times on this page** · `76` le roi de Navarre.
