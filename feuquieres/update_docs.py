# One-off: prepend the solved-state section to NOTES.md, rewrite the tracker and README rows, extend .gitignore.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

notes_new = r'''# Feuquières → Catinat, Pignerol, 25 January 1691 — **read 2026-09-16** (586 of 601 tokens over the two letters in the code)

**Result.** The 418-group despatch is written in the *petit chiffre* of the Pignerol governors (Bazeries' term; 367
groups, the small companion of the Grand Chiffre of 1691). The same code carries a second printed letter that nobody
had connected with it: **Louvois to d'Herleville, governor of Pignerol, Versailles, 6 September 1690**, printed in
cipher *with its contemporary "traduction"* in the 1819 *Mémoires de Catinat*, t. I pp. 140-142 (MDZ bsb10720286
scans 212-214, `herleville.txt`, `img1/`). d'Herleville was Feuquières' predecessor at Pignerol; the cipher stayed with
the governorship. The two letters share 72 of the d'Herleville letter's 91 groups, the same 46 % share of tokens on
groups below 100, twenty bigrams and the trigram `25 355 42` (= *de Mon-de[vis]*). Aligning the d'Herleville cipher
with its translation and propagating every reading to the Feuquières letter (and back) gives a key of 167 of the 179
groups used (`key_petit_chiffre_1690.tsv`) and the reading below (`reading.txt` gives the group-by-group alignment).

## The Feuquières letter, as read (17th-century spelling kept; unread groups in brackets)

> Je reçois, Monsieur, à dix heures du matin la lettre que vous me faites l'honneur de m'escrire du vingt-quatre,
> avec le duplicata. Vous aurez veu [par] le retour du courrier que je vous dis [54 257]is [go] exécuter vos ordres.
> [Par] cecy vous sçaurez que je suis tout prest, [333] qu'on ne pense [9 go ri 122] les [des] que vous [122]u les
> commencer. [À] Veillane, persuadé qu'ils enlèveront le [19] au bruit de l'attaque de Veillane, le peu de monde
> qu'il y a et les moyens d'y entrer, tout doi[ven]t faire croire qu'ils ne viendront pas à le défendre
> sérieusement. Je ne sçais du tout par où faire passer à Saint-Ambroise les quatre-vingts maistres que vous [vous]
> demandez ; les chemins pour y aller du costé de Javan e[t] [a 132 257 l] vous coupe[s] [249 86]. En approchant de
> Veillane on trouve deux chemins, dont l'un vous conduit au fauxbourg des Trois Couronnes, l'autre aux maisons [292]
> et le long de l'estang. J'attaqueray [353] deux endrois, et surtout [mes se 271 se s] prendray garde que les dragons
> ne puissent m'eschaper. [342 103 190]

What it says: Feuquières acknowledges Catinat's letter of the 24th (received at 10 a.m. with its duplicate), says he
is ready and that the return of the courier carries his execution of Catinat's orders; the enemy will not defend
Veillane seriously (few men inside, ways in known); he does not see how to get the 80 horse Catinat asked for to
Sant'Ambrogio (the village between Avigliana and Rivoli) because the roads from the Javan side cut across; two roads
lead into Avigliana, one to the faubourg "des Trois Couronnes", the other to the houses along the pond; he will
attack at two points and above all keep the dragoons (Macel's, in the town) from escaping into the castle. This is
exactly the plan of Catinat's "Mémoire pour l'entreprise de Veillane" of 19 Jan (rendezvous at the head of the
estangs, the Javan and Trane roads, the faubourg, the dragoons) and matches Feuquières' own account in his
*Mémoires* ("ce régiment de dragons qu'on vouloit enlever dans la ville"). The letter's date, 25 January, the time
"dix heures du matin", and "du vingt-quatre" are all internal.

The last three groups (`342 103 190`) and the first eight of the d'Herleville letter (`39 249 190 86 40 103 190 11`,
with `103 190` common to both) are almost certainly nulls or a stock closing/opening, as in the Grand Chiffre, where
paragraphs begin and end with two to four "point ou nulle" groups.

## The d'Herleville letter (control: it matches its printed translation, with the clerk's own wording)

> [8 groups] Je mande à M. de Catinat que le roy vous permettoit de demander la contribution au pays de Mondevis, et
> que si vous croyez qu'il convien[s]t au servi[ce s] le roy de les exempter, mesme de permettre aux habitans dudit
> pays de razer la citadelle du[d]it Mondevis, de le faire. — J'atendray avec impatience l'arrivée du prochain
> ordi[n]aire pour sçavoir comment aura réussi vostre entreprise sur le chasteau de Villefranche.

The 1819 "traduction" reads *si vous jugez qu'il convient au service du roi* and *Mondovi*; the cipher has *si vous
croyez*, *Mondevis*, *razer*, *M. de Catinat* as one group (218), *le roy* as one group (102). That the translations
were free renderings, not verbatim decipherments, is also visible on the Grand Chiffre letter of the same day to
Catinat (t. I pp. 142-144), which decodes with Bazeries' table as *importantes nouvelles de la reussite* where the
printed translation has *des nouvelles*. This is why every exact known-plaintext aligner failed (see Method).

## The key (design)

Two-part code of 367 groups, the Grand Chiffre's little brother: **letters** (i/j and u/v one letter each) with two to
four homophones each, mostly below 100 (e: 4 41 125 212; s: 21 134 200 252 304; t: 91 322 343 362; n: 51 154 228;
r: 60 82 178 275; a: 32 213 251; u: 37 78 191 285; d: 63 168; l: 43 68; i: 90 144 182; y: 24 59; g: 81 259; x: 181
352; b: 40 50; f: 124 366; p: 5 240; c: 101; m: 28; o: 27; z: 104); **syllables** of the Grand Chiffre kind (ma 106,
ti 175, ro 113, ri 188, ra 135, re 22/44, se 83/110/183, pe 235, ve 150/165, vi 210, co 57/153, di 146/217, li 254,
ca 93, ha 193, he 229, mi 255, bo 318, bu 202, cu 179, fa 108, ga 279, go 145, lo 231, ta 156, te 205, to 250, va 76,
ci 169, do 214/311, su 247, xe 111, on 160, en 65, ns 243, st 234, is 280, oit 126, ment 85, mais 172, moy 334, puis
136, vie 148, sca 328, scavoi 74); **words** (de 25 42 71, que 99 147, le 56 177, la 114 151, les 47, des 237, du 300
347, au 184, et 258 341, si 196, y 24, on 100, ou 197, par 216, pas 195, pour 350, sur 88, tout 266, vous 84 241,
mesme 2, comme 80, peu 278, lettre 15, honneur 31, le roy 102, M. de Catinat 218, Monsieur 296 (with 355 mon), vostre
149, quil 164) and **nulls / points** (52, 194, and the opening and closing groups above). Numbers are spelled (*dix*,
*vingt-quatre*, *quatre-vingts*, *deux*). Place names are spelled (Veillane = ve-il-la-ne, Javan = ia-va-n,
Saint-Ambroise, Villefranche = vi-l-le-f-ra-n-c-he, Mondevis = mon-de-vi-s).

## Method (what finally worked, and what did not)

1. **Bazeries' Grand Chiffre de 1691 transcribed** from the Gallica page images of *Le Masque de fer* pp. 280-289
   (`bazeries/f305-f315.jpg`, `grand_chiffre_1691.tsv`, 587 entries, 91 left blank by Bazeries). Checked by decoding
   the 19 Aug 1691 despatch he prints as proof (`aug1691_decoded.txt`) and the three Louvois-Catinat letters of 6, 8
   and 10 Sept 1690 printed in cipher in the 1819 *Mémoires* t. I: all read cleanly. The table gives the *design* of
   the petit chiffre (Bazeries, p. 272: "il ne différait du grand que par son nombre de groupes"): letters with
   homophones, CV syllables, word stems, nulls, i/j and u/v merged.
2. **Second letter found.** The hOCR of all three 1819 volumes was pulled from the MDZ API (`fetch_mdz_ocr.py`,
   `catinat1819_*.txt`, not tracked) and searched for runs of numbers. Vol. I pp. 140-141 holds the d'Herleville
   letter in the petit chiffre with its translation; vol. II pp. 297-343 holds some 12,000 groups of Grand Chiffre
   letters of 1691 (Louvois to Catinat, no translations printed; they decode with the table, a by-product to exploit
   separately); vol. I pp. 15-17 holds an older Casal cipher of the 1680s with the editor's partial interlinear
   decipherment.
3. **Exact known-plaintext alignment fails** (beam aligner `align.py`, self-tested on synthetic encodings: fine),
   because the translation is not verbatim and because i/j, u/v are single letters. Annealers scored on the
   translation's 5-grams, on the LM with the closed inventory, or with the partial key fixed, all produced word salad
   (`solver_gc.py`, `solver_trad.py`, `solver_joint.py`, `solver_fixed.py`): the design-faithful control
   (`make_control_gc.py`) confirms 10-12 % recovery, truth outscored by more than 1,000 nats. Stochastic search is the
   wrong tool here.
4. **What worked: anchoring by hand and propagating between the two letters.** The second half of the d'Herleville
   P2 admits one segmentation of exactly 31 groups (*comment aura réussi vostre entreprise sur le chasteau de
   Villefranche*) in which every repeated group agrees; those units, carried into the Feuquières letter, gave *heures
   du matin*, *du vingt-quatre*, *m'escrire*, *duplicata*; each new word fixed further groups (Veillane from the
   thrice-repeated `301 151 310`, *enleveront*, *trouve*, *doivent* from 150 = ve, *dragons* / *chemins* / *maisons*
   from 243 = ns, Saint-Ambroise from the *faire passer à …* clause, *le long de l'estang*, *dont l'un … l'autre*).
   `show.py`, `ctx.py` and `reading.txt` are the working tools; `key_partial.txt` the working key.

## What remains

Twelve groups unread (singletons or doubletons: 9, 19, 54, 122, 132, 194, 257, 271, 292, 333, 353 and the
opening/closing nulls), and a few units marked `?` in the key: *Trois Couronnes* (237 322 46 is 153 u ro n ne s;
"des trois couronnes" is the reading that fits the groups, a faubourg or inn of that name at Avigliana is
unverified), *do* 214/311, *par ou* 216/197, *vous* 241 (perhaps *nous*), *le roy* 102 vs *roy*. Check against the
original (SHD, Archives du dépôt de la guerre vol. 1079, where Catinat's 29 Jan report also sits) if it can be seen.
Bazeries' reading of 1893 was never published; this is, as far as we know, the first since his.

---

# Earlier state (2026-09-15): attempted, not solved — kept for the record

'''
p = os.path.join(HERE, 'NOTES.md')
old = open(p, encoding='utf-8').read()
if 'read 2026-09-16' not in old:
    open(p, 'w', encoding='utf-8').write(notes_new + old)

