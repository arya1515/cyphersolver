# Lope Hurtado de Mendoza (Rome) to Charles V, 1522 — RAH Salazar 9/26, DECODE R9634–R9656

Status: in progress (key being rebuilt from a contemporary decipherment; first values fixed)

Catalogue entry 144 ("Lope Hurtado de Mendoza (Rome) to unknown recipient, 8 ciphertexts",
RAH Signatura 9/26). Opened 2026-09-20, after the sanchez1522 session established that these letters
are **not** in Alonso Sánchez's cipher.

## Why this is a separate target

The nine Lope Hurtado records are bound in Salazar 9/26 among Sánchez's, were catalogued with them,
and look at first like more of the same: same months, same recipient, cipher mixed with clear inside
the sentence, code groups of the same shape. They are in a different cipher. Sánchez's codes end
strictly in `b c d f g h l m n`; Hurtado's take finals `p` and `z` (`tep`, `tap`, and groups ending
`-z`). See `../sanchez1522/NOTES.md`.

## Prior art: none

Tomokiyo's *Correspondence in Cipher of Imperial Ambassadors Alonso Sanchez and Juan Manuel (1522)*
(Cryptiana, 6 Sept 2025) reconstructs **Sánchez's** and **Juan Manuel's** ciphers. It does not mention
Lope Hurtado, and his records R9634–R9656 fall outside both ranges it lists. A web search for a
decipherment of his cipher returns nothing. **This key has not been published.**

## The records

| DECODE | 9/26 ff. | date 1522 | pp | DECODE status |
|---|---|---|---|---|
| R9634 | 14–16 | Sept | 6 | Non-decrypted |
| R9644 | 237–243 | 1 Nov | 14 | **Decrypted** |
| R9645 | 243–244 | Nov | 4 | Non-decrypted |
| R9646 | 252 | — | 2 | Non-decrypted |
| R9648 | 260–265 | 9 Nov | 12 | Non-decrypted |
| R9649 | 266–268 | 9 Nov | 6 | Non-decrypted |
| R9650 | 269–272 | — | 10 | **Decrypted** |
| R9652 | 295–296 | Nov | 2 | Partially decrypted |
| R9656 | 334–335 | Nov | 4 | Non-decrypted |

Images in `img/` (git-ignored; RAH material, fetched from DECODE 2026-09-20).

## The crib: R9644 carries its own decipherment

R9644 is the way in. The record holds **both** the ciphered letter (ff. 238–239) **and a full clear
version of it** (f. 242), the clear headed and closed with *Claro* section by section, and keyed to
the cipher by **marginal letters A, B, C** written against the matching passages on both.

So the attack is a straight crib: align the cipher against the clerk's own plaintext, token by token,
wherever the word counts match exactly.

## First values, fixed against the clear

The clear (f. 242) reads:

> … y que los que le tienen por frances veen si sus officios y fortalezas y servicio de su casa lo
> haze con franceses o castellanos. Su Sa[ntidad], a lo que yo pienso, espera lo que hara el
> arçobispo de Bari, y no gastar nada si ser pudiesse, porque esta tan escasso **que nunca hombre lo
> fue mas**; hasta que el arçobispo venga creo que sera mejor **no apretallo mucho**.

The cipher (f. 238) runs, with *hasta que el arçobispo venga creo que sera mejor* standing in the
clear on the cipher page itself:

```
… ton  tab    xud     xul  ɣm   xon  │ hasta q el arçobispo venga creo q sera mejor │ tu  ᵷʒ℔ʒ ʒ7 ∞ʒ ɸeɋ
    que nunca hombre  lo   fue  mas                                                    no  a-p-r-e-t-a-ll-o  mucho
```

Six tokens against six words, in a sentence with no room for slippage:

| code | value |
|---|---|
| `ton` | **que** |
| `tab` | **nunca** |
| `xud` | **hombre** |
| `xul` | **lo** |
| `ɣm` | **fue** |
| `xon` | **mas** |
| `tu` | **no** |

`ton` = *que* settles the point that this is not Sánchez's key, where *que* is `ho`.

Carried in `key_codes.tsv`.

## A second anchor, on the same leaf

Lower on f. 238 the cipher runs `… ɣof ∞7∞ᵷLʒ#8ʃ3m zun top │ descargo de los q │ …`, with
*descargo de los q* standing in the clear on the cipher page. The plaintext at that point (f. 242)
reads:

