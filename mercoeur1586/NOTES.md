# Anonymous ("MR") to the duc de Mercœur, 26 June [c. 1586] (BnF fr. 15564 f. 151)

Catalogue item 13. Session 2026-09-21.

Status: attempted, closed unread. The cipher is not read; the clear frame is transcribed below.

## Result

**Attempted and closed from the evidence; the ciphered passages are not read.**

- Lasry's 2022 key for the Guise→Mercœur letters in this volume (ff. 27, 78, 119, 142; cryptiana `GL.htm`,
  image `GL_BnFfr15564.png`) is a different system. It uses cursive letter-forms plus Roman-numeral nomenclator
  groups. f. 151 uses Greek letters (β θ δ ε μ λ η φ σ), □ and △, digits (3 4 5 6 7 8 9) and Latin letters. No sign
  set is shared. Tomokiyo reports (`unsolved.htm`, "Letters from Duke of Guise?") that Lasry himself found f. 151,
  said it "does not decipher with the same key and is probably too short for cryptanalysis".
- Checked against the other 1586 League-circle keys in this repository: Mayenne–Forget Cipher-1
  (`matignon1586/key.json`, `key143_a.png`) and the Clairambault 357 two-digit figure cipher (`clair357`). Neither
  matches.
- Ciphertext-only: 217 signs in six runs, 55 sign types (`cipher.txt`, my transcription). A homophonic
  simulated-annealing run (`anneal.py`, 4-gram French model of the Henri IV letters, `matignon1586/lm.pkl`, 8 restarts)
  gave −1.87 per sign on the real text and −1.82 on a shuffled control. That is no signal: the text is below the
  unicity distance for a homophonic system of this size, even before counting nomenclator groups.

What would move it: another letter in the same key (the "MR" correspondent's other letters to Mercœur, in
fr. 15564–15566 or in Mercœur's papers), or the key itself.

## Source

- Gallica fr. 15564 = `ark:/12148/btv1b9064027v`. **f. 151 is the slip on the right of view 164** (8935 × 6606;
  the slip is at about x 4880–8500, y 3080–4100). The folio number "151" is at the top right of the slip, with an older
  number "226" at the bottom right. The address leaf "A Monseigneur / Monseigneur le Duc de Mercœur" is on view 165
  left, but it belongs to the f. 152 letter ("Moy cousin").
- Images in `img/` (git-ignored). Re-fetch: `https://gallica.bnf.fr/iiif/ark:/12148/btv1b9064027v/f164/{x},{y},1850,380/full/0/native.jpg`.

## The clear frame (my reading)

> Tout a esté [C1] que je vous ay adverty par ma derniere du ..e de ce mois. Et voy bien que [C2]. Toutes choses y
> estans disposées et preparées ainsi que j'estime que vous aurez esté adverty [C3] assister … sans v[ost]re
> presence, afin que nous eussions cest heur que desirons (?) tout plus tost … Je regrette infiniment n[ost]re malheur
> si [C4] ⓝ Je ne faillray de vous tenir adverty de [C5] … Test rey (?) duquel nous nous pensé … Mais nous avons
> depuis estimé qu'il viendra plus a propos d'attendre encores un peu … le tout ensemble [C6] mais esperons
> beaucoup par sa valeur. Ce xxvj^e juin.
> [monogram] MR

The writer uses "nous" and writes as a party close to Mercœur, planning an action that is waiting on Mercœur's
presence. The monogram "MR" is not identified. The year (c. 1586) is the catalogue's; the slip itself has no year.

## System

Homophonic substitution with nomenclator signs, written as unseparated signs inside a clear letter. The most
frequent signs are y ×16, σ ("so") ×12, 4 ×10, 9 ×10, † ×9 (`python docs/_check_profile.py --measure cipher.txt`).
