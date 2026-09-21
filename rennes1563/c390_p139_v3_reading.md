# Colbert 390 p.139 (1563 note to the bishop of Rennes) — v3: READ IN PART

Fresh transcription from Gallica btv1b10033942k f70, region x3500-6320 y900-2700, autocontrast + gamma 2.2
(crops: c390/v3/blk_e.png, tiles T00-T31, zooms q*, z*). Tokens: c390_p139_v3.txt (legend in its header).
Values: Tomokiyo/key.md homophones + p.138 gloss calibration; lattice (fr-1530-despatches) with <=2 values per
glyph, nulls only //, =, d-loop (ꝺ) and the clear-looking pour/que/est lookalikes. Per-token alignment:
c390_p139_v3_lattice.txt. Status marks: **secure** = every glyph at its calibrated value, sense closes;
*probable* = one glyph forced or one letter missing; … = unread.

## p.138 calibration check (done first)
Confirmed against the gloss: V̄6/v̄ß = qu'il; qq = que; ⊥⊥ = pour; ca = faire; z = p and a (parler = z z ℌ β ƀ ℌ);
ℌ = r; ƀ = e; β/ß = l; 9 = n (m in "mariage"); ſſ = o (g in "digne"); λ = u/v; aß = v/u; La = d; ϑ = m;
η = a; 3 = c/e; x1 = e (re-garde); 8 = luy; ā = g; ẽ = ff (suffisant). ꝺ behaves as a null on p.139.

## Line by line (pass 3: tokens re-encoded with separated shape classes; v3dec.py fixed values)
Fixed values: ʒ̶=s, ʒ=s, ʓ/ʒ̂=r, ſ=a, ſʳ=null, ℊ plain=o, ℊ looped=f, 4-star=x, ✗=b, ll=ss, md=ce, ẓ=null,
ÿ=null, ♯=y, ⊬=y, ꝺ=null, others as p.138. `?` = no value. Secure/probable reading beside each line.
1  queievoustiennepourtrop            **que je vous tienne pour trop**
2  aduiseyaffectionegloyalservite(ur) **advisé** [et] **affectionné** *[ā] loyal serviteur* (♯ here must be "et"; 1st λ = e)
3  (u)rduroymonfilspourvousen·orloair·bien   *[servite]ur* **du roy mon fils pour vous en** … **bien**
4  [en]dchosequi[est]aiartieyeasonservi       … *chose qui est* … **son servi-**
5  cesnelaisseratienvousdirequilfault         **-ce** … *[n]e laisser* … **vous dire qu'il fault**
6  bienquevouslesyeuxofrtypourobserver        **bien que vous les yeux** *o[uv]erts* **pour observer**
7  coretotesccsseseasseronteni                *comment? toutes ces … passeront en ce…* (ƀ = p here, key value)
8  auoyailcedemoncousinyqueoessdr?            … **ce de mon cousin** … que …
9  ?sesactionsencoresqueienin                 **ses actions, encores que je** …
10 ?visseaucuneoentadoubte·racineoe          … **aucune** … *doubte* …
11 doyeraduisetoutcequevouscongnoistrez       … *advis*, **et tout ce que vous congnoistrez**
12 llemer[blot]iter?anlenvoyeyal?ndae         … *[e]n l'envoyez* …
13 euobeaufrere·sseparedes?                   … **beau frère** … *[se] sépare des* …
14 rinciraalebien                             … **bien**

## Pass 2 (exemplar separation, same session)
Shape separations found by using secure words as exemplars (zooms c390/v3/q0-q7, z1-z3):
- **ʒ̶ (crossed 3-swash) = s**: l.2 [s]erviteur, l.4 [s]ervice, l.6 ob[s]erver. Plain ʒ = s in l.9 "ses";
  hook-topped ʒ̂ = r (l.3 servite[u]r). ʓ (s-hook) = r (l.6 obse[r]ver, l.11 congnoist[r]ez).
