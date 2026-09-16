# DECODE R1408, "Di Varsouia 24 Xbre 1627" (ÖStA HHStA Staatskanzlei Interiora, Chiffrenschlüssel Kt. 14 Fasc. 20 f. 176) — NOTES

**Verdict: read.** A homophonic substitution with an alphabet in plain order (odd figures 13–33 = *a b c d e f g h i l m*,
even figures 14–32 = *n o p q r s t u [x] z*), six letter-pair symbols standing for consonants, a dozen two-figure
syllables and particles in the ranges 01–09 and 40–50, the letters *a* and *m* as nulls, and thirteen three-figure
groups that are word codes. Every spelled word reads; three of the small groups and the ten word codes are glossed
from context, not read. The letter asks its addressee to make good a promised canonry of Olmütz for one of the
sons of "this Most Serene [Queen]", i.e. of the Polish royal couple.\*

Session 2026-09-16. Ciphertext is Tomokiyo's transcription in [variable2.htm](http://cryptiana.web.fc2.com/code/variable2.htm)
("the numbers and letters are written without space in the original manuscript, but I believe my grouping into
two- or three-digit groups is fairly straightforward"). DECODE's public record: one page, *Non-decrypted*, cipher
type *Simple substitution, Homophonic substitution*, dates 1600–1799 placeholder, inline cleartext yes, transcription
exists, images and documents behind login. Not seen. The TARGETS.md note called the letter pairs "syllables or nulls";
they are neither.

## 1. The ciphertext

[ct.txt](ct.txt): 509 tokens as Tomokiyo splits them; after joining his suggested pairs (ll zg fi pr lu th) 442
tokens: 295 two-figure groups (36 distinct), 13 three-figure groups (100 113 120 123 151 154 157 159 160 223),
56 *m*, 52 *a*, 7 ll, 5 zg, 4 fi, 3 lu, 2 pr, 2 th, and single *o*, *p*, *n*.

What gave the structure away before any solving:

- The figures 12–33 (30 absent) carry 265 of the 308 numeric tokens, and their frequency profile (29 and 16 at 35,
  21 at 29, 13 at 27, then 18, 17, 17, 15, 13, 10, 9, 9, 7, 7, 5, 4, 4, 2, 2, 1, 1) is monoalphabetic Italian
  (*e a i o* ≈ 30 each, *n l r t s c d* 10–18). IC of the numbers 0.058, dragged down by the rare groups.
- 01–09 (14 tokens) and 40–50 (15 tokens) are too rare to be letters and too even to be homophones of vowels.
- *a* and *m* are a quarter of all tokens. Treated as symbols, both anneal to the same vowel (run
  [solve2.py](solve2.py) `withletters`), which no Italian text allows, so they carry no letters. They fall mostly at
  word ends (see the marked decode below), which is the usual clerk's habit of dropping a null after each word.

## 2. Solving

1. **5-gram annealing on the numbers alone** ([solve.py](solve.py), Italian 5-gram model from `../lucca/it5.npy`,
   nulls dropped, text split at the three-figure codes): six seeds, no agreement, but seed 3 (−2.48 per 5-gram)
   already had *avere*, *questa*, *un caricato*, *aiuto*, *subito*, *bene*. Forcing distinct letters on the 19 core
   figures ([solve2.py](solve2.py)) did not help: at 253 5-grams the LM prefers *e t r s* soup.
2. **A unigram word-segmentation scorer** ([wordsolve.py](wordsolve.py)) degenerates into strings of *di la il*
   and also had a bug (swaps let core figures share a letter). Void.
3. **5-gram + dictionary coverage** ([combo.py](combo.py): LM score plus one nat per letter covered by a lexicon
   word of three letters or more, swaps only inside the core, free letters for the rare groups). From random keys,
   seeds 0 and 2 of six converge on the same key at −371 / −409; seeded from step 1's key, all three seeds land on
   it (−371, −374, −387). Reading at that point: *… un caricato d olmi. ad uno gli … suoi figlio hauendo io saputo
   in corte … uolonta di re … stata messa in esecutione … queste maesta ho stimato oficio … uoto seruitore io le so
   non suplicare … a uoler fare … prima … subito a me benigna risposta*.
4. **Controls.** The same objective annealed on three shufflings of the ciphertext tops out at −843, −865, −893
   against −371 on the real order.
5. **The alphabet is in order.** The converged core key is 13 a, 15 b, 17 c, 19 d, 21 e, 23 f, 25 g, 27 h, 29 i,
   31 l, 33 m on the odd figures and 14 n, 16 o, 18 p, 20 q, 22 r, 24 s, 26 t, 28 u on the even ones, which the
   annealer cannot have known. It fixes the two hapax figures as well: 32 = z (even series … u x z) and 12 as a
   symbol outside the alphabet.
6. **Rare groups and letter pairs by context** (every occurrence listed by the script in the session; the readings
   below are the only ones that fit all occurrences of each symbol):
   - zg = r (*rico·rdo*, *Nicolspu·rg*, *Se·renissima*, *confe·rire*, *servito·re*); lu = d (*ricor·do*, *a·d uno*,
     *desi·derano*); fi = n (*ho·nori*, *inte·ntione*, *i·n* ×2); ll = t (*al·tri*, *in·tentione*, *tal*, *sta·ta*,
     *ques·te*, *stma·to*, *servi·tore*); th = l (*Nico·lspurg*, *ta·l*); pr = ff (*ffece*, *e·ffetuare*).
   - 01 si (*Serenis·sima*, *de·siderano*, *si degni*, *si [154]*); 05 non (*ca·non·icato*, *non è*); 06 ne
     (*intentio·ne*, *essecutio·ne*, *dar·ne*); 09 de (*de voler*, *de devoto*); 40 con (*con·fido*); 46 con
     (*con·ferire*); 41 al (*al·tri*); 42 la (*supplicar·la*); 43 di (*di supplicarla*); 44 de (*de li suoi figli*);
     45 da (*da·to*, *dar·ne*); 47 che (×3, all at clause openings); 50 se (*se·renissima*, *es·se·cutione*,
     *se·rvitore*).
   - Single *o*, *p*, *n* (one each) fall inside otherwise complete words (*che {12} o mi fece*, *hauer p dato*,
     *figli n*) and are read as nulls or transcription slips.

## 3. The reading

[plaintext.txt](plaintext.txt); [decode.py](decode.py) regenerates it (`-n` marks the nulls, `-g` glosses the codes).

> Mi ricordo che, fra li altri honori che {12} mi fece in Nicolspurg, mi confido d'hauer dato intentione a questa
> Serenissima [100] [113] de uoler conferire un canonicato d'Olmiz ad uno de li [123] suoi figli; hauendo io {03}
> saputo in [160] corte che tal uolontà di [120] non è [151] stata messa in essecutione, sì [154] desiderano [157]
> queste Maestà, ho stimato oficio de deuoto seruitore, [154] io le sono, di suplicarla, [154] fo, a uoler far
> effetuare [160] [223] [159], prima {04} si degni darne subito a me benigna risposta.

Spellings as enciphered: *Seerenissima* (a doubled 21 or a slip for *Serenissima*), *stmato* (no *i*), *ffece*,
*oficio*, *suplicarla*, *effetuare*, *essecutione*, *Olmiz*, *Nicolspurg*. Single consonants and *essecutione* are
ordinary for 1627; the first two need the image.

Glosses (inference, not reading): [154] ×3 = *come* (fits *sì come desiderano*, *come io le sono*, *come fo*);
[160] ×2 = *questa* (*in questa corte*, *effettuare questa …*); [151] = *ancora*; [120] = the addressee's title;
[100] [113] = the Queen's title; [123] = *Serenissimi*; {12} = an honorific subject (*V.S.*); {03}, {04}, [157],
[223] [159] open.

## 4. What it says\*

Nikolsburg (Mikulov) was the seat of Cardinal Franz von Dietrichstein, Bishop of Olmütz 1599–1636, in whose gift
a canonry of Olmütz lay; the writer had been received there and had then told "this Most Serene [Queen]" in Warsaw
that the Cardinal meant to give one of her sons an Olmütz canonry. The Queen of Poland in December 1627 was
Constance of Austria, Ferdinand II's sister, whose younger sons (John Albert, Charles Ferdinand) were being placed
in church benefices in exactly these years. The letter, written from Warsaw to the Cardinal on 24 December 1627,
says the promise has not yet been carried out, that "these Majesties" (Sigismund III and Constance) want it, and
asks either that it be done or that he be given a prompt answer. The addressee is therefore Dietrichstein and not
the Emperor,\* which would explain why the piece sits in the Chiffrenschlüssel series rather than in a
correspondence. The writer is not named in the cipher; an Italian-writing agent moving between Nikolsburg and
Warsaw in 1627 is the profile.\*

\* Inference from the text and general history; nothing in the record names sender or addressee. The DECODE
cleartext frame (login) or the Dietrichstein papers would confirm it.

## 5. What remains

- The image, for *Seerenissima*, *stmato*, the three stray single letters, and any cleartext beyond the dateline.
- The ten word codes and {03} {04} {12}: a second letter in the same key, or the key itself (Kt. 14 Fasc. 20 is a
  key fascicle), would fix them.
- R2179 from the same article (undelimited digits) is a different system and untouched.

## Files

- [ct.txt](ct.txt) — Tomokiyo's transcription, 509 tokens as he splits them.
- [solve.py](solve.py), [solve2.py](solve2.py) — 5-gram annealers (numbers only; with distinct core; with *a m* as symbols).
- [wordsolve.py](wordsolve.py) — lexicon loader and the word-segmentation scorer (the standalone solver in it is the failed step 2).
- [combo.py](combo.py) — the 5-gram + coverage annealer that converged; `key_combo_seeded.json`, `key_combo_rand.json`, `key_seed3.json` its outputs.
- [decode.py](decode.py) — final key, writes the plaintext; [plaintext.txt](plaintext.txt).
- Corpus and 5-gram table are `../lucca/corpus` and `../lucca/it5.npy` (not committed there either).

Checked: token counts, convergence from random and seeded starts, three shuffled controls, alphabet order, every
occurrence of every rare symbol against its reading, word-level Italian throughout. Not checked: the manuscript
image, sender, addressee, the word codes. User must verify: §4 before it is repeated anywhere; DECODE registration
and any note to Tomokiyo are Daniel's steps.