> … las obras ningun servidor de v. ma la esta satisfecho; **da por descargo** de lo que dexa de
> fazer la obligacion que tiene a procurar la paz …

So `zun top` = **da por**, which

- **confirms `top` = *por*** in a second, independent context (the first was `top ton` = *porque*);
- gives **`zun` = *da***;
- and shows the ten-sign run `∞7∞ᵷLʒ#8ʃ3m` standing where *satisfecho* must be, and the eight-sign
  run `Ɉ℔ɸʒx℔4` where *servidor* must be — so long words are spelled out letter by letter between the
  codes, as in Sánchez's cipher.

Nine values are now confirmed against the clerk's own plaintext, twelve more probable. The
`key_codes.tsv` file keeps the two apart in a `confidence` column; nothing probable is being used to
derive anything else.

## The key is shared across his letters

R9650 (9/26 ff. 269–272, the other *Decrypted* record) carries the same forms. On f. 270:

> `ᵹᵹʒ` **`ton` `tab` `xud`** `ɣifLᵹ` `zil` `tod` · **`tu`** `ʃʃ℔℔ᵹLᵷ9ʒ7` `zun℔` `xil` `to7` **`top`** ·
> *disimular en este caso v. Mt.*

`ton tab xud` stands there in identical forms, and `top` again immediately precedes clear words in a
slot that reads *por disimular en este caso* — a **third** independent context for `top` = *por*.
`tu` and `zun` recur too.

So Hurtado used one key across these letters, and values won on R9644 carry to the rest. That is what
makes the six non-decrypted records reachable once the key is far enough along.

## The clear version begins on f. 241, and gives the opening of the letter

`IMG_R9644_I45411_P1.jpg` shows f. 241: *Al Rey — de Lope Hurtado, de Roma, del primero de
noviembre*, then **Claro**, then the plaintext in lettered sections (A …). So the clear runs
ff. 241–242 and covers the cipher of ff. 238–239 from its start.

Its third paragraph is the crib for the top of the cipher page:

> **Es muy bien lo que v. ma dize que lo que hoviere de hazerse con** los criados de su Sa
> **primero los sepa, pero hasta que v. ma les de lo que fuere servido, si algo se le dixesse**
> pensaria que era para no les dar nada …

(bold = what stands in the clear on the *cipher* page too; the rest is enciphered there.)

Aligning the enciphered stretch after *si algo se le dixesse*:

| cipher | plaintext |
|---|---|
| `⊃84∞7ʒ∞7` | **pensaria** — eight signs for eight letters |
| `ton` | **que** (again) |
| `ᵷʒ7` | **era** |
| `teɡ` | **para** |
| later, `zun`+`ʒ` | **dar** |

New confirmed values: **`ᵷʒ7` = *era***, **`teɡ` = *para***, and the letter **`ʒ` = r** — the last
attested twice over, in the *r* of the spelled *pensaria* and in `zun`+`ʒ` = *dar*, which in turn
re-confirms `zun` = *da*.

**A retraction.** The earlier probable `zar` = *Bari* was wrong. `zar` is frequent, and here it falls
in the slot *los criados **de su** Sa*; it is now carried as *de* or *su*, still probable. This is why
the probable values are kept out of any derivation.

### The next line aligns end to end

The following line of cipher matches the plaintext token for token with nothing left over:

| `ta` | `xil`+s | `zun`+`ʒ` | `xur` `zun` | `ɋ` | `x∞ʒ∞7` | `ton` | `tu` | `ton`+`℔∞7` | `ton` | `xul` |
|---|---|---|---|---|---|---|---|---|---|---|
| no | les | dar | **na·da** | y | diria | que | no | **que·ria** | que | lo |

Three things come out of it.

1. **Two codes for *no*.** `ta` and `tu` both stand for it, in the same line — the cipher has
   homophones at the code level, not only in the alphabet.
2. **Codes carry syllables.** `xur`+`zun` = *na*+*da*, and `ton`+`℔∞7` = *que*+*ria*. `zun` is the
   same *da* confirmed earlier in *da por*; here it is the second syllable of *nada*. Word boundaries
   go both ways in this cipher exactly as they do in Sánchez's.
3. `x∞ʒ∞7` is five signs for the five letters of *diria*, consistent with `ʒ` = r.

### Three codes chained into one word

