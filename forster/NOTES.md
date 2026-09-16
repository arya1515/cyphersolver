# Sir Richard Forster, 13 May 1644 (Archives départementales du Val-d'Oise, 68.H.8, 3e liasse) — NOTES

**Verdict: already READ by others; alphabet verified here.** The passage was deciphered by George Lasry after
Britland's 2013 article appeared, independently by Norbert Biermann, and again in September 2026 by Robert Pitt,
whose key is public (GitHub `robertpitt/forster-cipher`, commit 0817cd5, 14 Sept 2026; Lasry and Biermann credited
in commit af9d1fb, 15 Sept 2026, on Britland's information). Tomokiyo's unsolved page (last modified 6 Sept 2026)
still lists it as unsolved. What is added here: a permutation control on Pitt's key, and a blind recovery of the
alphabet from the ciphertext alone, with matched controls, which also explains why the first n-gram attempt fails.
Nothing about the *text* is new here.

Session 2026-09-16. Not first, and no claim to be.

## 1. The target as it really is

The tracker row said "134 groups, 24 symbols" and predicted a regular Stuart key like Ormonde's or Boswell's. Both
were wrong. Tomokiyo's transcription (blog, 21 Sept 2021, [src/blog.txt](src/blog.txt); identical token for token
to Pitt's input) has **207 cipher tokens in 37 comma-separated groups, 34 distinct symbols** (18 numbers, 16
letters), 8 hapax, IC 0.047, plus two clear French passages and the date. The commas are word (or word-pair)
boundaries, which is what makes it tractable.

| | |
|---|---|
| numbers | 0 2 4 5 7 8 12 14 16 19 20 30 40 50 70 80 88 90 |
| letters | a b c d e f g l n p q s t u x y |
| commonest | 30 ×24, 2 ×18, 0 ×18, 20 ×13, x ×10, c ×9, s ×9 |

**Not a regular key.** Under the reading, cipher letters map a:d b:t c:l d:i e:g f:b g:y l:r n:f p:a q:c s:o t:n
u:m x:s y:p, and numbers 0:e 2:e 4:a 5:g 7:d 8:t 12:c 14:z 16:i 19:n 20:r 30:u 40:s 50:t 70:f 80:l 88:q 90:p. No
shift, no block, no odd/even row: it is a mixed alphabet with a second (and for t a third) symbol for the frequent
letters, e a c d f g i l n p r s t doubled, u single despite being the commonest letter. So the "first thing to
try" from Ormonde and Boswell does not apply; the family is closer to the Richelieu type of homophonic alphabet.
The unused values (1 3 6 9 10 11 13 15 17 18 60 100, and letters h i k m o r) presumably cover h k m o x and more
homophones in the full key.

## 2. Key and reading (Pitt; Lasry and Biermann earlier)

[key.py](key.py) applies Pitt's table ([src/pitt/recovered_key.json](src/pitt/recovered_key.json)) literally:

> il ny a aucun subiet descrupule de manquera dieu | ie vous en responds et mesmes dans | lesreigles de perfection
> prenez**sd**ulement lesuoyesde prudence p**i**ur con**c**eruer uotre uie pour enfaire a dieu un plus grand
> sacrifi**y**e parla multiplication des uos seruices pour lesalut de uos freres | et mesurer a cela sil est
> meilleur d'agir, ou de soupir 13. de may. 1644

"Il n'y a aucun sujet de scrupule de manquer à Dieu; je vous en réponds, et même dans les règles de perfection.
Prenez seulement les voies de prudence pour conserver votre vie, pour en faire à Dieu un plus grand sacrifice par
la multiplication de vos services pour le salut de vos frères, et mesurez à cela s'il est meilleur d'agir ou de
souffrir/subir." Spiritual counsel: preserve your life for further service. Whether it is *to* the Queen or a
copy of something sent to Forster is not decidable from the passage; Britland's abstract has Forster "then in
France" writing to an unknown correspondent, and gives the clear phrase as "de soubir" where Tomokiyo has
"soupir".

