# fr. 3181 f. 55: second transcription pass (v2)

Source: Gallica btv1b9059845t f36, region x 4600–8720, y 600–2800 (full-res). Each line was cropped
in halves at native resolution. The first-pass crop `f55rot.png` covers only lines 1–10; lines 11–13 lie
below y 2058. Tokens with candidate sets are in `f55_v2.txt`. Decode with `PYTHONUTF8=1 python lattice.py f55_v2.txt`.

## Values changed or added since the first pass
- **ℌ = r** (not b). It gives *descouvert* (l.1) and *pourra sortir* (l.5).
- **ɼ (c with a curl) = o**. It gives *mon intention* (l.3), *pourra* (l.5) and *voir* (l.10).
- **ɗ (d with a loop) = u/v**. It gives *advis* and *sur* (l.2), *toute* (l.3–4) and *voir* (l.10).
- **ɕ (c-curl with a tail) = t**. It gives *conduict[e]* (l.2), *te* (l.4) and *monstr…* (l.8).
- **+ = y** in l.1 (*j'ay*). It is *vostre* in l.2 (*vostre advis*), the same double value as in c390 p.357.
- **ß = l**. It gives *concile* (l.9) and *l'utilité* (l.10).
- **G̃ = rt** in *sortira* (l.10).
- **ʮ = et** (probable) in l.2, l.4 and l.8. It may be a null.
- **✗ (crossed) = b** in *deli✗eray* (l.6).
- **ꜧ = y** in *ayt* (l.4) and *j'ay* (l.5).
- **The last cipher word is *Trante*** (Trente, for the Council): G 5ʼ z 9 G ᑲ.

## Line by line (letters; ? = unresolved sign; word division mine)
1. [do=null] par o u i a y s c e u c e *que* *vous* a v e z d e s c o u v e r t
2. ? ? *par* o? e *la* d u m a r i a g e s? *et* *vostre* a d v i s s u r *la* [con] d u i c t
3. e d i c e u l x e n (?) m o n i n t e n t i o n ¢? e t r? q u e t o u
4. t e (‡ null) f o r ? *et*? a y t t e n u c e c h e m i n d ? n t i e u e r a ?
5. c e *qui* p o u r r a s o r t i r i a y a u s s e n t e n d u c e *que* l
6. *vous* m i s t e n a v a n t *qui* l a v o i t d e e l i b e r a y *faire* ? *lettre* *bien*
7. d e *la* ? b/p i e n t (e/ost) *et*? [= null] a v a n c e ? ? c o n c i l e a c e *que* i u
8. ? q y c h a c u n *faict* l/s d e e a i n a *par* t *et* m o n s t r r e r b
9. o ? e e/et f r u c t u e u s e ? (r)t y e e u e e d e c e c o n c i l e *mais* *nous*
10. s o m e s [= null] v o i r l u t i l i t e *qui* e n s o (rt) i r a [= ⱬ nulls] m e s
11. m e s ? e c e *qui* s e p r o m e c t d e s s e (e e) i o n s **Decembre** (clear) d e s
12. *que* ? e s *vous* a v e z o y *par* *lettre* s *vous* *est* a n t d e r n i e r e ? e n t a ? ?
13. t r a n t e [nulls: // ʌ vre & que xix ß]

## Running text

> c'est pour … par où j'ay sceu ce que vous avez descouvert … par … la [matière] du mariage, [et]
> vostre advis sur la conduicte d'iceulx en mon intention, [et] se trouve toute … fort … [et qu'il]
> ayt tenu ce chemin, dont … ce qui pourra sortir. J'ay auss[i] entendu ce que l[e …]
> vous mist en avant, qui l'avoit … délibéray faire … lettre bien … de la … bientost [et]
> l'avance[ment du] concile, à ce que j[e] veoy[?] chacun faict … de … part, et monstrer
> b[onne et] fructueuse … de ce concile. Mais nous sommes [à] voir l'utilité qui en sortira,
> mesmes ce qui se promect des sessions [de] Decembre, desquelles vous avez oy par
> lettres, vous estant dernierement à … Trante.

**In English.** Catherine has learned what Rennes discovered and has his opinion on the marriage question
and on how to handle it, in line with her own intention. She hopes that whoever has taken this course will
keep to it, and that something will come of it. She has also heard what someone (name lost) put to Rennes.
The Council follows: she wants it advanced quickly, and wants everyone so far to do their part and to show
[good and] fruitful … of the Council. "But we are waiting to see the benefit that will come of it, and in
particular what is promised from the December sessions," of which Rennes has heard by letter, having lately
been … at Trent.

## Follow-up pass (sibling value tables applied)
- **ſſ = o** (p.139). In l.3, "¢ ᑲ ɕ ℌ ʃʃ gʃ ᑲ G ɼ ɗ" becomes s e t r o u(v) e t o u, i.e. *se trouve tou[te]*. This is probable (the ¢ = s and gʃ = v choices are forced).
- **ſſ = o** in l.4, "ſa ʃʃ 9 ɕ" becomes *dont*. The rest, "10 ᑲ ɗ xy ee z r", reads i e v e r a ?, which is not a word. *continuera* is dropped.
- **N = l** (c392). In l.11–12, "ſa ᑲ ¢ | qq N ᑲ ʒ" becomes des|que|les, i.e. *desquelles vous avez oy par lettres*. This is secure, and it closes the start of l.12.
- **ℊ = m** (c392). In l.12 it gives *dernierement* (secure).
- **l.8.** With µ = v and ᑲ read as e, "iu | ᑲ ʃʃ ꜧ" gives j v e o y, i.e. *je veoy* (one letter out of order). This is probable.
- **✗ = b/c.** *délibéray* is kept. At the end of l.8, ✗ = b still gives *b[onne]*; this is probable.
- The following were checked against the siblings with no gain:
  - ꝥ ꟗ (l.2)
  - gd (l.4)
  - ⊥ (l.6)
  - ɸ (l.7)
  - ß ſa ᑲ ᑲ z 10 9 z (l.8)
  - ‡ G̃ ꜧ … (l.9)
  - ɾ (l.11)
  - z h Ə (l.12)

  Single ‡ is not the double ‡‡ (n/et) of c392, so I left it unassigned.

## Security
There are about 470 cipher glyphs. After the follow-up pass: about 78% secure, about 9% probable (*et* = ʮ, *conduicte*, *se trouve toute*, *je veoy*,
*bonne et*, *sommes*, *mesmes*) and about 13% unread. Before v2, about 55% was secure.

## Still unread
- **l.1 start "par où j'ay"**: + = y is attested in c390, but "par où" before "sceu" is odd. It might instead be "par lui a vostre".
- **l.2, the first two signs (ꝥ ꟗ)**, and **ɼ ᑲ before *la***: these are unknown signs. They are perhaps "[et]" and "ce".
- **l.3, εʃ after *en*, and ¢ before *et*.** One extra sign each, perhaps nulls.
- **l.4**: *gd* after *fort* is unknown. After *dont*, the signs "10 ᑲ ɗ xy ee z r" (i e v e r a ?) do not make a word.
- **l.5, *aussi***: the *i* is missing, or ʒ = si.
- **l.6, "qui l'avoit t'… délibéray"**: the grammar is unclear. The sign ⊥ before *lettre* is unknown; it may be *une* or *la*.
- **l.7, ɸ before "bien/pien"**, and **"5ʼ ɕʃ" in avance[ment du]**: *ment du* is restored from the sense, not from the signs.
- **l.8 is the weakest line.** "…q y chacun" may be *jusques icy*, but that needs *e* = s. "l/s de e a i n a" is not read; it may be *son devoir* with misread signs. "monstrrer" has one r too many.
- **l.9, "? (r)t y e e v e e" before *de ce concile*.** Six *e*-homophones in a row suggest that some of these shapes are other letters (s?). *l'yssue* is a guess and is not used.
- **l.11, ɾ in "mes?e"**, and *sessions* has three e-signs in place of the double s. The same homophone confusion.
- **l.12, "z h Ə" before *Trante***: *à* plus two signs with no value. Perhaps *au [concile de]* abbreviated, or cancelled strokes.
- **General**: the ᑲ / d / ɗ family (e, s?, u/v) is not fully separated. Most of the remaining gaps are e/s ambiguities. Working through the sibling letters (Colbert 390 p. 139, 392 p. 231) should separate them.

## Crib pass (La Ferrière II, spring–summer 1563)
The letters to Rennes printed nearest in date are 30 Apr 1563 (LF II 85-88, Colbert 390 f.183), 17 May 1563 (LF II 36-38, fr. 3181 f.5x) and 13 July 1563 (LF II ~?, Gaillon).
LF II also mentions, in its notes, Lorraine to Rennes of 20 June ("efforts … pour obtenir la session du concile en juillet"), Birague of 30 June on the marriages, and Lansac from Trent, 8 July (the portraits of the King of the Romans' daughters). colbert390_glossed.md was not present when I checked.

The wording that bears on f.55 is:
- 17 May: "j'ay veu ce que me respondez des mariages … ce que mon cousin le cardinal de Lorraine en a proposé et traicté avec mondict frère l'Empereur". This supports *du mariage … vostre advis* (l.2).
- 17 May: "Il y a longtemps que nous n'avons que bien peu de choses du Concile … si cette longueur d'attente nous produisoit quelque bon fruict, dont je ne sçay que me promettre, encores que **chacun veoye** à l'oeil le besoing … d'une **bonne et** sérieuse reformation". This parallels l.8–10: *chacun … bonne et fructueuse … ce qui se promect*. It raises *b[onne et] fructueuse* to probable-strong. It also points to "veoy/veoye" in l.8 (*je veoy*, kept probable).
- 17 May: "Mandez-moy si mondict bon frère **continuera** en sa résolution d'aller en personne audict Concile". This makes "… continuera" a candidate again for l.4 ("ſa ʃʃ 9 ɕ 10 ᑲ ɗ xy ee z", read d o n t i e v e r a). The signs do not give c-o-n-t-i-n-u, so it stays unread. It is noted as the likely sense (the Emperor continuing on his course: "ayt tenu ce chemin … continuera").
- 30 Apr: "le rendre **fructueulx**". This supports l.9.
- 13 July: "suis bien de **vostre adviz**". This supports l.2.

Nothing in these letters touches the openings of l.1 or l.2, or the ⊥ and ɸ signs in l.6–7. Re-checked on the crops, no crib changes a sign value. The crib pass therefore upgrades confidence and does not add letters.

**Final figures:** about 78% secure, about 10% probable, about 12% unread. The 95% target is **not** reached. The remaining gaps need either a glossed sibling that exemplifies ꝥ ꟗ, gd, ⊥, ɸ, ‡ and G̃ as whole letters, or a copy of the decipherment (none is known; LF printed the passage as "Partie chiffrée"). Crib-guessing letters into those slots would be invention.

## Glossed-sibling pass (f. 57–58 aligned; see fr3181_glossed.md)
Sign values taken from the f. 57–58 margin decipherments, which are in the same hand as f. 55:
- **ʃʃ (the ɕʃ sign) = le.** Glossed three times. This corrects the earlier "sc = lettre" reading:
  - l.6 "ca ⊥ ʃʃ pl" becomes *faire ⊥ le bien* (secure).
  - l.7 "avance 5ʼ ʃʃ concile" becomes *avancer le concile* (secure; 5 = r is glossed in *prendray*, the same value as in *Trante*). This removes the old *avance[ment du]* guess.
  - l.12 "at ʃʃ ʒ" becomes *par-le-r*, i.e. *oy parler* (secure). "N ᑲ ɤ" with ɤ = z gives *desquelz*.
- **⊥ (l.6) = u̲ = pour**, the word sign glossed in *pour eviter*: *délibéray faire pour le bien* (probable, from a shape match).
- **ɸ (l.7):** "ɸ 5 10 ᑲ 9 G ᑲ̌" reads ɸ + r i e n t é. *le bien de la [Ch]rienté*, i.e. *Chrestienté* (the "xpienté" abbreviation, ɸ = chi), is probable. ɸ itself is not glossed. The following "# =" is *et* + null.
- **ꟗ (l.2) = ∠ = vous** (glossed in *si vous le*), probable. So l.2 opens "ꝥ vous par ɼ ᑲ la du mariage". ꝥ and ɼᑲ stay unread.
- **l.4: ‡ = con** (‡̲ glossed in *congnoistront* and *contentement*), and **gd = g ᑲ = m e** (small g = m is glossed 5 times). This gives *toute conforme*: "se trouve toute conforme, et ayt tenu ce chemin" (probable).
- **The d-family, settled.** d = e; La = d; ɗ/ɑS = u/v; ∂/ϑ = m; ᑲ = e in all ~20 glossed cases; the overlined ᑲ̄ = se. **No gloss supports ᑲ = s.** The ᑲ-runs in l.9 (‡ G̃ ꜧ ᑲ ᑲ ɑS ᑲ ᑲ) and l.11 (*sessions* with three ᑲ) therefore stay unread or suspect. They were not forced.
- **Unchanged and still unread:**
  - l.1 opening
  - ꝥ, ɼ ᑲ (l.2)
  - εʃ, ¢ (l.3)
  - "10 ᑲ ɗ xy ee z r" after *dont* (l.4)
  - ß La ᑲ ᑲ z 10 9 z (l.8), where ß could be l or g, both glossed
  - ‡ G̃ ꜧ … (l.9; *con…* is possible if the ‡ is the same sign, but no word fits)
  - ɾ (l.11)
  - h ϑ (l.12)
  - f.52 was not aligned: it is in a different hand and has no ᑲ.

### Running text (after this pass)
> … vous avez descouvert. [ꝥ] vous par … la [matière] du mariage, et vostre advis sur la conduicte d'iceulx en … mon
> intention se trouve toute conforme, et [qu'il] ayt tenu ce chemin, dont … ce qui pourra sortir. J'ay aussi entendu ce que
> l[e …] vous mist en avant, qui l'avoit délibéré faire pour le bien de la Chrestienté et avancer le concile, à ce que je veoy
> chacun faict … par[t], et monstrer b[onne et] fructueuse … de ce concile. Mais nous sommes à voir l'utilité qui en sortira,
> mesmes ce qui se promect des sessions de Decembre, desquelz vous avez oy parler, vous estant dernierement à … Trante.

**Figures (about 470 glyphs):** about 80% secure, about 11% probable, about 9% unread. The previous figures were 78%, 10% and 12%. The 95% mark is still not reached.

## Colbert 390 pass
The glossed pages of Colbert 390 (pp. 241–305, 313 and 199; pp. 221–231 excluded) are in the f.52 hand. Only h has a glossed value there: **h = b** (p. 241, "mon beau"). In l.12 "z h Ə Trante" that gives à b … Trante, which is not a word, so it stays unread. εʃ (l.3) and ɾ (l.11) may be Tomokiyo's nulls "eps3" and "r-hook". That is not glossed, so I have not counted them as read. No other residual sign was resolved. **The figures are unchanged: about 80% secure, 11% probable, 9% unread.**
