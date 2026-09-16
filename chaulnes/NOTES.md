# Louis XIV to the duc de Chaulnes, Versailles, 10 July 1690 — attempted 2026-09-16, not solved

Cryptiana "French Cipher to Ambassador in Rome (1690)"; Tomokiyo's article `louisxiv.htm` §4B; Klausis Krypto
Kolumne 31 Jan 2019 ("Can you decipher this letter written by Louis XIV?", 13 comments, unbroken). The letter,
signed *Louis*, countersigned *Colbert* (de Croissy), was offered by the Paris dealer Traces Écrites in 2017
(ref. 11273, "300 chiffres"); five page photographs are on the Klausis post and the dealer's page, and the
dealer's page carries a transcription of the clear parts with all but one cipher paragraph. Chaulnes was
ambassador extraordinary in Rome 1689-91 for the "affaire des bulles": Alexander VIII would not institute the
bishops named since 1682 unless the prelates who had sat in the 1682 Assembly disavowed the Four Articles.

## What was done

**Ciphertext.** All nine cipher passages verified group by group against the page images at 2x
(`crop_*.png`) and written to `ciphertext.txt` with the surrounding cleartext: **300 groups, 116 distinct**
(the dealer's "300 chiffres" is exact). Two corrections to the dealer/Tomokiyo transcription: p.1 l.5 reads
**527 523** (not 823), and the "mandiez que" passage reads **456** (not 458). Nine groups are underlined
(527, 32 twice, 313, 48, 535, 306, 439, 30, 138) and two small raised figures (2, 3) sit in the long paragraph.
Frequencies: 170 x14, 306 x13, 22 x12, 172 x10, 180 x10, 488 x10, 201 x7, 433 x7, 10 x7, 523 x6.
Repeats: 306 180 (x5), 22 306 180 (x3), 523 172 (x3), 12 122 118 434 (x2), 509 102 433 (x2), 306 180 124 12x 396
(x2, once 122 once 120).

**Structure.** The Colbert de Croissy foreign-office codes of 1684-1702 recovered by Wallis, Lasry and Tomokiyo
(d'Avaux 1684, Béthune and Teil 1689, Castaignère 1690, Harlay 1694, Usson 1702) share one design: single
letters at low numbers in alphabetical order (a=10, 12, 14... or a=20, 22... or a=2,3; b=5,6...), then a
ten-column table numbered row by row in which one consonant's syllables run down a column in the order
a-e-i-o-u at steps of 10, with words in the column of their initial. This letter fits that design: 24 distinct
groups below 80 (67 tokens, 22%), and step-10 chains 170-180-190-200 (14/10/5/1), 172-182-192, 120-130-140-150,
122-132-142-152, 436-446-456, 439-449-459-469-479 (a full five-vowel run), 473-483-493, 481-491, 513-523,
433-443, 386-396. So the code is a one-part Croissy table of at least 535 entries, different from the 1690
Castaignère code (its top groups 53, 202, 59, 98, 185 barely occur here).

**Printed plaintext (the Richelieu route).** The letter answers Chaulnes' despatches of 8, 12 and 17 June 1690
and its minute should be in Archives diplomatiques, Correspondance politique Rome vol. 331 or 332. Checked and
negative: *Recueil des instructions... Rome* t. II (Hanotaux/Hanoteau 1911, full text) quotes the King's letters
of 18 and 24 Jan, 6 Feb and 14 Sept 1690 but not 10 July; Gérin, *Louis XIV et le Saint-Siège* (1894, both vols)
stops in the 1670s; Gérin, *Recherches historiques sur l'Assemblée de 1682* (1870) has no 1690 Chaulnes
material; Google Books full-text search for the letter's distinctive clear phrases ("duplicata de vos lettres des
8, 12 et 17 juin", Ratabon/Durazzo/lardons) returned nothing before the API rate-limited this address. Not
reachable from scripts: Gérin's 1877 *Revue des questions historiques* article "Le pape Alexandre VIII et Louis
XIV" (t. 22, on Gallica only; Gallica and HathiTrust block scripts). DECODE's public metadata has no record
for Chaulnes or a 1689-91 Rome key; BnF fr. 6204 holds Louvois' ciphers, not Croissy's.

**Ciphertext-only attack, with a matched control.** `solver.py`: simulated annealing over a code-to-unit map
(units = letters, CV syllables, common bigrams, 500 frequent words plus a domain list), scored by a spaceless
character 7-gram model trained on 6.1 M characters of period French (`corpus_fr.txt`: Recueil t. II, Gérin's
three volumes), with the cleartext of each passage as context, a per-letter term, a unit prior, a null penalty
and a bonus for step-10 chains decoded as one consonant's vowel series. Control (`make_control.py`,
`control.txt`): a King's instruction from the Recueil encoded with a random code of the same design (letters
2-3 homophones, ten-column syllable table, 120 words, nulls), 300 groups in 11 passages, 105 distinct groups.