Four tokens conflict with the reading (bold above): `a`→d in *sdulement* (6 other occurrences want d), `16`→i in
*piur* (6 others want i), `q`→c in *conceruer* (3 others want c), `g`→y in *sacrifiye* (2 others want y). Each is a
single slip of the encipherer or of the typeset transcription (Britland's, not a photograph), the rate (4 in 207)
is like Boswell's, and no alternative assignment removes them without breaking the other occurrences. Britland's
correspondents read "aucune voie de scrupule" and "preveu seulement" where Pitt reads "aucun subiet" and "prenez";
the hapax `f` (b in *subiet*) and `14` (z in *prenez*) are the tokens at issue and cannot be settled from one
occurrence each.

## 3. Verification

### 3a. Permutation control on Pitt's key

[solve.py](solve.py), [solve2.py](solve2.py): the 20 plaintext-letter identities are permuted over Pitt's
homophone partition, 20,000 times, and the 207-letter decode scored with a French 5-gram model.

| model | Pitt key | null mean / sd / best | z | null ≥ real |
|---|---|---|---|---|
| letters only, `../sp53/corpus_fr.txt` (6.5 M letters) | −450.3 | −1327 / 117 / −960 | **7.5** | 0 / 20,000 |
| letters + word edges, `../chaulnes/corpus_fr.txt` (u for v, i for j) | −524.9 | −1768 / 142 / −1230 | **8.8** | 0 / 20,000 |

### 3b. Blind recovery, and what the controls say ([run1.txt](run1.txt) to [run4.txt](run4.txt))

A homophonic annealer (34 symbols → 26 letters, 150k steps, 8–12 restarts), first without and then with the
word boundaries, on the target and on six matched controls: held-out French of 207 letters enciphered with a random
key of exactly Pitt's homophone multiplicities (the control's letters ranked by frequency get 3, 2, 2, … symbols),
adjacent words merged with probability 0.2 as in the target (*descrupule*, *lesreigles*, *parla*).

| run | model | controls read (of 6) | target |
|---|---|---|---|
| 1 | 5-gram, letters only, no word edges | **0** (16–49% of letters right; the solver's optimum beats the truth on 5 of 6) | gibberish, 31% of Pitt's key |
| 2 | 5-gram with spaces, raw corpus | 3 (99.5–100%); 3 fall into an all-*i* attractor from OCR Roman numerals | attractor |
| 3 | same, Roman numerals and *ii* words removed | 5 (99–100%), 1 at 44% | −591.6 found vs −602.4 for Pitt: **a wrong key outscores the truth**, 14.5% agreement |
| 4 | same, training text with **v→u, j→i** | **6 of 6** (98–100%) | **97.6% of Pitt's key blind**: 202 of 207 tokens |

Run 1 is the Moray lesson at this length: 207 letters over 34 symbols with a plain letter-stream model is below
the solver's threshold even on controls, so nothing could have been read into a target failure. Run 3 is the more
useful lesson: the controls pass and the target fails, which means the *plaintext*, not the cipher, was out of the
model's distribution. The letter writes *u* for *v* (uotre, uie, uos, seruices, uoyes) and *i* for *j*
(subiet, ie), as every 1644 hand does; a model trained on a 19th-century edition with *v* and *j* scores that
spelling about 200 nats worse than modern French of the same length, and gibberish wins. Normalising the
training text fixes it, and the blind key then reads:

> il nu a aucun subiet descrupule de manquera dieu | lesreilles de perfection preneisdulement lesuouesde prudence
> piur conceruer uotre uie pour enfaire a dieu un plus grand sacrifiue parla multiplication des uos seruices pour
> lesalut de uos freres

The five disagreements are the three rare symbols whose value n-grams cannot fix and sense does: `g` (×3) read
*u* for *y* (ny, uoyes, sacrifiye), `14` (×1) *i* for *z* (prenez), `e` (×1) *l* for *g* (reigles). So 31 of 34
symbols are recovered from the ciphertext alone and the other three by the words; Pitt's alphabet is confirmed
independently of his work.

## 4. What stays open

- The manuscript. Britland's note 1 places the Forster papers at the Archives départementales du Val-d'Oise,
  MS 68.H.8, troisième liasse (the papers of the English Augustinian convent at Pontoise, where Forster's
  daughter was a nun*). No image is online; the four slips and the two hapax words (*subiet*/*voie*,
  *prenez*/*preveu*) need it, as does the question whether this passage is a whole letter or an extract.
- The recipient, and whether the same key appears in other Forster or Henrietta Maria papers of 1644.
- Reporting: Tomokiyo's page still says unsolved; Lasry, Biermann and Pitt have priority, and Pitt's repository
  is the public record. Nothing here should be reported as a new decipherment.

\* inference from the archive reference and the Pontoise convent's known Forster connexion; not verified.

## Files

| file | what |
|---|---|
| [ciphertext.txt](ciphertext.txt) | Tomokiyo's transcription, verbatim |
| [key.py](key.py) | tokenizer, groups, Pitt's key, literal decode |
| [ng5fr.py](ng5fr.py), [solve.py](solve.py) | letters-only French 5-gram; permutation test, blind annealer, 6 matched controls → [run1.txt](run1.txt) |
| [solve2.py](solve2.py) | word-edge model (27 symbols) with u/v, i/j normalisation; same tests → [run2.txt](run2.txt), [run3.txt](run3.txt), [run4.txt](run4.txt) |
| [src/blog.txt](src/blog.txt), [src/blog.html](src/blog.html) | the blog post, with the 2026 comment pointing to Pitt |
| [src/pitt/](src/pitt/) | Pitt's README, key, decoder and output (MIT) |

Model binaries (`ng5_*.npy`) are rebuilt by the scripts and not committed.
