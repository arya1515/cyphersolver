# Feuquières → Catinat, Pignerol, 25 January 1691 — attempted 2026-09-15

Cryptiana "French Cipher Despatch received by General Catinat (1691)"; Tomokiyo's article `louisxiv.htm` §7 ("An
Unbroken (?) Code/Cipher for Catinat (1691)"). Antoine de Pas, marquis de Feuquières, governor of Pignerol since the
end of the 1690 campaign, to Nicolas de Catinat, commanding in Piedmont, then at Suze.

## Sources (all reachable from scripts, 2026-09-15)

* **The ciphertext.** *Mémoires et correspondance du maréchal de Catinat* (Paris, Mougie, 1819), t. II, Pièces
  justificatives (1), pp. 283-284. Bayerische Staatsbibliothek digital copy bsb10720287, scans 317-318
  (`img/t2_0317.jpg`, `img/t2_0318.jpg`, fetched from the IIIF image API; the hOCR of the whole volume comes from
  `https://api.digitale-sammlungen.de/ocr/bsb10720287/<scan>`). Tomokiyo's transcription was collated against the
  page images: **three corrections on p. 284**: `114 285 362` (Tomokiyo 283), `154 259 143` (Tomokiyo 250),
  `156 99 135 59` (Tomokiyo 133). `ciphertext.txt` carries the corrected text: **418 groups, 160 distinct, range
  4-366**, in two paragraphs (the print indents a new paragraph at `65 32 5 240 ...`).
* **What the letter is about.** The 1819 editor (t. II p. 8): "Nous avons une dépêche chiffrée de Feuquières, datée
  du 25 janvier 1691, à Pignerol, où il se concerte avec Catinat sur l'attaque de Veillane, fixée pour le 27. Tous
  nos efforts ont été vains jusqu'à présent pour la traduire." Veillane = Avigliana, in the Susa valley between Suze
  and Rivoli, held by a Savoyard garrison (500 Germans of Lorraine, the Croix-Blanche, four companies of Macel's
  dragoons, per Catinat 12 Jan). The attack of 27 January 1691 failed; Feuquières and Catinat blamed each other
  (Catinat to his brother, Gap, 19 Feb 1691, t. II pp. 6-8; Feuquières, *Mémoires*, quoted in the note below).
* **Cribs from the same weeks.** *Lettres inédites des Feuquières* (Paris, 1845), t. V, pp. 323-334 (archive.org
  `lettresinditesde05tien`, OCR): Catinat to Feuquières, Suze, 12 Jan 1691 (used as the control plaintext,
  `control_plain.txt`), and Catinat's **"Mémoire pour l'entreprise de Veillane", Suze, 19 Jan 1691**: Feuquières to
  leave Pignerol in the evening with all his cavalry and dragoons and 1,200 foot; rendezvous "à la teste des estangs
  de Veillane"; two roads, by Gumiane and Javan or by Trane past the Chisola below Piosasque; seize the Capucins and
  the faubourg; four days' bread, oats for the horses, powder, three pack-horses or mules of tools and hatchets,
  miners' tools from the Pignerol magazines, a hundred grenades; Suze's column, two cannon, 20 horses to be asked of
  Feuquières. The 25 Jan letter is Feuquières' answer to this memoir. Its vocabulary is in `solver.py` (DOMAIN, CRIBS).
* **Bazeries.** Burgaud and Bazeries, *Le Masque de fer* (1893), p. 272, says Bazeries deciphered this "petit chiffre"
  as well; no text was ever published (Tomokiyo). "Petit chiffre" is Bazeries' term for a two-table code with few
  entries (jfbouch.fr). Bazeries' Catinat papers (the Grand Chiffre, DE=34/42/97, entries to 587) are a different
  code; Feuquières wrote to Louvois in the Grand Chiffre and to Catinat in this small one.

## Structure

| test | result |
|---|---|
| tokens / distinct / max | 418 / 160 / 366; IC 0.0088 (Norbert on Klausis Krypto Kolumne, 2016: the Catinat 1702 letter gives 0.0088 too) |
| share of tokens below 100 | **46 %** (192 tokens on 50 distinct groups; 96 of 363 possible values = 26 % of the range). Mean 3.8 tokens per used low group vs 2.1 above 100: the high-frequency units (letters) sit below 100, the syllables and words above. Same skew as Catinat 1702 (253 of 591 below 100) |
| step-10 chains (Croissy one-part signature) | 20 chains of ≥3 among the 160 used values; random sets of 160 values give 16.9 ± 2.6, P = 0.16. Pairs (g, g+10): 69 observed vs 68.3 expected. **No column structure**: not a Croissy table. Consistent with a two-part arrangement inside each block |
| repeats | `301 151 310` ×3 (twice as `150 301 151 310`), `101 229 255 243` ×2, `60 300 57 78` ×2, `210 51 81 91` ×2, `78 44 200` ×2, `317 101 193` ×2, `44 200` ×3; 26 further bigrams ×2; no immediate doublets |
| letter block | 50 distinct groups below 100 for ~22 letters: 2-3 homophones per letter, as in the Louvois code of 1676 (t. II pp. 343-352: 3 numbers per letter, 2 per syllable, 11 nulls, 300 entries). Sukhotin on the low-group adjacency gives a vowel class of 15 groups carrying 72 of 192 low tokens (38 %) |
| spelled stretches | 100 runs of consecutive low groups; 14 of length ≥4, longest 9 (`65 21 63 59 65 91 22 60 52`) |