The next line gives `… ɋ xul h℔∞ ℔ xᵹ∞ **ton zun ℔∞74** ᵷard zilᵹ84 …` against the plaintext
*… y los criados **quedarian** descontentos …*:

> `ton` + `zun` + `℔∞74` = *que* + *da* + *rian* = **quedarian**

`zun` = *da* is now confirmed a third time, in a third role: a whole word in *da por*, the second
syllable of *na·da*, and the middle syllable of *que·da·rian*. The ending `℔∞74` is `℔∞7` (*-ria*)
plus `4`, which gives the letter **`4` = n** — the same sign as the *n* of the spelled *pensaria*.

### The letter alphabet starts to come out

The end of the same paragraph aligns exactly — four cipher units for four words:

| `∞L84℔ɋ` | `⊃8ʒxL67` | `xuɡ` | `ɣufɋ` |
|---|---|---|---|
| tiene | **perdida** | la | esperança |

*perdida* is spelled out, seven signs for seven letters, and that hands over a first slice of the
**substitution alphabet**:

| sign | `⊃` | `8` | `ʒ` | `x` | `6` | `L` | `7` | `4` |
|---|---|---|---|---|---|---|---|---|
| letter | p | e | r | **d** | **d** | i | a | n |

Two signs for **d** in one word — homophones in the alphabet as well as in the codes. The values
cross-check against the spelled *pensaria* earlier in the paragraph (same `⊃`, `8`, `7`, `4`) and
against `ʒ` = r, already confirmed twice.

### A name spelled out

Further down, between *a v. Mt.* and the clear words *es el principal*, the cipher carries the
plaintext **El camarero Pedro**. *Pedro* is spelled `⊃ 8 x ʒ m` — five signs for five letters, of
which p, e, d and r are already confirmed, so the last one falls out: **`m` = o**.

The alphabet so far: `⊃`=p, `8`=e, `ʒ`=r, `x`/`6`=d, `L`=i, `7`=a, `4`=n, `m`=o.

Thirty-three values confirmed, fourteen probable.

*One caution:* the sign transcribed `∞` reads as **t** in *tiene* but seemed to be **s** in
*pensaria*. One of the two transcriptions is wrong. It is left unassigned rather than guessed.

## The key reads a record DECODE calls non-decrypted

R9648 (9/26 ff. 260–265, 9 Nov 1522, **Non-decrypted**) turns out to carry the same matter as
R9644's clear — *pregunte a su S.* and *le avia embiado la carta de v. Mt y q esperava saber lo de
Yngalaterra* stand in the clear on its leaves, answering to section **C** of the R9644 plaintext.
Hurtado sent his despatches in duplicate, so one clear version serves both.

That makes R9644's plaintext a crib for R9648 as well, and the key built on it reads there. On
f. 262, nine cipher tokens against nine plaintext words, with nothing left over:

| `ɋ` | `ton` | `ɣub` | `taf` | `tu` | `ɣof` | `ɣuc` | `ton` | `L84ℇ℔` |
|---|---|---|---|---|---|---|---|---|
| y | que | el | papa | no | esta | en | que | venga |

and immediately after the clear words *pregunte a su S.*:

| `ton` | `teʒ` | `ᵹʒ4∞` | `7zar` | `ɣon` |
|---|---|---|---|---|
| que | nueva | tenia | de | Francia |

`ɋ`, `ton` and `tu` are values won on R9644 and reappearing here correctly, which is the check that
matters. Seven new values come out of it — **`taf` = *papa***, **`ɣof` = *esta***, **`ɣuc` = *en***,
**`teʒ` = *nueva***, **`ᵹʒ4∞` = *tenia***, **`ɣon` = *Francia***, and the spelled *venga* — plus
`ɣub` = *el* promoted from probable, and support for `zar` = *de*.

**This is the first previously-unread text of Hurtado's read here.** It is short, and it leans on the
duplicate's plaintext rather than standing on the key alone, so it is a foothold rather than a
reading. But the mechanism now works end to end: crib → key → a record nobody had read.

### And it keeps reading

Further down the same leaf of R9648, against section C of the R9644 plaintext:

> `ton` `ɣub` `zed` │ *le avia embiado la carta de v. Mt* │ = **que el arçobispo** …

giving **`zed` = *arçobispo*** — a name-code for the man who runs through this whole
correspondence, the archbishop of Bari.

And a few words on:

| `ton` | … | `xuɡ` | `tef` | `top` | `xul`+s | `ᵹʒ℔ʒℇᵹʒᵹ` | `ɋ` | `top` | `xuɡ` | … |
|---|---|---|---|---|---|---|---|---|---|---|
| que | desseava mucho | **la** | **paz** | **por** | **los** | infieles | **y** | **por** | **la** | necessidad |

Everything in bold is a value won earlier and reappearing correctly; `tef` = *paz* is new. The run
*la paz por los infieles y por la necessidad* is continuous previously-unread text — Hurtado
reporting that the Pope wanted peace because of the Turks and because of the Emperor's need.

### The alphabet decodes a word on its own

On f. 264 of R9648, between the clear words *antes de agora* and *si se oviera hecho*:

> ‖ `tu` `ʃu` `ᵹ…7` **`℔ᵹ8ʒxL6m`** **`xur zun`**
> = no se [h]uviera **perdido** **nada**

`℔ᵹ8ʒxL6m` spells out p-e-r-d-i-d-o. Six of those signs — `8`=e, `ʒ`=r, `x`=d, `L`=i, `6`=d, `m`=o —
were derived on R9644 from *perdida*, *pensaria* and *Pedro*, and every one of them is correct here in
a word decoded without being looked for. `xur zun` = *na*+*da* likewise reappears intact.

The whole sentence then runs: *y antes de agora **no se huviera perdido nada**, si se oviera hecho
como muchas vezes yo lo escrevi a v. Mt* — Hurtado telling the Emperor that nothing would have been
lost had his advice been taken earlier.

R9644 carries this same sentence in the clear, being the duplicate, so the reading is corroborated
rather than unsupported; but the **decoding** was done from the key, not read off the crib, and that
is the test the key needed to pass.

### The key stands on its own: R9656, an independent letter

Everything so far leaned, somewhere, on R9644's plaintext — R9648 being its duplicate. **R9656**
(9/26 ff. 334–335) is not. It is headed *Al Rey — De Lope Hurtado, de xx de noviembre*: a different
despatch, three weeks later, with **no clear version and no duplicate**. If the key is real it must
read there unaided.

It does. On f. 334, after the clear words *las cartas traxo don Correo q vino con la valante*:

> ‖ `tu` `n7` `Lᵹʒᵹ` `∞∞` **`ɣub`** **`taf`**
> = no … **el papa**

`ɣub` = *el* and `taf` = *papa* were both won on R9648 against R9644's crib, and both read correctly
here in a letter that crib does not cover. Elsewhere on the same leaf `ton` (*que*), `zar` (*de*),
`ɣof` (*esta*), `sub` (*si*) and `tu` (*no*) all fall in slots that make sense.

**This is the validation that matters.** The key was built on one letter's crib and reads in another
letter that has none.

The three unresolved units between *no* and *el papa* are left blank rather than guessed; the sense
wants something like "no ha querido ver", but wanting is not evidence.

### One more from the crib

R9648 f. 264, after the clear words *A lo q he entendido*:

> ‖ `ɣʒ` `ʃta` **`zil`** **`ɣub`** **`zed`** **`zar`** `ɣᵹᵹ84ɣ` │ *trata de algunas cosas su S.*
> = … **con el arçobispo de** Cosenza …

against section B of the R9644 plaintext. That gives **`zil` = *con***, re-confirms `zed` =
*arçobispo* in a second context, and promotes **`zar` = *de*** — now attested three times over
(*de su Sa*, *de Francia*, *de Cosenza*), which matters because `zar` is one of the commonest groups
on every leaf.

### The commonest group of all

A little further on the same leaf, against section C of the plaintext (*… por la necessidad de v. ma,
pues queda de la guerra honrrado y approvechado. Yo dixe a su Sa …*):

> … `zar` **`rab`** … `ᵹᵹ497xm` `ɋ` `7℔℔…xm` │ *yo dixe a su S. q v. Mt.*
> = … de **v. ma** … **honrrado** **y** **approvechado** …

`zar rab` falls exactly on *de v. ma*, and `rab` is one of the commonest groups on every leaf of
every letter — which is what *vuestra magestad* ought to be in despatches addressed to the Emperor.
**`rab` = *vuestra magestad***.

The two spelled words either side check the alphabet again: *honrrado* and *approvechado* both end
`…7 x m` = a-d-o, with `4` = n inside the first. Every one of those signs came from R9644.

Fifty values confirmed, ten probable.