- **ſʳ (long-s with r-hook) = null**: l.4 ser[ſʳ]vi, l.5 [ſʳ]ce, l.6 ob[ſʳ]serv-. Plain ſ = a (advisé, aucune).
- **♯ = y/i** (key "hash"): l.2 lo[y]al; l.11 do[y]e. In l.2 "advisé ♯ affectionné" it must be "et" (unresolved).
- **ℊ plain = o** (l.2 l[o]yal); **ℊ looped = v/f** (l.5 qu'il [f]ault, l.6 o[v]erts) — one value not settled.
- **✗ = b**: l.6 o[b]server, l.10 dou[b]te, l.13 [b]eau frère.
- **4 in l.6 = x** (key star4): les yeu[x]; 4 = f elsewhere (fils, beau frère) — two shapes, not yet separated on image.
- **ll = ss**: l.5 lai[ss]er. **md = ce** (l.11). **ẓ = null** mostly, **z** in congnoistre[z]. **ÿ = null**.
- Still no value: ẟ/ẟar/ẟao (l.9, l.12, l.13 end — p? in "[p]rinci-"), ℛ (l.10), ✱ (l.12), aʓ (l.12), N (l.8),
  ℞ (l.4), ꞇ (c with bar, l.7), € (c in "cousin" but blocks l.10 "sa [sainc]teté").

Newly read (pass 2), cipher -> text:
- l.2 Lo ß ℊ ♯ η σ | ʒ̶ λ ℌ λ k G x1 aß ʒ̂ = *[et] loyal serviteur* (first λ must be e: a backslash-e? — probable)
- l.4 … ¢ C aı ẓ ʒ̶ ſʳ x1 ℌ aß io ſʳ 3 d = **son service** (secure)
- l.5 x1 σ z ẓ mJ ll d ℌ = *(n)e laisser* (probable); … < ÿ La k ẓ ʓ ƀ = **vous dire**; v̄ß ℊ z λ σ eτ = *qu'il fault*
- l.6 < σ x1 ¢ ♯ ƀ µ 4 … ſſ ℊb ℌ G ŧ ⊥⊥ ſſ ✗ ſʳ ʒ̶ d ʓ aß ƀ ℌ = **vous les yeux** … *overts* **pour observer**
- l.9 end / l.10 start: que je … *[v]ie?* **aucune** … *de doubte*
- l.12 ſ 9 ß d aı µ C ⊬ ƀ ŧ = *[e]n l'envoyez* (probable)
- l.13 ✗ d η µ 4 ℌ ƀ ʓ x1 = **beau frère**; ʒ ¢ ƀ z z ℌ ẓ d La ƀ ŧ = *[se] sépare des* (probable)
- l.14 ʓ k 9 ẓ m io ʓ η ſ ß x1 bien = *[p]rinci[p]ale? … bien* (low)

## Pass 3 additions
- l.7 end: ¢ ƀ η ll ẓ x1 ʓ ſſ aı eτ d 9 m x1 = *[e]s passeront en ce* — ƀ takes its key value p here (probable).
- l.7 start: m C Ꝫ x1 G · C eτ x1 ẓ ¢ 3 € = *comment? [t]o[u]tes ces* — Ꝫ (ℌ-like with a 3, not ℌ) read as mm/men;
  € = e here but c in "cousin" (two shapes or one polyphone): not closed.
- l.12: ✱ is an ink blot over a glyph (image r10), not a sign.
- l.11 "ſʳ ʓ ſ La λ mJ ¢" = ·r a d v i s: ʓ = r gives "r'advis"; "son advis"/"s'advis" needs ʓ = s. Blocker: ʓ.
- l.3 end, l.4 middle, l.8, l.10 end: no word closes with any class value; listed below.

## Pass 4 (every open run; candidates tested in t4.py with only the run's uncertain signs free)
- l.2: the sign before "affectionné" is NOT ♯: zoom p0 shows a looped tp-form (key: et = g-tail/tp). **tp = et**
  (secure); ♯ (crossed tt) = y/i stays (lo[y]al, do[y]e). Two shapes, settled.
- l.4: ƀ tp d η ¢ C aı = *[..]e et en son service* (η = n, key a|n); "ſ mJ z ʓ G k ẓ" before it still fails:
  candidates "à ma partie", "à part", "importante" all break mJ = i or ʓ = r. Blocker: mJ/z order in this run.
- l.5: x1 σ z ẓ mJ ll d ℌ ſ T = *[je] ne laisseray* with T = y (key T = y) and ſ = a; "ʒ 9" before it would
  need ʒ = je (not attested); io ƀ η after it unread ("de" expected; does not fit). Blockers: ʒ here, io ƀ η.
- l.12: σ d ϑ ƀ ʓ ✱ mJ G x1 ℌ = **le mér[i]ter** (✱ = blot over i); ẟao 9 ß d aı µ C ⊬ ƀ ŧ = *[en/on] l'envoyez*
  (lattice best "on"/"en"; ẟao one vowel-sign or clear "a"?). Blocker: ẟao.
- l.12 end - l.13: ſ σ aʓ 9 ẓ La ſ ƀ x1 λ ℊ ẓ before "beau frère": no candidate closes; lattice gives only
  "l'and-peu-" nonsense. Blockers: aʓ, ℊ (ε-form), ẓ.
- l.13: ✗ is a stroke through δ (✗δ) — one sign, b.
- l.3 end, l.8 (ſ λ ſſ ♯ z k ß; ♯ qq N d ʒ ¢ La ʓ ẟ ẓ), l.9-10 (d 9 mJ ẓ aı ℛ aß io ll d; ʓ z € mJ aı ÿ ƀ ℊ x1),
  l.14 (ʓ k 9 ẓ m io ʓ̃ η ſ ß x1): no candidate fits all fixed values. "princi[p]a[l]e" (l.14) needs ẟao = p and
  ʓ̃ = p, contradicting l.12 — rejected.
- Settled page-wide: tp = et; ♯ = y/i; T = y; ✗δ = b; ✱ = blot. Not settled: ƀ (e everywhere; p only in
  "passeront", l.7 — likely a different ƀ shape, unconfirmed), € (c in cousin, e in l.7), looped ℊ (f/v), ℞, ℛ,
  ẟao, aʓ, N, ẟ.

## Pass 5 (glossed values from colbert390_glossed.md: p.189/p.199 slip, p.221, p.225)
Applied: € = f; plain ℊ = u; looped ℊ = m/o; ♯ = y; N = l; ƀ = e only; ‖/ll = word "plus"; ‡‡ = et; ‡ = pour;
tı = p; ζ = p/i; Y = d; ıō = i/y; h = b. Decode (v3dec.py, V.update line):
1 queievoustiennepourtrop · 2 aduise[et]affectione·loyalservite(ur) · 3 urduroymonfilspourvousen…bien ·
4 …chosequi…[ƀ‡‡]…sonservi · 5 ce…nelai[plus]eray…vousdirequilvault · 6 bienquevouslesyeuxouertspourobserver ·
7 coretotescfssesea[plus]eronteni · 8 auoyail·cedemon[€]iousin·yquelessdr… · 9 …sesactionsencoresqueie… ·
10 …vi[plus]e·aucune·uenta·doubte·[ʓ]afin[ÿ]eue · 11 doye…advis·ettoutcequevouscongnoistrez · 12 lemér[i]ter…l'envoyez… ·
13 …beaufrere…separedes · 14 …bien
Consequences:
- **ℊ classes re-sorted by value**: the ℊ in "loyal" must be the looped form (= o); the ℊ in l.5 "qu'il [ℊ]ault" and in
  l.6 "o[ℊ]erts" read as plain ℊ = u/v: **qu'il vault / ouverts** (probable; "fault" withdrawn). My l.5/l.6 shape
  labels were the wrong way round; re-check on the zooms.
- **ƀ = p withdrawn**: l.7 "passeront" retracted; with ll = plus, l.7 end reads "s e a [plus] e r o n t" (unread).
- **ll = plus breaks l.5 "laisseray"** (mJ ll d ℌ ſ T = i[plus]eray). Either this ll is a different ss-sign or the
  reading is wrong: downgraded to unread-probable.
- **€ = f breaks l.8 "cousin"** (€ mJ ſſ µ ¢ mJ aı = f i o u s i n). p.221 writes cousin 3 ſſ λ z m 9, so the l.8
  sign should be re-checked; "mon cousin" is kept as probable on context (p.221: "mon cousin le cardinal de Lorraine").
- **€ = f in l.10**: "ʓ z € mJ aı" = [ʓ] a f i n → **afin** (probable); what follows (ÿ ƀ ℊ x1 = [ÿ] e u e) is unread.
- **€ = f in l.7**: "¢ 3 € ʒ ʒ̶" = s c/e f e s → *ses effe[ts]?* (weak).
- N = l: l.8 "♯ qq N d ʒ" = y que l e s → "…y. Que les…" (probable).

## Running text (French, pass 5)
[Envoyez que par] … que je vous tienne pour trop advisé et affectionné et loyal serviteur du roy mon fils pour
vous en … bien … chose qui est … et en son service … [ne] lai[ss]eray? … vous dire qu'il vault bien que vous
[ayez] les yeux ouverts pour observer … ses effe[ts]? … -eront … ce de mon cousin …, que les … ses actions,
encores que je … aucune … doubte, afin … advis, et tout ce que vous congnoistrez … le mér[i]ter … l'envoyez …
beau frère … [se] sépare des … bien.

## English
"… that I hold you too well-advised, devoted and loyal a servant of the king my son to … you … a matter which is …
and in his service … to tell you that it is well worth your keeping your eyes open to watch … its effects(?) … of my
cousin … that the … his actions, although I … any … doubt, so that … opinion, and all that you will learn … to
deserve it … send it … brother-in-law … separates(?) from … well."

## Secure / probable / unread (pass 5)
- Secure ~160 / ~440 (36%); probable ~120 (27%); unread ~37%. The glossed values removed two pass-3/4 readings
  (passeront, fault) and put laisseray and cousin in doubt; they added afin, vault, ouverts, que les.

## Glyphs that block (pass 5)
| run | blocking | note |
|---|---|---|
| l.2 ā after affectionné | ā | g at standard value; no word |
| l.3 end ÿ ſſʓ Lo ℊ ſʳ mJ ʓ ẓ | ſſʓ, ℊ class | no word before "bien" |
| l.4 ℞; ſ mJ z ʓ G k ẓ ƀ ‡‡ d η | ℞, mJ run | "et en son service" kept; middle run open |
| l.5 ʒ 9; mJ ll d ℌ ſ T | ll (plus vs ss) | "laisseray" needs ll = ss |
| l.6 ẓ ſʳ | – | verb before "les yeux" missing (maybe the ẓ sign) |
| l.7 whole | Ꝫ, 3/€, ll | only fragments |
| l.8 ſ λ ſſ ♯ z k ß; € in cousin; ¢ La ʓ ẟ ẓ | €, ẟ | |
| l.9 ẟar; l.9-10 d 9 mJ ẓ aı ℛ aß io ll d | ẟar, ℛ, ll | |
| l.10 ℊ ƀ aı G ſ ("uenta"); ÿ ƀ ℊ x1 after afin | ℊ class, ÿ | |
| l.11 ſʳ ʓ ſ before advis | ʓ | |
| l.12 ẟao; ſ σ aʓ 9 ẓ La ſ ƀ | ẟao, aʓ | |
| l.13 x1 λ ℊ ẓ | ℊ class | |
| l.14 ʓ k 9 ẓ m io ʓ̃ η ſ ß x1 | ʓ̃, ẟao | |
Signs never glossed anywhere yet: ẟ, ẟao, ẟar, ℛ, ℞, aʓ, Ꝫ, ſſʓ. Next exemplars per colbert390_glossed.md: € and
ll lines of p.221/p.225, then pp.223-231 and p.313/317.

## Method (passes 1-5)
1. Fresh transcription from IIIF f70 (autocontrast + gamma 2.2, tiles and 1.5x zooms); p.138 gloss alignment
   rechecked; fixed-value decode with Tomokiyo key (key.md) + p.138 values; lattice (fr-1530-despatches), ≤2 values/glyph.
2. Secure words used as exemplars to split shape classes (ʒ̶/ʒ/ʒ̂/ʓ, ſ/ſʳ, ℊ plain/looped, ✗, ll, md, ẓ, ÿ);
   a page-wide one-value-per-glyph ascent (v3ca.py) was tried and rejected (homophones/polyphones break it).
3. Tokens re-encoded with the classes (c390_p139_v3.txt header), v3dec.py re-run; l.7 end read ("passeront").
4. Every open run zoomed; candidate readings tested in the lattice with only that run's signs free (t4.py) and
   checked against other occurrences; tp = et, T = y, ✱ = blot settled; l.4, l.5, l.12 advanced.
5. Glossed values from other Colbert 390 pages (colbert390_glossed.md) applied; runs re-decoded; readings that
   contradicted them withdrawn or downgraded.
