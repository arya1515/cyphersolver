# f. 46r — Gramont to Montmorency, Rome, 11 Oct [1529] (BnF fr. 3091 no. 23), right page of `full/btv1b9060253s_c050.jpg`

The page is entirely in cipher: 33 lines, and the text runs on from f. 45v and into f. 46v (the first and last words are split across pages).
Key: Lasry, BnF fr. 3040 f. 16. Crops are in `work_46r/` (`Z<nn>_0/1/2.png` = each line in three overlapping pieces at 1.7x; `lc3.py` makes them).
The aliases below are the ones fed to `decode.py`. Where a glyph read against the table, the alias records what the glyph *reads as* (see "Key notes").

## Key notes (from this page)

* **`#` (compact hash) is very often A, not M.** It gives a in faire, raint, alliez, aultrement, affin, admiral, charge, laisse,
  avant, tant, sa, parolle, avoir, gardes, pancant, plaindre, etc. Elsewhere it gives m (mine, me, ministres, mes, mais,
  nombre, deman-, demesler). Glyphs I read as A are written `H` below and those read as M are written `#`. On this page I could not
  see a consistent difference in shape between the two, so the choice is made from context.
* **The R-shaped glyph after an A-sign reads V/U** (`k` below) 4 times: `A R` au commancement (L06), `# R` si avant (L11),
  `A R` davantage (L14), `o R | C e 8 L` aucune (L32-33). Everywhere else R = E (que, faire, pere, estre ...). It could be a
  distinct V-glyph that looks like R, or an "au/av" digraph.
* **`ß` vs bold `B`:** the common glyph in que/qu'il/quelque/avecques/quoy is Q (`b`). Real B (`B`) only in obligé, observer,
  bonne, bon, bien, besoin, soubdaine, nombre, combien.
