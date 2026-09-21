# Pilot: shape-true re-transcription + decode, measured
Files: trans.txt (sign-by-sign transcriptions), shapedec.py (direct key map + 5-gram lattice, fr-1600-letters),
pilot_lines.md (per line: signs / ref / old+LM / new direct / new+LM with error counts), catalogue.md/png.
Reference strings = the same refs calib.py uses (readers' readings checked against the clear copies/margin); old numbers
recomputed on exactly these lines from work_cluster/calib.py (w_emit=2, bonus=1.5).

| subset | chars | old alias argmax | old alias + LM | new shape direct | new shape + LM |
|---|---|---|---|---|---|
| R4234 P16 (13 l.), P19-20 (6 l.), R4235 P8D (4 l.) | 791 | 14.5% | 9.2% | 6.8% | **5.8%** |
| R4240 l.1-2 only | 50 | 30% | 30% | 12% | **8%** |

Residual errors (new+LM, 46 on the 791-char set): about 12 are reference artefacts (C2 ref stops before the
last word "[est]oit arrive" which the signs carry; L6 ref drops the scribe's "den" before the deleted run; L4
"pur" for "pour" is what is written), leaving ~4.3% genuine: 7/B, 4/27, 5-as-S ("sand", "sorie"), dropped letters.

Caveat (contamination): the readers' readings for P15-P20 and P8D were displayed to me before transcribing
(while locating lines), so the transcriptions are not strictly blind. I transcribed by shape and kept what I saw
(e.g. "pur", "den", "sand", "lion", "nulce"), but the numbers should be treated as optimistic by perhaps 1-2 points.
R4240: only lines 1-2 were done; the page is warped and each line needs individual crop fitting (the other 24 not done).
### R4234_P16_L4 (R4234_P15-P20:21)
- signs: `I nE {Y|A+|n*} I# | Gh R27 A+ N7 Tg | Pc Um R27 | Q Up Eo`
- ref:        iaygrantpourque
- old+LM:     irierantpureque  (5 err)
- new direct: iyigrantpurque  (3 err)
- new+LM:     iaigrantpurque  (2 err)

### R4234_P16_L5 (R4234_P15-P20:23)
- signs: `Lx E9 Sinf | N7 Of Um Uv Eo LL E9 Sinf | Q Up I | Of N7 Tg | Eo Sinf Tx E9 | Eo S6 C4 R27 I Pc Tg Eo Sinf | Pn A3 Rr | D5 Eo C4 A+`
- ref:        lesnouuellesquimontesteescriptespardeca
- old+LM:     lesnouuellesquiontesteescriptespardeca  (1 err)
- new direct: lesnouuellesquiontesteescriptespardeca  (1 err)
- new+LM:     lesnouuellesquiontesteescriptespardeca  (1 err)

### R4234_P16_L6 (R4234_P15-P20:25)
- signs: `Q Up E9 | 40 | A3 | D5 Eo | N7 Of Um Uv Eo A+ Up | D5 E9 N7 ~ ~ ~ ~ ~ ~ | Mq A3 N7 D5 Eo | A+ Up | C4 L10 Eo Rr Gh Eo | D5 Eb S6 Of N7`
- ref:        queroyadenouueaumandeauclergedeson
- old+LM:     iqueroyadenouueaudenuouuusmandeauclergedeson  (10 err)
- new direct: queroyadenouueaudenmandeauclergedeson  (3 err)
- new+LM:     queroyadenouueaudermandeauclergedeson  (3 err)

### R4234_P16_L7 (R4234_P15-P20:27)
- signs: `Rr Of I# A8 Um Mq Eo | Tg R27 Of I# S6 | D5 Eo C4 I Mq Eo Sinf | Up E9 N7 {Up|F} Eo Sinf | A+ | L10 A3 | N7 Of Tg I C4 Eo | D5 Eo`
- ref:        roiaumetroisdecimesuenuesalanoticede
- old+LM:     royaumetroisdecimesuenuesalanoticede  (1 err)
- new direct: roiaumetroisdecimesuenuesalanoticede  (0 err)
- new+LM:     roiaumetroisdecimesuenuesalanoticede  (0 err)

### R4234_P16_L8 (R4234_P15-P20:29)
- signs: `S6 A+ Sinf A3 I N7 C4 Tg Eo Tx E9 | ET | I {Up|Of} I N7 C4 Tg | Lx Eo S6 | Tg Rr OD I# S6 | A+ Um Tg R27 Eo S6 | Lx E9 Up Eo E9 S6`
- ref:        sasaincteteetioinctlestroisautresleuees
- old+LM:     sasaincteteetioinctlestroisautresleuees  (0 err)
- new direct: sasaincteteetiuinctlestroisautresleuees  (1 err)
- new+LM:     sasaincteteetioinctlestroisautresleuees  (0 err)

### R4234_P16_L9 (R4234_P15-P20:31)
- signs: `Lx A+ N7 Nx Eo Eb | Pc A+ {S6|Tg} Eo E9 | S6 A+ N7 | D5 L10 Of C4 Tg Rr Of I# | D5 I C4 Eo LL E9 | S6 A+ Sinf A3 I N7 A+ Tg Eo Tx E9`
- ref:        lanneepasseesansloctroidicellesasainctete
- old+LM:     lanneepasseesandloctroydicellesasainatete  (3 err)
- new direct: lanneepaseesandloctroidicellesasainatete  (3 err)
- new+LM:     lanneepaseesandloctroidicellesasaintete  (3 err)

### R4234_P16_L10 (R4234_P15-P20:33)
- signs: `ET | A+ Pc S6 I | L10 A+ | C4 A3 L10 Up {Mq|E9} N7 I# Eo | D5 Up | Tg Um R27 C4 | S6 Of I Eo N7 Tg | Pc OD Um R27 | Lx Up I#`
- ref:        etaussilacalomnieduturcsoientpourluy
- old+LM:     etausilacalomnieduturcsoientpourluy  (1 err)
- new direct: etapsilacalumnieduturcsoientpourlui  (4 err)
- new+LM:     etapsilacalomnieduturcsoientpourlui  (3 err)

### R4234_P16_L11 (R4234_P15-P20:35)
- signs: `F A+ I R27 Eo | Pc R27 A+ N7 D5 R27 Eo | Lx OD C4 A3 S6 I OD N7 | D5 Eo | Sinf E9 | D5 Eo C4 L10 A3 Rr E9 R27 | C4 Of N7 Tg R27 E9`
- ref:        faireprendrelocasiondesedeclarercontre
- old+LM:     faireprandrelocasiondesedeclarencontre  (2 err)
- new direct: faireprandrelocasiondesedeclarercontre  (1 err)
- new+LM:     faireprandrelocasiondesedeclarercontre  (1 err)

### R4234_P16_L12 (R4234_P15-P20:37)
- signs: `Lx Eo D5 I C4 Tg | S6 Eo I Gh N7 Eo Um R27 | {Of|Up} Um I L10 | Tg Rr OD Um Up Eo Pn Of I Tg | Lx E9 Up Eo N7 Tg`
- ref:        ledictseigneurouiltrouueroitleuent
- old+LM:     ledictseigneurouiltrouueuoitleuent  (1 err)
- new direct: ledictseigneurouiltrouuepoitleuent  (1 err)
- new+LM:     ledictseigneurouiltrouueroitleuent  (0 err)

### R4234_P16_L13 (R4234_P15-P20:39)
- signs: `{A+|Pn} Gh R27 Eo | Eb N7 Up E9 Rr S6 | 20 | Q Um A+ N7 Tg | A+ Um X | C4 H Of S6 Eo Sinf | D5 Eo SS Up S6 D5 I C4 Tg E9`
- ref:        agreenuerslempereurquantauxchosesdessusdictes
- old+LM:     uereenuerslempereurquantauechosesdessusdicte  (4 err)
- new direct: agreenuerslempereurquantauxchosesdessusdicte  (1 err)
- new+LM:     agreenuerslempereurquantauxchosesdessusdicte  (1 err)

### R4234_P16_L14 (R4234_P15-P20:41)
- signs: `Sinf I Eo | Up Of Um S6 | A+ I# | N7 I Eo N7 | Up Of Um Lx Up | Eo S6 C4 R27 I Pn R27 Eo | Tg Of Um Tx | C4 Eo | Q Up E9`
- ref:        ieuousaibienuouluescripretoutceque
- old+LM:     sieuousaybienuouluescriretoutceque  (3 err)
- new direct: sieuousainienuouluescripretoutceque  (2 err)
- new+LM:     sieuousainienuouluescripretoutceque  (2 err)

### R4234_P16_L19 (R4234_P15-P20:50)
- signs: `Up N7 Eo | L10 E9 C4 Tg R27 Eo | E9 N7 | C4 H I F R27 Eo | Q Up E9 | I Eo | Pc Um I# S6 Eo | Mq Of N7 D5 Tg Rr E9 Rr`
- ref:        unelectreenchifrequeiepuissemonstrer
- old+LM:     unelentreencorequeiepuisemontre  (7 err)
- new direct: unelectreenchifrequeiepuisemondtrer  (2 err)
- new+LM:     unelectreenchifrequeiepuisemonstrer  (1 err)

### R4234_P16_L20 (R4234_P15-P20:52)
- signs: `A+ Um Rr | D5 Eo SS Um S6 D5 I C4 Tg {S6|n*} | C4 E9 Sinf A+ N7 Eo | D5 Eo Lx Of D5 Eo S6 | ET | S6 Eo N7 Of I# S6 | C4 Of Mq`
- ref:        auxdessusdictzcesantdelodesetsenoiscom
- old+LM:     audessusdictzcesanedelodesetsenuiscom  (3 err)
- new direct: aurdessusdictscesanedelodesetsenoiscom  (3 err)
- new+LM:     audessusdictscesanedelodesetseroiscom  (4 err)

### R4234_P19_C1 (R4234_P15-P20:93)
- signs: `Lx E9 D5 I C4 Tg | Rr D5 Of R27 I# Eo | Eb S6 Tg | A+ D5 Up Eo R27 Tg I#`
- ref:        ledictdorieestaduerti
- old+LM:     ledictedurieestaduerti  (2 err)
- new direct: ledictrdorieestaduerti  (1 err)
- new+LM:     ledictsorieestaduerti  (1 err)

### R4234_P19_C2 (R4234_P15-P20:94)
- signs: `Tx A+ N7 Tx | D5 Eo Mq A3 Rr S6 Eo I LL E9 | Q Up Eo | D5 Eo Lx I# Of N7 | Q Up I L10 E9 Sinf Tg | Of I Tx A+ RR I Up E9`
- ref:        tantdemarseillequedelyonquilest
- old+LM:     mandemarseillequedelyonquilestoisauie  (9 err)
- new direct: tantdemarseillequedelionquilestoitarriue  (10 err)
- new+LM:     tantdemarseillequedelionquilestoitarriue  (10 err)

### R4234_P19_C5 (R4234_P15-P20:100)
- signs: `A+ Lx A3 | C4 {Of|Pn} Um R27 Tg | Pc A3 Rr | Lx Eo | N7 A+ R27 Of N7 | D5 Eo | S6 A3 I N7 C4 Tg | N7 L10 A3 N7 C4 A+ Rr Tg | ET`
- ref:        alacourtparlebarondesainctblancartet
- old+LM:     alacourtparlenabarondesainctblancartet  (2 err)
- new direct: alacourtparlenarondesainctnlancartet  (2 err)
- new+LM:     alacourtparlebarondesainctblancartet  (0 err)

### R4234_P19_C6 (R4234_P15-P20:102)
- signs: `Q Up E9 | Lx Eo | D5 I C4 Tg | D5 Of Rr I# Eo | Lx E9 Sinf | Pc Eo Rr E9 | Pc R27 A+ N7 D5 Rr Eo | A+ Up | R27 Eo Tg Of Um N7`
- ref:        queledictdorielesespereprendreauretourn
- old+LM:     queledictduielespereprandreauretoun  (6 err)
- new direct: queledictdorielespereprandreauretoun  (4 err)
- new+LM:     queledictsorielespereprandreauretoun  (5 err)

### R4234_P20_C7 (R4234_P15-P20:107)
- signs: `F A+ I Gh N7 Eo | Uv OD Um Lx Of I R27`
- ref:        faigneuouloir
- old+LM:     maigneuoulur  (3 err)
- new direct: faigneuouloir  (0 err)
- new+LM:     faigneuouloir  (0 err)

### R4234_P20_C8 (R4234_P15-P20:108)
- signs: `LL E9 C4 Eo | N7 E9 | Sinf Pc A+ I Gh N7 Eo Rr`
- ref:        allerenespaigne
- old+LM:     llecenespaigne  (2 err)
- new direct: llecenespaigner  (3 err)
- new+LM:     llecenespaigner  (3 err)

### R4235_P8_L1 (R4235_P8D:8)
- signs: `S6 Rr I | 40 | Eo S6 Tg | F Of R27 Tx | Eo N7 | I Tg A+ Lx I Eo | D5 Up | C4 Of S6 Tx Eo | D5 E9 | Lx Of Mq N7 A+ {N7|R27} D5 I Eo | {F|Pn} A3 C4 I`
- ref:        siroyestfortenitalieducostedelombardeefaci
- old+LM:     sriroyestfortenitalieducostedelumnandeepari  (6 err)
- new direct: sriroyestfortenitalieducostedelomnandiefaci  (4 err)
- new+LM:     sriroyestfortenitalieducostedelomnandiefaci  (4 err)

### R4235_P8_L2 (R4235_P8D:11)
- signs: `LL Eo Mq E9 N7 Tg | Lx Eo | D5 I C4 Tx | Eo Sinf Tg A+ Tx | {Q|n*} D5 Eo | F L10 OD R27 Eo N7 C4 Eo | S6 E9 | Pc OD Um RR A+ Rr | Eo D5 Up`
- ref:        llementledictestatdeflorencesepourraedu
- old+LM:     llementledictestatdeflorencesepourraredu  (1 err)
- new direct: llementledictestatqdeflorencesepourraredu  (2 err)
- new+LM:     llementledictestatdeflorencesepourraredu  (1 err)

### R4235_P8_L3 (R4235_P8D:13)
- signs: `I# R27 Eo | E9 N7 | Lx A+ N7 C4 I Eo N7 Nx Eo | Lx I N7 Eo {C4|R27} Tx Eo | ET | D5 Eo Up {Of|Up} Tg I OD N7 | D5 Up D5 I C4 Tx | S6 Eo I Gh`
- ref:        ireenlancienneliberteetdeuotiondudictseig
- old+LM:     ireenlancienneliberteetdeuotiondudictseig  (0 err)
- new direct: ireenlanciennelinecteetdeuotiondudictseig  (2 err)
- new+LM:     ireenlancienneliberteetdeuotiondudictseig  (0 err)

### R4235_P8_L4 (R4235_P8D:15)
- signs: `N7 Eo {Uv|Um} R27 | 40 | C4 A+ R27 | Eo S6 Tg A3 N7 Tx | Eo Mq Pc E9 C4 H Eo | 20 | D5 Up | C4 Of S6 Tx Eo | D5 E9 | Lx A+ D5 I C4 Tx Eo`
- ref:        neurroycarestantempeschelempereurducostedeladicte
- old+LM:     neurroycarestantempechelempereurducostedeladicte  (1 err)
- new direct: neurroycarestantempechelempereurducostedeladicte  (1 err)
- new+LM:     neurroycarestantempechelempereurducostedeladicte  (1 err)

### R4240_L1 (R4240:20)
- signs: `Rr nE Uv E9 R27 Gh Eb R27 I ? Um Sinf | Q Up I`
- ref:        uergeriusqui
- old+LM:     uueetquemo  (9 err)
- new direct: ruergerixusqui  (2 err)
- new+LM:     ruergeriiusqui  (2 err)

### R4240_L2 (R4240:21)
- signs: `Eo S6 Tg OD I Tx | B Uv Lx C4 Eo | D5 Up F Eo Uv | Pc A3 Pn Eo | C4 L10 E9 Mq Eo Lx Tg | ET | D5 Eo Pc Uv I# S6 | C4 OD Lx`
- ref:        estoitnuncedufeupapeclementetdepuiscon
- old+LM:     estoituercedufeupaperlemetetdepuisco  (6 err)
- new direct: estoitbulcedufeupapeclemeltetdepuiscol  (4 err)
- new+LM:     estoitnulcedufeupapeclementetdepuiscol  (2 err)
