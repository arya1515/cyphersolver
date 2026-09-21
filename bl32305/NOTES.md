# BL Add MS 32305: Paris 1719 and "Carré" 1742–45 code letters (catalogue #78)

Status: attempted, open. Worked 21 Sept 2026.

## The volume

BL Add MS 32305 is catalogued as 39 folios of "unidentified cipher keys". The DECODE records R2963–R2981 show that it is a
codebreaker's working file of intercepted letters, most of them deciphered between the lines at the time. Catalogue
entry #78 grouped six records (R2963, R2964, R2965, R2968, R2972, R2974) under "Unknown sender (Paris)". They are not one
correspondence. All nineteen records R2963–R2981 were viewed (R2975–R2981 on 21 Sept, key hunt) (images via the DECODE cookie, git-ignored in `img/`):

| Record | Folio | What it is | State |
|---|---|---|---|
| R2963 | f. 5 | German letter to a "Marquis", 28 Jan [1719?], figures for names and words (1203 = London, 1439 = Theophili…) | deciphered interlinear at the time: **read** |
| R2964 | f. 6 | "A Mr [struck out]", Paris 7 Feb 1719, *Extrait*, French, clear with a 3-figure code | **open**: ~a dozen values glossed |
| R2965 | f. 7 | Paris 10 Feb 1719, *Extrait*, same code, same writer ("Vos Parens", "votre Cousin") | **open**: same glosses |
| R2966 | f. 8 | French letter, 2-figure letter cipher (20 = a, 97 = s…) | deciphered interlinear: read (not in #78) |
| R2967 | f. 10 | London 4 and 11 July 1740, French, a few code groups (0813 = le Sr Walpole) | glossed: read (not in #78) |
| R2968 | ff. 11–12 | "Anonyme à Monsr Carré en Pellmall à Londres", March 1742, all figures (3-figure, ≤ ~800) | **attempted, closed**: transcribed, two-part code, nothing glossed |
| R2969 | f. 13 | "Carré 1742": a frequency count of R2968 + R2970's groups (686 ×20, 212 ×19…; tentative 686/106 = de, 121 = la) | not a key |
| R2970 | ff. 14–17 | "Copie d'une Lettre en Chiffre, sans date", to Mr Carré, Palmal, under cover to Mr Chevening(?), jeweller near Charing Cross; same code as R2968; endorsed "R Aug. 22 1742" | **attempted, closed**: two-part code, transcribed (merged into #78) |
| R2971 | ff. 18–21 | French, 4-figure code (≤ ~4600), Queen of Hungary; pencil "Carré 1742" | deciphered interlinear: read (not in #78) |
| R2972 | ff. 22–23 | "Lond. 19 Janv. 1745", all figures, same code as R2968 (212, 771, 283, 606…) | **attempted, closed**: transcribed |
| R2973 | f. 24 | 6 March 1749, Vienna/Petersburg accession, code groups | glossed: read (not in #78) |
| R2974 | ff. 25–28 | "L. 17/28 Nov. 1749", 2-figure letter cipher | deciphered letter by letter: **read** |
| R2975–R2978 | ff. 29–33 | Dec 1749 – Jan 1750 (some Dresden), French, 2-figure letter cipher | deciphered interlinear: read (R2978 = #79) |
| R2979 | f. 34 | Hague 9 Aug 1753, "Hanau to Fer.", 4-figure code in a clear letter | decipherer's working copy, glossed in part: read in part at the time (#79) |
| R2980 | ff. 35–36 | "A Mr de H.", London 8–12 Dec 1758, continuous 2-digit cipher | deciphered: read (not in #78) |
| R2981 | ff. 37–39 | L. 12/23 Jan 1759, 2-figure letter cipher | deciphered: read (not in #78) |

So of the six catalogued items, R2963 and R2974 were read at the time, and R2964, R2965, R2968 and R2972 are open.

## The Paris 1719 code (R2964, R2965)

A letter from Paris, written a few days after Lord Stair's formal entry (5 Feb 1719 NS), to a correspondent in England
who is told he will stay there "jusqu'au retour de S. M. Brit." The tone ("vos Parens", "votre Cousin", "le caractère des
esprits de votre Famille") is that of a cover vocabulary, probably Jacobite or Spanish-side (Alberoni is named).
`R2964_transcription.txt` gives the whole of f. 6: **354 figure groups, 191 distinct, 116 seen once, highest 900.**
The decipherer's glosses (both letters): 36 = re, 88 = pas, 95 = le, 184 = que, 243 = vous, 347 = a, 531 = pour,
652 = qu'il, 786 = s; crosses mark 27, 258, 285, 611 as persons.

The glosses are not in alphabetical order (re 36 < pas 88 < le 95 < que 184 < vous 243 < a 347), so this is a two-part
code, and its order cannot be used. With about 700 groups in the two letters for a code of about 900 entries, most
values occur once. A ciphertext-only break is not feasible from this material; the decipherer of the time stopped at the
same place. What would move it: the key, a clear copy, or more letters in the same code elsewhere in the BL/SP 107 files.

## The Carré code (R2968, R2970, R2972)

Attacked 21 Sept 2026 (work first done in a separate `r2970/` folder, merged here). **Attempted, closed**: a two-part code of about 800 three-figure groups with word-level entries; not breakable ciphertext-only from the three surviving letters.

### The documents

Three letters in one code, all in BL Add MS 32305 :

| Record | Folio | Heading | Groups | Distinct | Max |
|---|---|---|---|---|---|
| R2968 | ff. 11–12 | "Anonyme à Monsr Carré en Pellmall à Londres", Mars 1742, ΔΔΔ | 372 | 208 | 796 |
| R2970 | ff. 14–17 | "Copie d'une Lettre en Chiffre, sans date, et adressée avec ces caractères ΔΔΔ à Mr Carré en Palmal Lond. sous un couvert adressé à Mr Chevening(?), Marchand Joailier près Charing Cross"; signed "Anonyme"; endorsed "R Aug. 22 1742" | 470 | 219 | 800 |
| R2972 | ff. 22–23 | "Lond. 19 Janv. 1745" | 481 | 196 | 796 |
| all | | | 1323 | 381 | 800 |

R2969 (f. 13, "Carré 1742") is the decipherer's frequency count. Transcriptions (all in `carre/`): `transcription_R2968.txt`,
`transcription_R2970.txt`, `transcription_R2972.txt` (one line per MS line, page markers, `_` = underlined,
`?` = doubtful). Parser: `carre/parse.py`. Images are not committed (fetched with the DECODE cookie).

Notes on the copies: all three are fair copies made by the intercepting office, sheet-lettered (A–E, a–d, e–h) with
catchwords. R2968 f. 12r repeats a line (`156 106 514 512 539 279 231 686`) and brackets the first copy: a
copyist's dittography. R2972 has a later hand's underlining of repeated runs (`95 57 606 451`, `212 621 675 195`,
`9 440 144 299 86 600 707`) and faint pencil letters under a few groups (h, r?, d?, b?/e?): a decipherer's
tentative guesses, not a reading. R2970 was received 22 Aug 1742, so it is later than R2968 (March 1742).

**Check against R2969.** R2969's tallies are of R2968 + R2970 together (the two 1742 letters), counting the
bracketed dittography. With that line included my transcription gives exactly R2969's figure for 686 (20), 212 (19),
106 (18), 121 (14), 12 (14), 707 (12), 781 (11), 539 (10), 621 (10), 518, 330, 610 (9), 66, 232 (8), 44, 98, 231,
283, 476, 551, 611, 771 (7); it differs by one for 573 (12 v 11), 27 (9 v 8, one doubtful 27 at a page edge),
772 (7 v 8). R2969's second column lists 610 with 19, apparently a slip. So the transcription is sound to about one
group in 300.

### Statistics

- 1323 groups, 381 distinct, 147 seen once; values 1–800 (one 800, none above). Each hundred has 36–62 distinct
  values: the whole range 1–800 is in use. Flat profile: the top value (212) is 2.3 % of the text, then 12, 106, 686
  (1.8–2.0 %), 707, 66, 121, 283, 621, 75.
- No separators, no nulls detectable: groups are separated by points (R2968, R2972) or spaces (R2970) only.
- Repeats are short: 94 repeated bigrams, 24 trigrams, 8 four-grams, one five-gram (`151 521 330 621 212`, in
  R2968 and R2970); `95 57 606 451` ×3 and `75 95 57 606` in 1745 (a name or title spelled in groups, underlined).
- The 1742 and 1745 letters share the code: 73 % of the 1745 tokens use a value seen in 1742 (68 % of R2970's use a
  value seen in R2968), and the top values recur (12, 212, 106, 66, 283).
- Underlined single groups (R2970: 73, 218, 349, 7, 211, 587, 204, 319, 307, 785, 328, 80, 143, 135, 685, 383,
  235; R2968: 356, 196, 365, 135, 549, 631, 204, 785, 287, 585, 80) are the intercepting clerk's marks, probably for
  proper names; 135, 204, 785, 80 are underlined in both 1742 letters.

### What the system is

1. **Not a letter-level homophonic cipher.** Annealing a letter-per-group assignment against the French 4-gram model
   (`carre/anneal_letters.py`, `lang` model `fr-modern`) reaches −2.09/−2.11 per char on the real text and −2.12/−2.17 on
   the same groups in shuffled order: no difference, and the output is gibberish (`carre/anneal_letters.out`). With 381
   types for 1323 tokens a letter homophonic would be overfitted anyway; the type/token ratio and the Zipf-like
   profile are those of a word code.
2. **Not a one-part code.** In a one-part French code, le/la/les (l-), que/qui (q-), et/en (e-) would pile the token
   mass into their alphabetical bands. `carre/onepart_test.py` compares the observed token mass per 50-value bin with what an
   alphabetical list of the 700 commonest French words (fr-gutenberg) predicts: Pearson r = −0.26. Placing the top 30
   values at their proportional alphabetical positions scores worse than random values (86 % of 2000 random
   placements do as well). The contemporary tentative identification (686/106 = de, 121 = la) also assigns
   non-adjacent values to de.
3. **So: a two-part code** of about 800 entries (words, and presumably syllables/letters for spelling names such as
   the underlined 1745 run), the same type as the Paris 1719 code in this volume, whose glosses prove two-part order.

Language: French is assumed from the headings (French clerk's heading, "Anonyme", the writer's ΔΔΔ address mark);
nothing in the figures confirms it.

### Is it breakable?

Not ciphertext-only. 1323 tokens for an ~800-entry random-order code give at most a handful of reliable
identifications (the few frequent function words) and no way to verify them; the decipherer of the time stopped at
the same place (R2969, pencil guesses on R2972). No crib is available: the letters are undated/anonymous and the
contents unknown; a guessed crib (Walpole, Carteret, the Pragmatic Army, the Pretender) cannot be placed without a
known sequence, and the only repeated long run (`95 57 606 451`) is too short to test a name against.

What would break it:
- the key itself, or another letter in the code with an interlinear decipherment. Places to look: the rest of BL Add
  MS 32305 and neighbouring codebreaker volumes (Add MS 32258–32310, the Newcastle/Secret Office papers), SP 107
  (intercepted letters), SP 36 1742 (Carré as an addressee), and the Secret Office decipherers' letter-books
  (Willes family) for "Carré" or "Carre, Pall Mall";
- a clear copy or summary of any of the three letters (e.g. in the Newcastle papers, Add MS 32699–32700 for Aug 1742);
- the identity of Carré and of "Chevening" the jeweller, which would suggest names for the underlined groups and a
  crib for the opening (R2970 and R2968 both open without a salutation run in common).

### Log

- 21 Sept 2026: fetched R2968, R2969, R2972 images (R2970 already in `decode/`); transcribed the three letters from
  the full-resolution images; checked against R2969; statistics; letter-homophonic anneal + shuffled control
  (no signal); one-part test (no signal). Conclusion above.

### Key hunt (21 Sept 2026): negative

- **R2975–R2981** (the rest of the volume; R2982 on is Add MS 4136): all 1749–59, letter ciphers or 4-figure codes, deciphered. None in the Carré code; no key, table or clear copy.
- **R2971** (pencil "Carré 1742"): a French despatch from London to "V.A.S." (a prince), 1742, 4-figure syllabic code deciphered interlinear (448 = de, 745 = que, 693 = les, 4209 = la). Not to Carré, not the same code: 448 and 745 never occur in the 1323 Carré groups. The pencil heading is an archivist's.
- **R2972's marks under groups** ("h", "e", "r?/d?", "b?") are the decipherer's cross-references to the sheet (e–h) where the same run recurs (`9 440` → h, `95 57 606 451` on f → e and on e → f, `600 707` → g), not plaintext guesses. R2972 carries no decipherment.
- **Web search** (Carré Pall Mall 1742 cipher/Jacobite; "Add MS 32305"; Mr Carré 1742–45; the jeweller "Chevening"): nothing.
- Still to try, offline: the Willes decipherers' letter-books, Newcastle papers Add MS 32699–32700 (Aug 1742, Jan 1745), SP 36 / SP 107 for "Carré, Pall Mall".

## Prior art

Checked: the BL catalogue description (unidentified cipher keys) and a web search for the shelfmark; no edition or
study of these letters found. DECODE has no transcription files for any of the records.

## Catalogue #79: R2978 and R2979 (checked 21 Sept 2026)

The rule scorer made "Unknown sender (Dresden) to unknown recipient, 2 ciphertexts, 25 Jan 1750 – 9 Aug 1753" out of
the last two records of the file. Both were viewed at full resolution. They are two unrelated items, and neither is open:

- **R2978, f. 32 (4 pp.)**, "Dresde 25. Janv. 1750", French, a 2-figure letter cipher (e.g. 93 = s, 24 = t, 54 = d,
  12 = n). The contemporary decipherer wrote the plaintext letter by letter over every line ("…que l'on ignore pas les
  dangers auxquels notre position nous expose… les insinuations de Mr de Guydickens…"). Read at the time.
- **R2979, f. 34 (2 pp.)**, "Hanau to Fer.", "Hague, 9 Aout 1753". This is not the intercepted letter itself. It is the
  decipherer's working copy: the clear syllables written out, the unread 4-figure groups (up to about 3300) left as
  figures, with glosses over the groups he had worked out (1688 = si in "con-si-derable", 3227 = Devonshire, 1560 = roi,
  1808 = Lor…). The second page ends "Ici on parle du mariage de 3245 avec 3263" and a column of question marks. Read in
  part at the time. The code is syllabic and word-level; from one working sheet, most of the unglossed groups occur once,
  so no new reading was attempted.

Catalogue #79 was removed as read at the time.