* **ρ-o-ρ (two F's joined by a ring) = FF** in affin (L09, L20) and proffit (L29), so the ring is not a null here.
* **"Ш on a bar" = G** (guerre, longue, regarde, charge, gardes, davantage, dommage, besoing). **●/◉ (ring with dot) = V/U**
  (sieur, ou, leur, pour, aux, avoir). It also seems to stand for m in doumage (L29), or that spelling is simply Gascon.
* **`Y` (S-hook flourish over a crossbar) = I/Y**: luy, j'ay, il y, voyant, delaiast.
* **Signs the table does not cover:**
  - `!` = a cross with a spiral/loop head. It occurs twice: "luy estre [!] obligé par ses chappitres" (L01) and "avecques ledict [!] aux aultres
    choses" (L12). It is probably a word or name sign (Empereur? pape?). I have not identified it.
  - `?` in L14 and L26 = a small triangle on a stem standing on a base bar. In L26 it sits between two -o- nulls right after the heart name sign
    ("la bonne grace du ♡ ~?~ &"). It may be a second name sign or a separator.
  - Other `?`: L01, after "ses" (a dark ß-like blot); L03, a dark blot in "d?eulx"; L16, an R-shape with a long tail tangled with L15's
    zigzag, reading "m'a d?"; L27, a small c/o-like glyph that must be A (traicter).
  - `(` / `)` (a short 3-shape) = null (L04, L07).

## Line by line

Lnn | aliases | decoded | word-divided French reading
---|---|---|---
L01 | `l n Y W s d r R ! g B l 4 G W v H r s R s ? C 7 A P i t r R s` | lviestre?obligeparses?chappitres | luy estre [!] obligé par ses [?] chappitres
L02 | `o C R b e L k q n s ~ f s C A n W y | T b k 4 l F n s d | c s d` | aceqvevovsscavez&qvilfvstconst | a ce que vous [null?] scavez & qu'il fust const-
L03 | `r H 4 8 C t | v X n r g B s W r e R r | + ? L k l z | + R F o 4 r W` | rainctpovrobserverd?evlxdefaire | -raint pour observer d[?]eulx (?) de faire
L04 | `k R 8 4 r ) l L s + i C d s H = J R y | A W 8 d 4 R r L r W s t J` | venirlesdictsalliezaentiereresti | venir les dicts alliez a entiere resti-
L05 | `d n t 4 g 8 | X n H k l d r W # R 8 d | l L e r F H 4 r R l A` | tvtionovavltrementlevrfairela | -tution ou aultrement leur faire la
L06 | `G n W U R 4 l F H C R B g N L # i 8 L | A k c # o 8 C R # L 8` | gverreilfacebonnemineavconmancemen | guerre. Il face bonne mine au commancemen-
L07 | `d | s 4 k i R 8 + r H ) 4 l o C W b n R | 4 L n g n s + i C t y` | tsiviendrailaceqveievovsdictz | -t, s'il viendra; il a ce que je vous dictz;
L08 | `+ L b n X Y 4 H Y A + n W r d J # X 8 + i C d s 4 R n r` | deqvoiiaiadvertimondictsievr | de quoy j'ay adverty mondict sieur
L09 | `l H + # 4 r o l | H F F i 8 b e R | + W l g 8 G n R # H 4 8 | J l` | ladmiralaffinqvedelongvemainil | l'admiral, affin que de longue main il
L10 | `r W G H r + R | A c + n 4 r R | s o | C 7 H r G W | T b n 4 l 8 R` | regardeacondviresacharge&qvilne | regarde a conduire sa charge & qu'il ne
L11 | `l H 4 S W + R e L 8 4 r | s J | H k o 8 d | b n 4 l | v g e U H` | laissedevenirsiavantqvilpovrra | laisse de venir si avant qu'il pourra
L12 | `A k W C b k R s l L + 4 C d | ! H n z o n l d r R s | C 7 g s R` | avecqvesledict?avxavltreschose | avecques ledict [!] aux aultres chose-
L13 | `s v H 8 C o 8 t d r X n k W r + i F J C n l d R W 8 C R s t` | spancanttrovverdificvlteencest | -s, pancant (pensant) trouver dificulté en cest-
L14 | `R C 4 ? T + A k o 8 d H G W l e Y H Y W s C r 4 v d b e R` | eci?&davantagelviaiescriptqve | -eci [sign ?]. & davantage luy ay escript que,
L15 | `s 4 l d r g n k X i t B q 8 b n R 8 g e s d r R + 4 C d` | siltrovvoitbonqvenovstredict | s'il trouvoit bon que nostre dict
L16 | `s H J 8 C t v R r W # H + ? A 8 C A s | X k | + R l H Y H s d` | sainctperemad?ancasovdelaiast | sainct pere m'a d[it?] (?), en cas ou [il] delaiast
L17 | `s X 8 C 7 W # 4 8 q n B 4 W 8 b n R + n d g e t 4 l F R 4 s d` | soncheminovbienqvedvtovtilfeist | son chemin, ou bien que du tout il feist
L18 | `l W # A = o + R W 8 b n R l b e L k 4 = R 4 l R s t q J d` | lemalladeenqvelqvevilleilestoit | le mallade en quelque ville [ou] il estoit,
L19 | `v r R s d H t g n d F H 4 r R T H 4 A c # o 8 C W H C L` | prestatovtfaire&aiaconmanceace | prest a tout faire; & a ja commancé a ce (se)
L20 | `v l H 4 8 + r R | H F F 4 8 | b n R | s 4 l | L s d g J d | B R s g J 8` | plaindreaffinqvesilestoitbesoin | plaindre, affin que, s'il estoit besoin-
L21 | `G | l H C 7 X s W | 8 L s R # B l H s d | s 4 s X e B + o 4 8 R` | glachosenesemblastsisovbdaine | -g, la chose ne semblast si soubdaine.
L22 | `J l | F H i C d | t g n d | l W v X S 4 B l R | d H 8 t | + W v H r g = R` | ilfaicttovtlepossibletantdeparolle | Il faict tout le possible, tant de parolle
L23 | `b e L | v o r s W | # 4 8 i s d r R s | c B J R 8 | b n 4 l y | s q J R 8 d` | qveparseministresconbienqvilzsoient | que par ses ministres, combien qu'ilz soient
L24 | `W 8 | v W n | + W | 8 g # B r R | W 8 | b n 4 | J l | s R F 4 W | v g n r | # R` | enpevdenombreenqviilsefiepovrme | en peu de nombre, en qui il se fie, pour me
L25 | `W 8 d r R t L 8 J r | # W v r 4 H 8 d | l R k X e l g 4 r | d R 8 4 r` | entretenirmepriantlevovloirtenir | entretenir, me priant le vouloir tenir
L26 | `L 8 | l H B g N L | G r A C R | + n | & | ~ ? ~ | T s 4 | J W k R g 4 H` | enlabonnegracedv<P>?&siieveoia | en la bonne grace du [heart = person] [sign ?]; & si je veoia-
L27 | `4 s | b n W | l L + i C d | s J W e r | R k s d | H t r ? 4 C d R r` | isqveledictsievrevstatr?icter | -is que ledict sieur eust a tr[a]icter
L28 | `b n R l b e L | C 7 g s L | H k R C b n R s | l e Y | X e | 4 l Y | v W n` | qvelqvechoseavecqveslviovilipev | quelque chose avecques luy ou il y peu-
L29 | `s d | H k g 4 r | v r g F F i d | X n | + X e # A G W | v g n r` | stavoirproffitovdovmagepovr | -st avoir proffit ou doumage pour
L30 | `l n 8 G | X e | v X e r | l H n l d r R | L 4 R # L | t J R 8 + r g J s` | lvngovpovrlavltreeiemetiendrois | l'ung ou pour l'aultre, e[t?] je me tiendrois
L31 | `s k r | # L s | G H r + R s | # o 4 s | k g Y o 8 d | b n J l | 8 L | + R # o 8` | svrmesgardesmaisvoiantqvilnedeman | sur mes gardes; mais voiant qu'il ne deman-
L32 | `+ W | H k C n 8 L | C 7 g s W | T | b n R | l L + J C d | s 4 W k r | 8 H | o k` | deavcvnechose&qveledictsievrnaav | -de aucune chose & que ledict sieur n'a au-
L33 | `C e 8 L | b e W r R = L | H + L # W s l W r | H k W C b n R s | l e Y` | cvneqverelleademesleravecqveslvi | -cune querelle a demesler avecques luy

## Continuous reading (modernised a little)

[... f. 45v] ... [à] lui être [!] obligé par ses chapitres, à ce que vous savez, et qu'il fût contraint, pour observer d'eux (?),
de faire venir lesdits alliés à entière restitution ou autrement leur faire la guerre. Il fait bonne mine au commencement,
[pour voir] s'il viendra; il a ce que je vous dis. De quoi j'ai averti mondit sieur l'amiral, afin que de longue main il regarde
à conduire sa charge et qu'il ne laisse de venir si avant qu'il pourra avec ledit [!] aux autres choses, pensant trouver
difficulté en celle-ci. Et davantage je lui ai écrit que, s'il trouvait bon, ce que notre dit saint père m'a dit (?), au cas où il
retardât son chemin, ou bien que du tout il fît le malade en quelque ville [où] il était, [il est] prêt à tout faire; et il a
déjà commencé à se plaindre, afin que, s'il était besoin, la chose ne semblât si soudaine. Il fait tout le possible, tant de
parole que par ses ministres, combien qu'ils soient en petit nombre, en qui il se fie, pour m'entretenir, me priant de le
vouloir tenir en la bonne grâce du [♡ = the King?] [sign]. Et si je voyais que ledit sieur eût à traiter quelque chose avec lui
où il pût y avoir profit ou dommage pour l'un ou pour l'autre, je me tiendrais sur mes gardes; mais voyant qu'il ne demande
aucune chose et que ledit sieur n'a aucune querelle à démêler avec lui [... f. 46v]

## English summary

* Someone (probably the Emperor, if `!` is his sign) is bound by his "chapters", i.e. treaty articles, to force the allies to make full
  restitution or else go to war with them. He is putting a good face on it for now, waiting to see whether "he" will come.
* Gramont has told "the Admiral" to prepare his charge well in advance and to come as far forward as he can.
* He has also written that, if the Pope agreed, the traveller could delay his journey or even pretend to be ill in whatever town he was
  in. "He" is ready to do anything and has already started complaining (of illness), so that the move would not look sudden if needed.
* "He" (apparently the Pope) does all he can, by word and through his few trusted ministers, to keep Gramont close, and asks to be
  kept in the good grace of the [heart-sign person, presumably the King].
* Gramont would be on his guard if the two parties had business that could profit or harm either of them. But since "he" asks for nothing
  and "ledict sieur" has no quarrel with him, [the sentence continues on f. 46v].
* The referents rest on the unidentified `!` sign and on the pronouns, so read them as a hypothesis. The reference to the
  Emperor's allies being made to restore (Cambrai/Barcelona terms) and to someone's advance towards Bologna fits October 1529.
