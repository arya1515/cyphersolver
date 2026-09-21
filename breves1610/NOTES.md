# Marie de Médicis → Savary de Brèves, Rome, 10 Nov 1610 (BnF fr. 3789) — catalogue item 25

Status: no write-up

**Result, 21 Sept 2026: attempted, not read.** The passage is found and transcribed, its sibling (15 Sept 1610) too,
and the key it most probably uses is located. The only copy of that key available here is not good enough to apply.

## The letters

Gallica btv1b9059628m. The BnF notice's folios run two ahead of the stamped foliation in the scan: its "no. 12,
fol. 21 et 23" is **stamped f. 19r–v (canvases 36–37)**, and its "no. 11, fol. 19" (15 Sept 1610) is stamped f. 17
(canvases 32–34). Stamped f. 21 is a Savoy letter, which misled the first look.

- **10 Nov 1610** (signed Marie, countersigned Brulart): about 45 signs on f. 19r, lines 5–7, in mid-sentence:
  "Aussi vois-je bien [cipher] ne se[roit] pressé jusques à l'extremité du desarmement pour recevoir enfin la honte
  d'un refus absolu…". The context is Savoy's disarmament after Henri IV's death and Spain's refusal. The digits
  on f. 19v are show-through, not more cipher.
- **15 Sept 1610**: two passages, about 70 signs, f. 17r lines 22–24, on Savoy's son's journey to Spain.
- Transcription: `ciphertext.txt`. On DECODE they are R2076 and R2075 (Tomokiyo, "not deciphered").

The deciphered Villeroy letter in the same volume (stamped f. 26, Dec 1605) has an interlinear decipherment, but its
code is a different one: "content" = y b q 29̈ gives y=c, b=o, q=n, and those values turn Marie's text into nonsense.

## The key

DECODE **R2077** (Henri IV → Brèves, 5 Jan 1610, fr. 3541 f. 4–7) is marked Decrypted. Tomokiyo (louisxiii.htm)
says that letter was broken ciphertext-only by **Lasry, with Biermann and Tomokiyo, in 2021**. Camille Desenclos then
found the key at the BnF: R2077's note says **"The key is in BNF Français 3642"**. The record's only document is a
photo of that key (`DOC_2077_2022-Jan-30-16-52-01_93064.png`, 833 × 587 px, saved in `decode/`, git-ignored). The
R2077 note itself says R2075/R2076 "may be in the same cipher".

What the photo shows: an alphabet of 2–5 homophones per letter, many of them Latin letters used as signs (a b c d
under M, e f g h under N). A t/u/x/y/z box with qq, ǂǂ and ʓ for t. Plain numbers 4–99 for persons and a–b words: 4 le
pape, 14 le roy d'Espagne, 34 le duc de Savoye, 36 les princes de Savoye, 41 le duc de Parme, 62 card. Borghese,
c. 71–72 le Sr don Jouan / le Sr Conchine, 78 avoir, 79 avec, 86 armes, 88 bien, 96 Cardinal, 98 car. Letters with a
comma for c–e words: a, ce · y, et · x, en · 3, de?. Overbarred numbers 4̄–46̄ run from Flandres to milanois. The
photo stops there, so M–Z words are missing.

Marie's text uses the same kinds of sign (qq, ǂǂ, code letters with commas, plain and barred numbers). The 10 Nov
passage opens "72 4 79" = [Conchine?] le pape avec. But the alphabet as I read it from the 833-px photo gives
gibberish: `beam.py` runs a beam search over each sign's candidate letters, scored with the fr-1600-letters model, and
reaches −95 on 16 letters. One of three things is wrong: my assignment of photo columns to plaintext letters, the key
itself (a related table), or both.

## What would move it

1. **Lasry's R2077 decryption** (ciphertext plus plaintext) would calibrate every sign. He is the paper's
   co-author; ask him.
2. A full-resolution image of **BnF fr. 3642** (not on Gallica, SRU search 0 hits), including the M–Z code page.

## Brèves's reply (checked 21 Sept 2026)

Brèves's Rome letter-book, BnF **Cinq cents de Colbert 351** (Gallica btv1b10033961z, copies 1608–1611), pp. 724–730
(canvases 365–368): **"A la Reyne Regente, du 9 Decembre 1610"**, opening "J'ay receu les commandemens de V.M. du 10
Novembre". It answers the letter point by point **in paraphrase, never in her words**. It covers the pope's praise of
the regency over Cleves-Jülich, the Cologne conference breaking up, the Milan armament, and the hope that the king of
Spain would disarm at the pope's request. The pope approves the regency telling its ambassador in Spain that France is
bound to protect the Duke of Savoy if attacked, and Brèves warned the pope that Spain aimed to master Italy. Savoy is
the ciphered passage's subject, and this is its likely gist. But nothing in the reply fixes its words, so it gives no
crib strong enough to recover signs.
(The next letter, 14 Dec 1610, answers one of 23/24 Nov, p. 731 and canvas 370.)

**Closed as unreadable from available sources:** the key photo is partial and too coarse, the reply does not quote,
and the passage is too short (40 + 60 signs) for a ciphertext-only attack on a homophonic nomenclator. Only item 1 or
item 2 above would reopen it.