## Section A confirms the spine

f. 237 carries the head of the ciphered letter, with **A** in the margin against the passage the
clear (f. 241) gives as:

> Ha sido muy bien que v. ma **prevenga a su Sa** de lo que conviene a su servicio, porque aunque
> **no haga lo que es obligado, no se disculpe despues con dezir que v. ma** no le mando prevenir…

The cipher runs, with the unbolded parts standing in the clear on the cipher page itself:

> *ha seido muy bien q v. Mt* │ `℔ᵹʒʒLℇ7` `ℇ7` **`ʃʃ`** **`ʃid`** │ *de lo que conviene a su servicio,
> por q aunq* │ ‖ `ɣʒ` **`tu`** `xLʒ` `ℇ7` **`xul`** **`ton`** **`ɣaf`** `tad` `xᵹ` **`tu`** `ʃu`
> `xᵹᵹɡLʒʒx℔` `ɣ7` **`zil`** `ɣʒʒ` **`ton`** **`rab`** │ *no le mando prevenir*

Six values already fixed — `tu` *no*, `xul` *lo*, `ton` *que*, `ɣaf` *es*, `zil` *con*, `rab`
*vuestra magestad* — all fall in their right places across a long sentence. That is the densest
single check the key has had.

New from it: **`ʃʃ` = *su*** and **`ʃid` = *Sa*** (Su Santidad, the Pope), from `ʃʃ ʃid` = *su Sa*.
Three more are probable — `tad` *obligado*, `xLʒ` *haga*, `ɣʒʒ` *dezir* — sitting in slots the sense
fixes but the counts do not.

The paragraph after it does the same. Clear: *Assi mesmo fue bien escrivir largo, **porque su Sa
tenia tanta passion que no conocia lo que** don Joan le havia servido*. Cipher:

> … **`top`** **`ton`** **`ʃid`** `ᵹ847` `ʃuf` `ʒ7xʒᵹᵹ4` **`ton`** **`tu`** **`zil`**+`mɡᵹᵹ`
> **`xul`** **`ton`** `xᵹ4` `LL741` …
> = **por** **que** **su Sa** tenia tanta passion **que** **no** **con**·ocia **lo** **que** don Joan

Seven fixed values in a row, and one more instance of the stem-plus-ending pattern: **`zil` (*con*)
+ a spelled *ocia* = *conocia***, which is the third construction `zil` has been seen in.

`ʃid` is worth a note. In section A it stood beside `ʃʃ` (*su*) as *su Sa*; here it carries *su Sa*
on its own. Either it means *Sa* and the *su* is sometimes coded separately, or it means the whole
title and section A wrote *su* twice. Not settled, and recorded as *Sa / su Sa*.

### The end of f. 237, and a second sign for o

The last two lines of the leaf run against *Yo he preguntado a su Sa lo que le parece **del duque**,
y me dixo que estava contento, **lo que no quedo de don Joan** segun dizen todos*:

> *yo he preguntado a su S. lo q le parece* │ ‖ **`zarᵹ`** **`ɣᵹb`** │ *y me dixo q estava contento*
> │ **`xul`** **`ton`** **`tu`** **`ton`·`x`·`m`** **`zar`** **`x`·`ᵹ`·`4`** `ʒLʃʃ4` `ʃob` `ɣL4`

- **`ɣᵹb` = *duque*** — the Duke of Sessa, the imperial ambassador at Rome, who with the Pope and
  the archbishop makes three of the four men these letters are about.
- **`zarᵹ` = *del***, `zar` (*de*) plus one sign.
- **`ton`·`x`·`m` = *que*+d+o = *quedo***, a code finished with two alphabet signs.
- **`x`·`ᵹ`·`4` = d-o-n = *don***, spelled outright — and that fixes **`ᵹ` = o**, a second sign for
  o beside `m`.

That last one matters beyond the word: `ᵹ` was one of the signs whose readings contradicted each
other, and it turns out to be a homophone of `m`. Part of the alphabet tangle recorded above was a
missing homophone rather than a bad transcription.

Fifty-five values confirmed, thirteen probable.

## A second complete crib: R9650 f. 272

R9650 has its own clear version, on **f. 272**, headed *Al Rey — De Lope Hurtado de …* exactly as
R9644's does. It is a full letter, and a rich one:

> Ayer vino posta **del arçobispo de Bari**; scrivieme de [xxiii] … dize que antes de seys dias
> enbiaria aqui uno suyo con quien avisaria largo … En substancia me dize que **los franceses son
> determinados de venir en Italia, y enbian gran suma de dinero a Leon**, y que es menester que se
> entienda en la defensa, y que **el papa** haga lo que pudiere, pues le va mas que a nadie. Y he
> dicho a su Sa que de **Hieronymo Adorno** me ha venido este aviso de unas cartas que ha tomado por
> amor de v. ma … por servicio de Dios y remedio de la yglesia y de su estado deve pensar lo que ha
> de hazer sin dilatar mas, porque despues no havra tiempo … trabajare de saber lo que el arçobispo
> scrive y vere la respuesta de su Sa. Y luego avisare a v. ma, que agora no puede ser, porque **el
> duque** me ha scrito que oy partira la posta … Yo le he avisado desto y a **don Joan Manuel** y al
> **visorey de Napoles** …

So there are **two complete cribs**, not one, covering two different letters — and this one brings
new vocabulary the first does not have: *franceses*, *Italia*, *dinero*, *Leon*, *yglesia*,
*Hieronymo Adorno*, *don Joan Manuel*, *visorey de Napoles*, *posta*. Those are exactly the content
nouns the key is short of.

It also tells us what the letters are *about*, independently of the cipher: the French are
determined to come into Italy and are sending a great sum of money to Lyon; the Pope must do what he
can; Adorno has intercepted letters; the archbishop of Bari is the channel to the Emperor.

## A measured coverage number

`decode.py` resolves a transcribed token string against `key_codes.tsv`. It applies **only the
confirmed values**; probable ones print in `<angle brackets>` so they can never be mistaken for
evidence, and unknown tokens print as `?tok` with a coverage figure.

Run on two lines picked from records the key was *not* built on:

| line | result | coverage |
|---|---|---|
| R9650 f. 270 | `?` que nunca hombre `?` con otros no `?` `?` les `?` por | **8/13 = 62%** |
| R9648 f. 262 | que nueva tenia `?` Francia `?` `?` que el arçobispo | **7/10 = 70%** |

So roughly **two tokens in three** now resolve on sight, in letters the crib does not cover. The
misses are of two kinds: a few nomenclator codes not yet met, and the spelled runs, which need the
alphabet. That is the honest state of the key — good enough to follow the sense of a passage, not
good enough to edit one.

## Where the work is now limited: the alphabet, not the nomenclator

The two halves of this cipher are not equally tractable at the resolution DECODE serves.

**The nomenclator is easy.** The code groups are three-letter latin trigrams written plainly —
`ton`, `zar`, `rab`, `xul`, `top`, `zil`, `taf` — and they read off the page without difficulty.
Fifty of them are now fixed, including the high-frequency spine (*que, de, no, y, por, la, lo, los,
el, en, es, si, con, papa, arçobispo, vuestra magestad*), and they carry most of the content.

**The alphabet is hard.** The spelled runs between the codes need per-glyph discrimination that the
images do not reliably support. Nine signs are fixed — `⊃`=p, `8`=e, `ʒ`=r, `x`/`6`=d, `L`=i, `7`=a,
`4`=n, `m`=o — every one of them cross-checked on several words. Beyond that the transcriptions
start to contradict each other:

- *tiene* wants `∞` = t, but my reading of *pensaria* wants `∞` = s;
- *venga* as transcribed wants `L` = v, but *perdida* fixes `L` = i;
- *Cosenza* comes out as eight signs for seven letters, with `ɣ` apparently serving as both c and z
  and `ᵹ` as both o and s.

At least one transcription in each pair is wrong. Rather than pick whichever reading suits, those
signs are left unassigned. **This is the same wall the sanchez1522 work hit**: the codes read, the
letters need a picture-book built glyph by glyph against known plaintext, and that is slow work on
these scans.

The practical consequence is that Hurtado's letters will read *in substance* — subject, parties,
sums, the drift of the argument — well before they read word for word.

## Next

- Work the rest of the R9644 alignment section by section, using the marginal A/B/C keys.
- Then R9650 (also *Decrypted*) and R9652 (*Partially decrypted*) as further cribs.
- Then apply the rebuilt key to the six non-decrypted records.
- Test whether the key is Juan Manuel's: Tomokiyo's Juan Manuel table has `ton` unassigned, so the
  values above do not yet contradict it, and the question stays open.