| objective version | control: true key | control: solver best (3 seeds) | tokens recovered |
|---|---|---|---|
| v1 LM with spaces, words allowed | — | -1443 / -1482 / -1532 | 4% / 0% / 1% (degenerates to "les les que pour") |
| v2 spaceless LM, class-restricted units, run moves | -857 | -973 / -922 / **-867** | 6% / 6% / 1% (better score than the truth, by mapping 30 codes to null) |
| v3 + per-letter bonus 1.0, null penalty | 30 | 397+ at 100k iterations | — (over-rewards long words; abandoned) |
| v4 + unit prior, per-letter bonus 0.7 | **-799.5** | -829 / -839 / -801 | 4% / 4% / 12% |

With the calibrated objective the solver's wrong solutions score within 2-40 nats of the true key, i.e. 300
groups do not determine a 116-entry nomenclator even with the cleartext context and the structural prior. This
is the same wall Lasry reports for d'Avaux 1684 ("too many distinct codes, and the automated algorithms did not
produce any valid solution"); he broke that letter only after inferring the letter block from a related 1688 key.
The real letter was run through v1-v2 as well (`run_real_*.txt`, `run2_real_*.txt`); the outputs are fluent
nonsense of the kind the control predicts and are not reported as readings.

**Letter block.** All alphabetical hypotheses for the groups below 80 (six alphabets, seven homophone schemes,
start 1-29) were scored on the low-code bursts ("5 47 53 6 10" after "lettre du 25e d'avril", "2 47 49 3 12"
after "eveschés", "12 32 51 22", "22 50 10") with the same model: the best is -2.7 nats per letter, against
-1.0 to -1.5 for real French, so the low block is not a plain alphabetical run of the kinds seen in the sister
codes, or it mixes letters with two-digit words and nulls as the Teil and Béthune codes do (Teil 1689: even
numbers 14-52 are nulls, 10 deletes the preceding group).

## Observations that a future solver can use

* 22 (x12) precedes 306, 170, 180 or 190 in nine of twelve occurrences and follows 433, 434, 409: a
  word-final letter (s, t or e) before a frequent word or the l/s-column syllables.
* 170-180-190-200 (14/10/5/1) has the frequency profile of la-le-li-lo or sa-se-si-so; 172-182-192 beside it
  would then be the next consonant's a-e-i.
* 433 (x7) is preceded by five different groups (381, 309 x2, 102 x2, 409 x2) and never by 22 or a low group:
  the profile of a suffix or particle entry such as *tion*, *que* or *ment*; 509 102 433 (x2) is a three-group
  word ending in it.
* 488 (x10) has no step-10 neighbours: a word. Thomas Ernst's syntactic reading *ne/ni* (Klausis comment 7)
  fits "jusqu'à présent de 488 408 190 192 488 168 ..." if the passage is Chaulnes' policy "de ne point presser
  l'expédition des bulles" (Recueil t. II p. 27 n. 2, Chaulnes to Croissy 26 Jan 1690).