row_targets = ('| 24 | Feuquières → Catinat, Pignerol, 25 Jan 1691 (Mémoires de Catinat 1819, t. II pp. 283-284; cryptiana "Cipher Despatch received by General Catinat (1691)") | 1691 | Hard | **read** (586/601 tokens of the two letters in the code; 167/179 groups) | `feuquieres/` | '
    "2026-09-16: solved. The code is the *petit chiffre* of the Pignerol governors (367 groups, companion of Bazeries' Grand Chiffre de 1691, whose table was transcribed from the Gallica images and verified on four 1690-91 despatches). A second letter in the same code, Louvois → d'Herleville 6 Sept 1690, is printed **with its translation** in the 1819 Mémoires t. I pp. 140-142 (found by searching the MDZ hOCR of all three volumes); the two letters share 72 groups. Exact known-plaintext aligners and annealers all failed (translation not verbatim; i/j, u/v merged); hand anchoring from one 31-group consistent segment and propagation between the two letters read the rest. Feuquières: received Catinat's of the 24th at 10 a.m. with duplicate; is ready; enemy will not defend Veillane seriously; cannot see how to pass the 80 horse to Saint-Ambroise (Javan roads); two roads into Avigliana, faubourg \"des Trois Couronnes\" and the houses along the estang; will attack at two points and keep the dragoons from escaping. 12 groups (singletons) unread; key in `key_petit_chiffre_1690.tsv`, readings in `reading.txt`, NOTES. Also found: ~12,000 groups of Grand Chiffre 1691 letters in t. II pp. 297-343 without translations, decodable with the table |")