So the working model is: letters with homophones scattered over 1-99, CV syllables, a few hundred-odd words and nulls
scattered over 100-366, no alphabetical order in either block. That is the design the solver and the control assume.

## Attack

`solver.py`: simulated annealing over group → unit, units = letters / nulls below 100 and CV syllables, common letter
groups, the 500 most frequent words of the period corpus, the Veillane vocabulary and period spellings above 100;
scored by the spaceless 7-gram French model of the Chaulnes attempt (`../chaulnes/lm7.pkl`, 6.1 M characters), a
per-letter bonus, a unit prior, a null penalty and a crib bonus (each crib word counted at most twice); moves include
placing a crib word over a run of groups with the letter/syllable split dictated by the groups' classes.

`make_control.py`: Catinat's letter of 12 Jan 1691 encoded with a random code of the inferred design (letters 2-3
homophones over 1-99, syllables 1-2 numbers and ~100 words over 100-366, nulls), encoding rates tuned to the
target's profile: 418 tokens, 155 distinct, 184 low tokens (target 418 / 160 / 192).

Results (`sweep_control.txt`, `seed_test.txt`, `run_real_*.txt`):

| run | result |
|---|---|
| n-gram objective, calibration sweep on the control (`sweep_control.txt`, 100k iterations each, six weightings of letter bonus, unit prior and crib bonus) | in every weighting the solver's best wrong key outscores the **true key** by 150 to 1,400 nats; recovery 4-12 % of tokens. Decomposition: the true text has 779 letters and scores -1.84 nats per letter under the LM; the solver's texts have 830-2,250 letters made of dictionary words and score -1.3 to -1.5 per letter, so the letter bonus and the crib bonus are farmed by mapping groups to long words ("canon cavalerie et canon ce sa garnison de cette canon...") |
| word-segmentation objective (`solver_w.py`: Viterbi over a period dictionary, 7 nats per uncovered letter) | same wall: after 3,000 iterations a word salad of short function words ("a sa es a ne se sa le le ai au son et la on...") scores -1,590 against the truth's -1,724; 34/418 tokens recovered |
| how much crib would bite (`seed_test.txt`: a fraction of the true code fixed, the rest annealed, 100k iterations) | 20 % of groups given → 14 % of the remaining tokens recovered; 40 % → 43 %; **60 % → 63 %**; 80 % → 81 %. Even with most of the code in hand the objective still prefers a wrong completion (best -1,650 vs truth -1,844 at 60 %). The Veillane cribs, a dozen words, are far below what is needed |
| real letter, two seeds, 300k iterations (`run_real_1.txt`, `run_real_2.txt`) | scores -81 and -155, i.e. the crib-farmed regime the control predicts; outputs are strings of crib words joined by letters ("de veillane le s pointe l i s te est trane s e r e poudre a chevaux...") and are **not readings**. Not reported as a decipherment |

**Verdict: attempted, not solved.** 418 groups over a 160-group two-part nomenclator are as underdetermined as the
300 groups of the Chaulnes letter were, and the crib vocabulary, though certain, is too small to constrain it. What
would open it: Bazeries' working papers (he read the letter, *Le Masque de fer* p. 272), a second letter in the same
code (Feuquières' other despatches to Catinat of the winter 1690-91 are in the Catinat papers; the 1819 editor
printed only this one), or the key itself among Louvois' ciphers (BnF fr. 6204 holds Louvois' keys of the 1690s,
checked for Chaulnes; a Feuquières-Catinat "petit chiffre" of 366 entries would be the thing to look for there).

Also checked and negative: no clear copy or paraphrase of the letter anywhere in the three volumes of the 1819
Mémoires (full OCR searched for Veillane, Feuquières, chiffre); the 1845 Lettres inédites print Catinat's side of the
exchange (12 and 19 Jan) but no Feuquières letter of January 1691; Bazeries' papers are not online.

## Files

| file | purpose |
|---|---|
| `ciphertext.txt` | corrected transcription, with the three collation notes |
| `img/` | page images of pp. 283-284 from the BSB IIIF server, and crops |
| `louis1676.jpg` | Tomokiyo's partial table of the 1676 Louvois two-part code, the design comparison |
| `control_plain.txt`, `make_control.py`, `control.txt`, `control_key.txt` | matched synthetic control |
| `solver.py` | the solver (n-gram objective) |
| `run_real_*.txt`, `sweep_control.txt`, `seed_test.txt`, `solver_w.py`, `sweep_control.py`, `seed_test.py` | run logs and the two calibration harnesses |
| `catinat1702_1.txt` | Tomokiyo's frequency table of the 1702 Catinat letter (43 % of 591 tokens below 100, 50 low groups: the same design) |