* The six bishops "nommez qui ont assisté à l'assemblée de 1682" whose bulls were at issue (Poudenx/Tarbes,
  Camps/Pamiers, Bonnin de Chalucet/Toulon, Gourgues/Bazas, Lézay de Lusignan/Rodez, Vintimille du Luc/
  Marseille; Recueil t. II p. 27 n. 4) and the negotiators (cardinals Cibo, Ottoboni, Acciaioli, Sainte-Cécile,
  abbé de Polignac) are the likeliest proper names in the long paragraph.

## Gérin 1877 checked (2026-09-16, volume supplied by Daniel from Google Books)

*Revue des questions historiques* t. XXII (1877) pp. 135-210, Ch. Gérin, "Le pape Alexandre VIII et Louis XIV"
(text extracted to `gerin1877.txt`; the PDF is not tracked). Gérin worked from AE Rome Corr. 321-345 and quotes
Chaulnes at length, but **he does not quote or cite the King's letter of 10 July 1690**. His 1690 citations of
the King's side are 24 Jan, 13 Feb, 19 May ("vous avez bien fait de désavouer tout projet de lettre, si le pape
veut soumettre l'affaire aux cardinaux"), 22 May (he would allow at most that after the expedition of the bulls
the next assembly thank the Pope "de la bonne justice rendue à tant de prélats"), then Forbin's instructions of
15 May and the letters to Forbin of 1 and 14 Sept. The "10 juillet" on his p. 182 is Chaulnes' despatch of that
day (Rome 331), not the King's. So the Richelieu route closes here: no printed plaintext of this letter exists
in Gérin, Hanotaux/Hanoteau or Gérin 1870/1894.

What the article does supply is the subject matter of the enciphered passages, from Chaulnes' letters of
25/28 April, 5, 12, 23, 30 May, 6, 8, 27, 30 June and 1 July (Rome 331): the Pope wanted to put the bishops'
draft letter to a congregation of cardinals (Albani, Rubini, Panciatichi, Ottoboni) and Chaulnes opposed it and
threatened to withdraw all his drafts and ask for his congé; Rome rejected the Versailles draft in which the
bishops say the 1682 doctrines were "reçues de tout temps en France"; Chaulnes refused to link the Régale to the
bulls though authorised to; he proposed that the coming Assemblée du Clergé write to the Pope disavowing any
decision of faith. These are the likeliest contents of P1 (the June "diligences"), P5 (what Chaulnes "croyez"
the Pope will accept from "ceux qui ont assisté à l'assemblée de 1682 et qui sont nommés"), P6 (Chaulnes' policy
"jusqu'à présent de ne point..." linking the Régale) and P8 (instances made to the Pope). They are paraphrases,
not the King's words, so they narrow the vocabulary without giving an alignable crib; against the control result
above they were not used to force a reading.

## What would solve it

1. The minute: Archives diplomatiques (La Courneuve), Correspondance politique Rome vol. 331-332, "le Roi à
   Chaulnes, 10 juillet 1690"; or Chaulnes' letters of 8, 12, 17 June (vol. 331) as cribs. Not digitised.
2. Any other letter in the same code with an interlinear decipherment (the Chaulnes papers were dispersed
   through the trade; the 1693 letter in Kahn is the Castaignère code, not this one).
3. Gérin 1877 (RQH t. 22), which quotes this correspondence from the archive, for a reader with Gallica access.

## Files

`ciphertext.txt` (verified groups with cleartext), `Louis-XIV-1..5.jpg` and `crop_*.png` (pages and 2x crops,
not tracked), `traces_wb.txt` (dealer transcription via Wayback), `klausis_comments.txt` (the 13 comments),
`lm.py`, `solver.py`, `make_control.py`, `eval_control.py`, `truekey.py`, `control*.txt`, `run*_control_*.txt`,
`run*_real_*.txt`, `louisxiv2.txt` (Tomokiyo's Castaignère decode), `louis1689A/B.png`, `louis1693b.jpg`,
`louis1684.png`, `louisxiv1694.png`, `louisxiv1702a/b.jpg` (sister-code sheets), `lasry_davaux.txt`.
Corpus texts and the 7-gram model are rebuilt with `python lm.py` after downloading the archive.org djvu texts
named in the notes.
