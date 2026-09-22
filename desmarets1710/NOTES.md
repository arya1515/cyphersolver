# Desmarets, Marly, 4 June 1710 (DECODE R10198)

Status: attempted, open

Outcome: attempted, open. The French text written between the figure lines is not a decipherment of those figures,
and the 471-group numerical code under it has no key on DECODE or in print that I could find.

## The document

- DECODE R10198 "Desmaretz_1", contributed by Alexander Pillon. Nicolas Desmarets, Controller General of Finances,
  Marly, 4 June 1710, to an unnamed "Monsieur". Three pages (images `IMG_R10198_I46716_P1..3.png`, fetched with the
  shared cookie, only 590 px wide; git-ignored in `decode/`, not public domain). DECODE status: "Partially decrypted".
- Layout: pages 1 and 2 (top) alternate a line of French prose with a line of numbers, 34 pairs. Then 22 lines of
  numbers with nothing between them (p. 2 bottom, p. 3), drawn with ruled lines as if for a decipherment that never
  came. The last figure line runs straight into the clear closing "Je suis tres parfaitement Monsieur Votre tres
  humble et tres obeissant serviteur", signed Desmaretz.
- Transcription: `transcription.txt` (G = French line, C = figures under it, U = figures with no French). 471 groups,
  183 distinct, range 1–568.

## What the French says

The French lines read as continuous prose about the Geertruidenberg peace talks (March–July 1710). They say an
attempt ("evenement") has failed. The powers now being sent are wide enough, but will not be pressed all the way.
The correspondent should secure guarantees and explanations about the Allies' "demandes ulterieures". The King wants
peace, but a safe peace that keeps "l'honneur de son gouvernement". Provided the further demands stop short of
"demembrements entiers" and are held to little beyond the preliminaries, he will agree. The talks will not end
without explanations and conferences, but this is "un relachement qui peut produire la paix", which would not have
happened "si l'on estoit demeure fermes dans les premieres resolutions." The prose stops there, and the last 22 lines
are figures alone.

## Why the French is not the decipherment of the figures

I ran four alignments of the 34 glossed lines against the figures under them:

1. Per-line letter EM (`em.py`): each group emits 0–9 letters. Degenerate.
2. Global letter alignment with a length prior (`em2.py`). Drifts out of sync.
3. Per-line soft EM with word-boundary bonuses (`em3.py`).
4. Word-level EM, where a group emits 0–2 whole words (`emw.py`).

None of them gives a consistent key. The frequent groups fall under unrelated words: 111 under "paix", "seure",
"selon", "on", "apparence"; 231 under "toutes", "fermes", "la"; 209 92 85 under both "vostre courier" and
"inevitable, peu". Repeated French phrases do not repeat in the figures: "demandes ulterieures" sits over
128 78 65 343 147 and over 209 64 321 161 27, and "qu'on vous envoye" shares only 64. The line-offset test
(`offset_test.py`) finds only a weak group overlap between lines that share French words (0.77 at offset 0,
against 0.49 for any two lines; 22 pairs).

The figures are a real code, not decoration. There are 183 types in 471 tokens (a uniform random fill would give
about 320), a Zipf-like head (111 ×13, 224 ×11, 347 ×10, 56 ×10) and repeated n-grams, among them the 6-gram
119 101 402 49 197 424. It first occurs under "dans les premieres resolutions" and again in the unglossed tail.

Reading: this is the "partially encrypted" letter DECODE describes. The prose lines are the clear part, in the same
hand as the closing formula. The figure lines carry a separate secret text in a numerical code of about 570 values,
probably a syllabic nomenclator with homophones, of the kind the Paris ministries used. The one shared 6-gram hints
that the secret part may deal with the same resolutions, but that is not a reading.

## Checks

- Web search for a printed text of the 4 June 1710 letter: nothing. Not checked: Boislisle, *Correspondance des
  contrôleurs généraux* III (1897), and the AE Hollande volumes for 1710 (Torcy–Huxelles–Polignac). Either could hold
  a copy in clear, and they are the best leads.
- DECODE keys dated 1700–1715: none French-ministerial (Saxon Flemming keys, Florentine, ACA Genoa). No sibling
  "Desmaretz_2".
- Ciphertext-only on a ~570-value homophonic code from 471 groups is not realistic (compare hellen1752, spaen1808).

## To move it

A clear copy or minute in AE Correspondance politique Hollande 222–224 (1710), or in Desmarets's papers
(AN G7 / BnF), or the key from the recipient's side. The recipient is probably one of the Geertruidenberg
negotiators (Huxelles or Polignac) or a banker go-between. Images at 590 px are also marginal for some digits.
