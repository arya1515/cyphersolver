# Duke of Sessa (Luis Fernández de Córdoba) → Charles V, Rome, 18 April 1524 — RAH Salazar A-31 (9/31) ff. 128–131

DECODE R9877 (ff. 128–129) and R9878 (ff. 130–131), catalogued "Luis Fernández, Rome, April **1424**,
Non-decrypted, 4 pp. each". Picked on 2026-09-18 as the longest pre-1450 ciphertext (oldest/CANDIDATES.md A2).

## 1. Not 1424: it is 1524, and not a blind break

- **DECODE's date is a typo.** The same series runs on as R9888–R9895 "1524"; the senders are Luis Fernández de
  Córdoba, 2nd **Duke of Sessa**, imperial ambassador at Rome 1522–26, and Lope Hurtado de Mendoza (1499–1558);
  RAH 9/31 is **Colección Salazar y Castro A-31**, which Bergenroth calendars in *CSP Spain* vol. 2 for April–May
  1524 ("M. Re. Ac. d. Hist. Salazar. A. 31. f. …"). The target itself is dated on f. 128v: **"De Roma xviij de
  Abril 1524"**. R9878 (ff. 130–131) is the duplicate of the same letter, sent by a second courier (both copies
  end "Al visorrey escrivo en el mismo punto"). Bergenroth skipped this letter (he has only Lope Hurtado's of the
  same day, no. 642, from the A-33 abstracts).
- **Sibling letters in the same cipher carry contemporary decipherments** ("Decrypted" in DECODE): f. 138 with
  its clear on f. 140 (17 Apr, CSP 639), ff. 170–171 with clear on f. 172 (22 Apr, CSP 643), ff. 322–323 with
  clear on f. 324 (19 May, CSP 651). The decipherer is the court's (Pedro de Soria, per Bergenroth's vol. 3
  introduction). So the route is key-from-sibling, the project's standard one.

