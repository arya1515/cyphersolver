# Catherine de Médicis to Philibert du Croc, Saint-Maur, 27 April 1567 (Destray 1924, plate after p. 56; Gallica bpt6k932364m f61) — NOTES

**Status: transcribed, attempted, not solved.** Session 2026-09-16, opened as candidate 2 of the short list in TARGETS.md.

## Source
Paul Destray, *Un diplomate français du XVIe siècle: Philibert du Croc* (1924), prints the letter (p. 53) and a facsimile
plate (leaf after p. 56). The original is in the Archives départementales de la Nièvre (Cipherbrain comment, Pascal,
29 May 2021). Gallica's IIIF route fetches the plate at 3328 × 4796 px with a browser User-Agent
(`https://gallica.bnf.fr/iiif/ark:/12148/bpt6k932364m/f61/full/full/0/native.jpg`). Schmeh posted it on Cipherbrain on
19 May 2021 ("Die verschlüsselten Briefe von Katharina und Maria von Medici"); the thread identified the recipient and
the printed source and proposed no reading. Tomokiyo lists it as unsolved and notes the clear lead-in *"jay recu du
sr x3 lettres en datte"*, so the cipher may open with a date.

## The clear frame
"Mons. du Croc. Ceste l[ett]re ne sera que pour vous advertir que jay eu de ma part grant plaisir dentendre que les
affaires de la Royne descosse ma belle fille sont de mieulx en mieulx et les choses a passer aussy plus asseurees de
tranquillite, ce quil fault esperer de ces [?] … je seray bien ayse d'avoir de ses nouvelles, et que vous faciez auprès
d'elle tous les bons offices que vous pourrez au bien de ses affaires … Jay receu du sr x3 lettres en datte [CIPHER]
… priant dieu Monsr du Croc vous avoir en sa ste garde. Escript a St Maur ce xxvije jour d'avril 1567." Signed Caterine,
countersigned de L'Aubespine.

## Transcription ([ct.txt](ct.txt))
Six lines, **147 tokens, 40 distinct symbols**; Latin letters (a d q p o g n x e c m b v h r f) mixed with a few
digits (6, 7) and graphic signs (double cross `#`, crossed `Hp`, `2B`, slashed o `ø`, `ð`, hooked `G`, `y/ȥ`, `ff`, `L`,
`≠`, barred `x`, triple cross). Dots occur eleven times and are too sparse to be word separators; they may mark
phrases or be nulls. Small vertical ticks (`|`, four times) may be letters (i or l) or marks. Commonest: `#` ×13, `p` ×9,
`g` ×8, `G` `o` `B` `y` ×7. The reading of several glyphs is uncertain; line crops are in the scratch files, not committed.

## Attempt
- French 5-gram model built from La Ferrière's *Lettres de Catherine de Médicis* i–iv, Teulet's *Relations politiques*
  ii and Labanoff vii (9.4 M characters, v→u, j→i, Roman numerals and OCR junk stripped), with and without spaces
  ([lm.py](lm.py)).
- Homophonic annealer with frequency initialisation ([solve.py](solve.py)). **Matched control fails**: a 147-letter
  passage of du Croc's own 1567 despatch, enciphered with a 40-symbol homophonic key drawn to the target's frequency
  profile, is recovered at 28–41 % over six seeds ([control.txt](control.txt)). So a ciphertext-only attack at this
  length is below the solver's threshold and was not run on the target as a result-bearing step.
- Lasry's key for the Charles IX → du Croc letter in the same book (cryptiana GL.htm, 25 May 2022) uses a different
  symbol set (Greek letters, digits, curls, with word codes for De, Et, Que, Par, Pour, Je, Vous, la Royne d'Angleterre,
  la Royne d'Escosse, Royaulme); it is not this cipher, though `#`, `ø`, `‡` appear in both.

## What would move it
Cribs. Catherine acknowledges letters from "le sr x3" with dates, so the cipher likely opens "du … et … de ce moys"
or names the writer's despatches; du Croc's own letters of March–April 1567 (Teulet ii pp. 294–297; Labanoff vii
pp. 110 ff., not printed for April) and Catherine's other letters of the month (La Ferrière iii; the 27 April letter
itself is not in the edition) would supply the vocabulary. Word segmentation is the other lever: if the dots and the
ticks are separators the problem becomes the Forster kind, which solved at 207 tokens. Until then: not solved, and
not claimed.

Checked: image fetched and transcribed; 147/40 counts; control failure. Not checked: glyph identities against a second
reader; whether the Nièvre archive holds a decipherment. User must verify: the transcription before any reading built
on it is trusted.
