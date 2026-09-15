# Intercepts by the Commonwealth (Thurloe State Papers, 1653-56) — cryptiana unsolved item #9

Four undeciphered pieces printed in Birch's *Thurloe State Papers* (1742), full text on British History Online.
Ciphertexts extracted to `a_*.txt` … `d_*.txt`; analysis in `analyze.py` (`analyze_out.txt`), key trials in
`apply_keys.py` (`apply_keys_out.txt`; keys harvested from cryptiana into `keys/`), solvers `solve_a*.py`
(outputs `solve_a2_*.txt`), LMs `lm_nl.json`, `lm_fr.json` (`lm_build.py`).

| | letter | size | type | verdict |
|---|---|---|---|---|
| a | Beverning & Vande Perre → Boreel (Paris), Westminster 1 Sept 1653 NS; TSP i.435 | 136 groups, 33 distinct: letters 6-33 (25 symbols), codes 113 117 211 222 327 329 519 527 | monoalphabetic letters + small nomenclator; plaintext Dutch (or French) | **stuck** |
| b | du Gard's "new direction" enclosed to White, Brussels 10 June 1656; TSP v.78 | 22 symbols incl. letters q t y m f | cover address; too short | stuck |
| c | anon., Brussels 12 Aug 1656 → Copinger; TSP v.267 | 16 single digits (`2 3 1 4 7 4 6 4 9 7 2 3 is come … to visit the 0 9 3 7`) | a name + a 4-letter word in a 10-symbol cipher | stuck |
| d | Jo. Waddall (London) → "Vanyeare", Bruges, 22 Aug 1656; TSP v.337 | 50 groups, 29 distinct, letters 7-86 + codes 226 243 | homophonic letters + codes; English | stuck |

## What was tried
- **Key matching** (`apply_keys.py`): every 1653-60 royalist/Commonwealth key on cryptiana (Marshall 1656-58,
  Barwick-Hyde 1659-60, Stamford 1655, Butler 1656, Charles II intercepted 1655, Kingston 1658, Westrope 1655,
  Hague agent/Blake) applied to (a)-(d), scored by English/Dutch/French quadgram log-prob. Nothing readable;
  best per-quad scores -4.8…-5.4 vs. ~-3.2 for real text. (d) under the Marshall key gives "Theare is bsgngm of
  ilm sent to lie nere kgcikmd…" — noise.
- **(a) hill-climb** (`solve_a2.py`, Dutch and French quadgram LMs, bijective and homophonic modes, 8 restarts):
  best -4.71 per quad (random -6, genuine Dutch -3.0…-3.4); output fragments like "…ormellenhebelandender…"
  — suggestive of Dutch ("hebben", "-ende") but not a reading. 128 letters over 25 symbols with 8 unknown code
  groups breaking the text is below what the statistics can carry; a plain alphabetical assignment on 10-33 (any
  rotation/reversal) was also excluded (`stats_a.py`).
- **(c)** is a 10-digit cipher: "[12 symbols] is come with a great train to visit the [0 9 3 7]" (Brussels, Aug
  1656 — the arrival of Don Juan José de Austria as governor, or a visit to Charles II's court at Bruges, are the
  obvious contexts). Pattern of the name ABCDEDFDGEAB with the 4-letter word [H G B E] (shares 9,3,7). "the king"
  (k-i-n-g) would force the name to read ?n?dgdfdig?n — impossible, so the digits are not simple letters, or the
  word is not "king". Unresolvable at 16 symbols.
- **(d)**: the clear frame is rich — "There is [6] of [3] sent to lie near [7] and six [6] of [243 226] are [3] to
  strengthen [3], and [8] is so far out of favour now that [5] told me he had a greater mind to [3] him than [4]"
  — but 27 distinct letter-symbols in 50 groups with homophones cannot be pinned; cribs like "horse", "hang" fit
  many assignments equally well.

## Where the originals are
Bodleian **Rawlinson A** (Thurloe papers), volumes v (1653) and xxxviii/xli (1656) per Birch's marginal
references; not digitised. Birch's transcriptions are the only online witness.

## Verdict: STUCK
Too short for cryptanalysis, no key online. Sibling-letter route: (a) — any other 1653 Beverning/Nieupoort
despatch to Boreel with a decipherment in the Dutch Nationaal Archief (Staten-Generaal, liassen Engeland) —
not online in transcription. (b)-(d): the Bruges court's agents' ciphers of 1656 (Hyde/Nicholas with White,
Copinger, Waddall) would be in the Clarendon MSS — not online.