| CSP no. | date | letter | Salazar A. 31 | DECODE |
|---|---|---|---|---|
| 633/635 | 13 Apr | Lope Hurtado → Emperor / → Gattinara | ff. 61–67 | R9871, R9872 Decrypted |
| 637 | 14 Apr | Sessa → Emperor (Goicoechea's 19th-c. reading) | f. 79 | R9873 ff. 79–86 |
| 639 | 17 Apr | Sessa → Emperor | ff. 138–140 | R9881 **Decrypted** |
| — | **18 Apr** | **Sessa → Emperor, this letter + duplicate** | **ff. 128–131** | **R9877, R9878** |
| 643 | 22 Apr | Sessa → Emperor | ff. 163–172 | R9883, R9884 **Decrypted** |
| 651 | 19 May | Sessa → Emperor | ff. 320–324 | R9890 **Decrypted** |

## 2. The cipher (Sessa–Charles V, Rome, 1524)

Mixed nomenclator in a rounded chancery hand: three-letter code groups for words and syllables (`gap` que, `sof`
de, `mus` la, `dim` se…), single letters and signs for spelling (`α` a, `ott` t, `4` o, `#` g, `nf` p, `ꝑo` the
plural -s suffix), `f~` as the clear/cipher switch and clause mark, `v db` as a null opener of each cipher
paragraph. Working key with evidence: [key_working.md](key_working.md). Cipher/clear pairs:
[pairs_f170.txt](pairs_f170.txt), [cipher_f138.txt](cipher_f138.txt) against [clear_f140.txt](clear_f140.txt),
[clear_f172.txt](clear_f172.txt), [clear_f324.txt](clear_f324.txt).

Secure code values (each aligned in at least one sibling): que `gap`, de `sof`, del/de l- `suf`, la `mus`, las
`mus ꝑo`, el `qib`, lo `kef`, no `ler`/`lex`, se `dim`, le/les `ka`, y `q+`, he `ma`, en `qid`, su Santidad `coh`,
rey `fad`, paz `Jep`, tregua `bob`, Francia `po3`, Inglaterra `mef`, suyços `cum`, arçobispo de Capua `yom`,
persona `lax`, platica `tud`, muy `log`, con `tat`/`tar`, mal `kch`, esta `qet`, sabe `dog`, sabia `dug`, mas `kah`,
scrito `pur`, muestra `luf`, ni `lep`, otra `lum`, parte `lux`, uno `baq`, otro `Jom`, por `hef`, forma `put`,
ningun- `lip`, franceses `qes`, ha `mn`, os `Jim`, di `g3`, do `ram`, si `cob`, t `ott`, ca `ttt α`.

## 3. Reading of ff. 128–131 (2026-09-18, in part; eight passes, see key_working.md)

Clear opening (f. 128r): *Teniendo escripto y cerrado el pliego del duplicado de xiiij deste que sera con esta, vi
una letra del obispo Verulano que esta en Constancia, de que aqui embio copia. Luego embie a Su Santidad a
suplicalle me mandase avisar de alguna particularidad para dar noticia della do conviniese. Mandome a mi Felice su
secretario, el qual me ha dicho que las letras que tiene son del dicho Verulano de vj y vij del presente, do dize
que hera acabada la dieta, y que Lucerna no concluyo de dar ayuda a franceses; que los cantones de Berna y Friburk
y Solodor, y para mas facilitarla y traer los animos del pueblo, publican que los suyços en Lombardia estavan
cercados y en grand peligro, con que juntava hasta el numero de ocho mill, que davan nombre de partir muy presto,
pero que el no podia saber el quando, por estar en Costancia donde algunos de sus amigos de Suyça le escrivian para
que exortase a Sus. que buscase alguna buena forma de paz. Esto es lo que me ha referido.*

Cipher (eight lines on f. 128r, one on f. 128v; the duplicate ff. 130–131 is token-for-token the same). Method:
every line cut into tokens by `tokens.py` (sheets in `tok/`, one PNG per token in `tok/*_tiles/`), the same done
for the deciphered siblings f. 138, ff. 168v, 170–171 and 322, and values assigned by aligning those against
their clears (f. 140, f. 172, f. 324). Transcription: [transcription_f128.txt](transcription_f128.txt).

> ¶ las dichas [vo]s no le las mostraron, que le ponen sospecha que desea aver algo que r-e-f-i-e-r-a de lo suso
> [ruc] [hay] no / **me parece que concuerda mucho con lo primero y postrero que el dicho obispo dize al maestro de
> postas** / hablé en la ora a Su Santidad a **pedirle que haya provisión** de [pa]-r-a los casos de suyços,
> persuadiéndole los m-re que r-ido los que no m-r-e-van / **pues tiene color para ello, aviendo començado** la
> plática de la paz y tregua r-[…] **entender lo que mas podré. Al visorrey escrivo en el mismo punto.**

Sense: Felice will not show Sessa the bishop's own letters, since they make him suspect that Sessa wants to get
something out of them for himself; Sessa nonetheless finds the report consistent with what the bishop writes to
the postmaster (Gabriel de Tassis: his Italian letter of 6 April, *tutti Elvetij son in arme … expedisca volando a
Milano et Roma*, is bound as f. 131); he went at once to the Pope to ask for a provision of money for the Swiss
business, persuading him that he has the colour (pretext) for it, having opened the peace-and-truce negotiation.
This is the news Bergenroth abstracts from the 22 April letter (CSP 643).

Pass 10 (the January 1525 letter R9897, same cipher, verbose clear on ff. 14v–15; fetched with the saved DECODE
cookie) attested `rad` = *dicha*, `boy`/`bez` = *-ido*, `Є` = *h*, `kel` = `kef` (*los*), and `lif 3` = *quiere*
(key_working.md, pass 10). Unread now: `vo` (the noun after *dichas*: the bishop's letters or their copies),
`z y` (the verb after *quiere*, *mostrar* from the sense), `per`, `rus`, `hay`, and the clause *los m-re que r-ido
los que no m-r-e-van*, where one sign value (probably `v`) is still wrong. The other 1525 letter, R9898 (14 pp.),
was then read through as well (pass 12): it carries no decipherment despite DECODE's "Decrypted", so it gave only
contexts (`z y` also after *si*; `ruc`/`rus` is a person who *ha respondido*; `hud` again in *la plática de la paz*).
Pass 13 (the 24 July 1524 letter R9893, cipher f. 483 with its clear on f. 485) corrected `lif` to *mostrar*
(*ni se quiere mostrar* = `lep dim fa lif 3 α`, `fa` = *quiere*) and gave `zum` = *hay*, `tas` *cosa*, `luh`
*mundo*, `qit` *estado*, `lic` *monsieur*, `gel` *qual*. Open now: `vo`, `z y` (after *mostrar*; also after
*si* in 1525; probably a conjunction, *porque* or *diziendo*), `per`, `rus`/`ruc` (a person), and the clause
*los m-re que r-ido*.

Pass 14 matched templates of the unread tokens against every downloaded page (`tmatch.py`). The September 1523
letter R9834, whose cipher faces its clear on f. 38, gives `z y` = *-on* (*dilataron*, *concedieron*), so the first
sentence reads *las dichas [vo]s no le las mostraron*. `ruc` and `hay` occur only in the 14 April 1524 letter R9873,
which has no decipherment; `vo` and `per` match nowhere. Those four are the residue.

The seven 1523 Sessa letters DECODE marks "Decrypted" (R9676, R9691, R9693, R9781, R9834, R9836, R9841; about 50
pages, fetched into `img/` with the cookie) use **the same cipher** (`sof`, `gap`, `ram`, `bas`, `qes`, `lex`, `cih`
all recur; R9781's August 1523 cipher block has its clear on f. 651). They are the remaining source for the four
open groups; aligning them is the same token-sheet work as passes 1–13. Pass 11 (the rest of
R9897, ff. 10–13v, against ff. 14v–15) confirmed `hud` = *plática*, `rad` = *dicha*, and added *larga*, *fue*,
*esto*, *tiempo*, *para*, *después*, *llegar*, *miento*, but none of the five (key_working.md, pass 11).

## 4. Images

DECODE images (RAH material, not public domain) are git-ignored in `img/`; only the public 200-px thumbnails and
the record pages are in `decode/`. Filesrv names: IMG_R9877_I46030_P1/P2, IMG_R9878_I46033_P1/P2,
IMG_R9881_I46038_P1/P2, IMG_R9884_I46049_P1–P4, IMG_R9890_I46073_P1–P3 (P4 not yet fetched), plus the neighbours
in section 1. Daniel downloads them logged in and drops them in `img/`.

To attest the nine open groups, the next deciphered Sessa letters (same correspondent, a year later, "Decrypted",
14 pp. each) are the ones to fetch, logged in, into `img/`:
- https://de-crypt.org/decrypt-custom/filesrv/?file=IMG_R9897_I46110_P1.jpg … `_P7.jpg` (9/34 ff. 10–16, 1525)
- https://de-crypt.org/decrypt-custom/filesrv/?file=IMG_R9898_I46118_P1.jpg … `_P7.jpg` (9/34 ff. 150–156, 1525)
Then `python tokens.py <img> x0 y0 x1 y1 tok/<name>.png` per cipher line and search the tile sheets for `rad`,
`vo`, `lif`, `per`, `kel`, `boy`, `rus`, `hay`.