row_readme = ("| Feuquières → Catinat, Pignerol (418-group two-part \"petit chiffre\") | 1691 | **Read** (16 Sept 2026): the code is the petit chiffre of the Pignerol governors, companion of Bazeries' Grand Chiffre de 1691 (table transcribed from Gallica and verified on four 1690-91 despatches). A second letter in the same code, Louvois to d'Herleville of 6 Sept 1690, sits in the 1819 Mémoires t. I with its contemporary translation; the two letters share 72 groups, and hand alignment carried between them reads 586 of 601 tokens. Feuquières fixes the Veillane surprise: ready on receipt of Catinat's letter of the 24th, the enemy will not defend seriously, two roads into Avigliana (the faubourg and the houses along the pond), 80 horse to Saint-Ambroise, attack at two points, keep the dragoons from escaping. First reading since Bazeries' unpublished one of 1893 | [`feuquieres/`](feuquieres/) |")

for fn, start, row in ((os.path.join(ROOT, 'TARGETS.md'), '| 24 | Feuquières', row_targets),
                       (os.path.join(ROOT, 'README.md'), '| Feuquières → Catinat, Pignerol', row_readme)):
    lines = open(fn, encoding='utf-8').read().split('\n')
    for i, l in enumerate(lines):
        if l.startswith(start):
            lines[i] = row
    open(fn, 'w', encoding='utf-8').write('\n'.join(lines))

gi_path = os.path.join(ROOT, '.gitignore')
gi = open(gi_path, encoding='utf-8').read()
add = '\n# feuquieres: bulky fetched texts and run logs (regenerate with fetch_mdz_ocr.py / archive.org / the solvers)\nfeuquieres/catinat1819_*.txt\nfeuquieres/rousset4.txt\nfeuquieres/feuq5.txt\nfeuquieres/masque_de_fer_1893.txt\nfeuquieres/m_bsb*.json\nfeuquieres/run_*.txt\nfeuquieres/ctx_out.txt\nfeuquieres/knockout_p2.txt\n'
if 'feuquieres/catinat1819_' not in gi:
    open(gi_path, 'w', encoding='utf-8').write(gi + add)
print('docs updated')
