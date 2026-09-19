# Vestigia 2831 p.3 (Buda 22 Nov 1489) - lines 15-28, SECOND PASS

Method note. The boxed strips in `seg/strips2/` could not be used as they stand: for these lines the
line-segmentation in `seg/v2831p3_glyphs.json` is itself wrong at the left margin. For line 15 the boxes
0-11 (x 157-453) sit on the row BELOW (line 16), and only from box 12 (x 455) on does the list follow
line 15; line 16's boxes 0-11 likewise sit on line 17's row; several boxes (l.15 nos. 7, 9, 10, 11) are
merged components spanning two rows. So the same drift that spoiled the first pass is baked into the
box list.

Instead the rows were re-found by an ink projection profile in five x-blocks and each line was
de-skewed into a straight strip (script kept out of the repo). Positions below are therefore the
**x coordinate on the page** (same frame as seg/v2831p3_glyphs.json: src img/v2831_p3r.jpg, offset
[900,870]), which is exact and reproducible, not a box index. Row centres used (x = 270/610/950/1290/1630):
L15 999/1008/1030/1037/1038, L16 1064/1082/1098/1116/1118, L17 1133/1153/1170/1186/1197,
L18 1204/1223/1240/1268/1267, L19 1273/1286/1317/1334/1344, L20 1347/1362/1390/1403/1405,
L21 1419/1436/1458/1473/1482, L22 1486/1504/1528/1547/1555, L23 1540/1566/1587/1611/1622,
L24 1606/1633/1647/1684/1695, L25 1676/1694/1722/1747/1767, L26 1748/1765/1789/1817/1830,
L27 1822/1837/1863/1889/1900, L28 1884/1896/1929/1952/1966.

New sign values settled in this pass:
- plain round **o** (no bar) = **b**: "habia" (L15 9-r-o-n-r), "deliberatione" (L16 x-//-d-n-o-q-q^a-o--n-e-b^e).
  The bar is what makes it t; the first pass's "epsilon for b" was this unbarred o.
- **i (dotted / short stroke)** = a inside words: "mandare" = a-r-g-x-i-q^e (L15).
- the ss ligature is **one** sign (n + crossed 4); the "4" is part of it, not a following e.

L15: [s/l]ia[?] i[?]usse ita[?], che p-o-a-i-[n^o][?]-a-re-re[?] che [1-2 signs under an ink blot] [♀] u[?] habia dicto de volerlo mandare piu / (L16) presto
 signs (page x): 162 d(s or l) | 190 n=i | 222 r=a | 250 n=i | 300 6=u | 330 n+4=ss | 382 4=e | 415 n=i | 432 p-str=t | 462 r=a | 495 ÷ null | 518 s=c | 540 9=h | 560 //=e  ("che") | 585 c=p | 610 eps=o | 648 r=a | 675 n=i + raised o with a bar (one group, unidentified) | 706 /=? | 725 q^e=re | 772 q^e=re | 810 s=c | 838 9=h | 868 //=e ("che") | 885-915 BLOT (1-2 signs lost) | 925 r-str with a small o below (the "♀" sign, unidentified) | 962 6=u | 995 9=h | 1010 r=a | 1035 o (unbarred) = b | 1060 n=i | 1078 r=a  ("habia") | 1105 x=d | 1125 n=i | 1148 s=c | 1170 o-bar=t | 1195 3=o  ("dicto") | 1218 x=d | 1240 //=e  ("de") | 1278 6=v | 1308 eps=o | 1338 d=l | 1358 //=e | 1380 z=r | 1405 d=l | 1432 3=o  ("volerlo") | 1462 a=m | 1492 r=a | 1512 g=n | 1540 x=d | 1568 i(dotted)=a | 1588 q^e=re  ("mandare") | 1632 c=p | 1652 n=i | 1668 6=u  ("piu") | 1700 w null
 (new: "mandare" - the first pass's unread "m-a-n-?-i-re"; the x=d and dotted i=a make it certain.)

L16: presto per tentarlo, che per deliberatione, et cosi se ne restara [b^e-] pa[ss]e[?] ...
 signs (page x): 160 c=p | 188 z=r | 218 //=e | 252 d + 285 o-bar = st | 318 3=o  ("presto") | 352 c=p | 382 //=e | 408 z=r  ("per") | 440 o-bar=t | 472 //=e | 498 g=n | 528 o-bar=t | 552 r=a | 578 z=r | 568 d=l | 598 3=o  ("tentarlo") | 622 s=c | 648 9=h | 672 //=e  ("che") | 698 c=p | 718 //=e | 742 z=r  ("per") | 778 x=d | 808 //=e | 832 d=l | 858 n=i | 882 o (unbarred) = b | 905 q=e | 935 q^a=ra | 968 o-bar=t | 998 n=i | 1022 eps=o | 1052 b^e=ne  ("deliberatione") | 1108 r-str=et | 1152 b=co | 1188 m^o=si  ("cosi") | 1235 m^e=se | 1275 b^e=ne | 1370 //=e | 1390 z=r | 1405 d + 1430 o-bar = st | 1458 r=a | 1485 q^a=ra  ("restara") | 1518 b^e with a long macron (the open "b^e-" sign) | 1580 c=p | 1605 r=a | 1645 n+4=ss | 1672 4=e | 1700 q=e
 (the last group resists: p-a-ss-e-e; "q" may be a q^e whose superscript has faded.)

L17: ...ro, et dice ancora che ad [q^s x̄] non havera ad dimorare piu che octo di, o dece al piu, et
 signs (page x): 155 q^s=ro | 190 x-bar=et | 235 x=d | 258 n=i | 288 s=c | 310 //=e  ("dice") | 332 r=a | 355 g=n | 385 b with macron = co | 418 q^a=ra  ("ancora") | 448 s=c | 472 9=h | 498 //=e  ("che") | 520 r=a | 538 x=d  ("ad") | 552 q^s=ro | 580 x-bar=et | 618 v=n | 648 eps=o | 672 g=n  ("non") | 705 9=h | 738 r=a | 762 6=v | 785 //=e | 810 q^a=ra  ("havera") | 848 r=a | 872 x=d  ("ad") | 898 x=d | 922 n=i | 948 a=m | 968 3=o | 990 q^a=ra | 1020 q^e=re  ("dimorare") | 1062 c=p | 1088 n=i | 1112 6=u  ("piu") | 1138 s=c | 1162 9=h | 1185 //=e  ("che") | 1208 eps=o | 1238 s=c | 1265 o-bar=t | 1292 3=o  ("octo") | 1322 x=d | 1348 n=i  ("di") | 1385 3=o  ("o") | 1408 x=d | 1438 //=e | 1470 b-stroked with dot = ce  ("dece") | 1508 r=a | 1535 d=l  ("al") | 1562 c=p | 1590 n=i | 1618 6=u  ("piu") | 1655 x-stroked=et
 (gains over the first pass: "ancora" for the unread "r̸ b^a a" - the 4th sign is q^a=ra, not b^a=na;
  and the whole line-end, which the first pass left as "x n 3 x // b̶· r d c n b x̸", is
  "di, o dece al piu, et" - so the unexplained recurring group "c n b" is really "c n 6" = "piu".
  "q^s x̄" (ro+et) stands twice more here in positions that want a place-name - "ad [X] non havera
  ad dimorare piu che octo di" - so it is probably a nomenclator, not ro+et.)

L18: che vole affretare el camino per trovarsi presto con la [1 sign] [l-e-n-m-a?] a la quale.
 signs (page x): 158 s=c | 182 9=h | 208 //=e  ("che") | 242 6=v | 268 eps=o | 298 d=l | 322 //=e  ("vole") | 352 r=a | 378 n+p-str = ff | 408 z=r | 432 //=e | 458 o-bar=t | 488 r=a | 548 q^e=re  ("affretare") | 575 q=e | 608 d=l  ("el") | 640 b-stroked=ca | 692 a=m | 725 n=i | 755 b^o=no  ("camino") | 792 c=p | 818 //=e | 845 z=r  ("per") | 875 o-bar=t | 905 z=r | 930 eps=o | 958 6=v | 968 r=a | 992 z=r | 1025 m^o=si  ("trovarsi") | 1065 c=p | 1090 z=r | 1118 //=e | 1145 d + 1175 o-bar = st | 1205 3=o  ("presto") | 1238 s=c | 1262 eps=o | 1292 g=n  ("con") | 1325 d=l | 1345 r=a  ("la") | 1365-1415 one sign: a round head with a long crossbar (like the et sign) - unread | 1440 d=l | 1468 //=e | 1495 g=n | 1520 a=m with a long bar | 1558 r=a | 1585 d=l | 1620 r=a  ("la") | 1655 ) crescent = q | 1698 s=u | 1730 r=a | 1760 d=l | 1788 //=e  ("quale") | final dot
 (gains: the first pass's unread tail "c e 4 | d z 4 | d n 8 q̈ z | d z 3 s z d //" is really
  "…a la quale."; the crescent ")" = q followed by small s = u gives "quale", which the drifted
  crops had turned into "d z 3 s z d". Only the two signs at 1365-1415 and the word at 1440-1558
  are still open.)

L19: gli pare essere stato [m-i-l-a-a-ss-que-i-o?] che havera [ca][ra/re] ad [q^s x̄] dice essere i[n]
 signs (page x): 152 8=g | 185 d=l | 210 n=i  ("gli") | 238 c=p | 258 r=a | 288 q^e=re  ("pare") | 320 //=e | 345 n+4=ss | 390 4=e | 415 q^e=re  ("essere") | 455 d + 490 o-bar = st | 518 r=a | 538 p-str=t | 562 3=o  ("stato") | 600 a=m | 645 n=i | 672 d=l | 700 f=a | 730 r=a | 755 n+4=ss (the crossed 4 runs to 810) | 822 ) crescent with a dot = q | 850 s=u | 878 //=e | 908 n=i (with a long macron) | 938 eps=o | 968 3=o | 995 s=c | 1020 9=h | 1048 //=e  ("che") | 1080 9=h | 1110 r=a | 1138 6=v | 1162 //=e | 1185 q^a=ra  ("havera") | 1205 b-stroked=ca | 1245 q^a (or q^e) = ra/re | 1278 r=a | 1305 x=d  ("ad") | 1335 q^s=ro | 1368 x-bar=et | 1390 x=d | 1408 n=i | 1428 s=c | 1450 4=e  ("dice") | 1478 4=e | 1512 n+4=ss | 1565 //=e | 1592 q^e=re  ("essere") | 1645 n=i | 1675 g=n
 (confirmed: "gli pare essere stato"; "dice essere in-" at the end. The stretch at 600-950 still
  resists: it reads m-i-l-a-a-ss-, then a clear ") s //" = "que". The third "q^s x̄" of the page
  stands here, again right after "ad".)

L20: ...care[?] intendere al [ca?] la singulare observantia de questo M: (Ser.mo Re de Hungaria) verso la [co-n-t-i-te?] et
 signs (page x): 150 b-stroked=ca | 188 z=r | 215 //=e | 245 n=i | 272 v=n | 300 o-bar=t | 330 //=e | 360 g=n | 390 x=d | 415 4=e | 442 q^e=re  ("intendere") | 478 r=a | 505 d=l  ("al") | 542 b-stroked=ca (one sign, uncertain) | 578 d=l | 600 r=a  ("la") | 628 d (straight) = s | 660 n with a tilde = in | 695 8=g | 725 6=u | 752 d=l | 778 r=a | 805 q^e=re  ("singulare") | 838 o (unbarred) = b | 868 d (straight) = s | 898 //=e | 928 z=r | 960 6=u | 990 r=a | 1015 g=n | 1030 o-bar=t | 1058 n=i | 1085 r=a  ("[o]bservantia") | 1145 x=d | 1175 //=e  ("de") | 1205 ) crescent with a dot = q | 1238 s=u | 1262 //=e | 1290 d + 1320 o-bar = st | 1350 3=o  ("questo") | 1378 M: = Ser.mo Re de Hungaria | 1400 6=v | 1428 //=e | 1470 z=r | 1505 m^u=so  ("verso") | 1558 d=l | 1585 r=a  ("la") | 1605 b=co | 1635 n=i | 1655 g=n | 1682 o-bar=t | 1708 n=i | 1738 L:=te | 1770 x-stroked=et
 (the big gain here: "la singulare observantia de questo Ser.mo Re verso la ..." - stock chancery
  phrasing that the first pass had as the unread runs "d ñ 8 6 d r q^e", "e e d // z 3",
  "6 z e a v z". "intendere" and "questo" and the M: nomenclator confirm the line.)

L21: sua, con prome[?]... [c-l-i-ss-?-t?] conveniente ad questo effecto, per disponer[e/a] la
 signs (page x): 150 d (straight) = s | 180 s with a dot = u | 208 r=a  ("sua") | 238 s=c | 265 eps=o | 295 v=n  ("con") | 312 c=p | 348 z=r | 382 eps=o | 415 a=m | 448 //=e  ("prome-") | 478 r=a | 505 a with a long bar (same sign as L18 x1520, unidentified) | 515 c=p | 552 d=l | 590 n=i | 625 n+4=ss | 668 7/long-s = ? | 695 p-str=t | 742 s=c | 772 eps=o | 800 v=n | 828 6=v | 855 //=e | 882 g=n | 908 n=i | 930 4=e | 952 v=n | 975 L:=te  ("conveniente") | 968 r=a | 998 x=d  ("ad") | 1032 ) crescent = q | 1060 s=u | 1088 //=e | 1112 d + 1142 o-bar = st | 1172 3=o  ("questo") | 1205 4=e | 1238 n+p-str = ff | 1275 //=e | 1305 s=c | 1332 o-bar=t | 1362 3=o  ("effecto") | 1398 c=p | 1422 //=e | 1450 z=r  ("per") | 1490 x=d | 1518 n=i | 1555 d (straight) = s | 1585 c=p | 1615 eps=o | 1645 8=n | 1675 q^a=ra | 1705 z=r | 1735 d=l | 1762 r=a  ("la")
 (gains: "prome[…]" (p-r-o-m-e) at 312-448, which the first pass had as the unread "c z z e a //";
  "conveniente ad questo effecto" confirmed; and the line-end run the first pass gave as
  "d s e c q^a z" is "d-i-s-p-o-n-ra-r", i.e. "per disponer(e/a) la".)

L22: et l[i]o[?] in la, et tena[?] del Turco, f-r-a-t-e-[ne?] ... il Turco, dopoi [i]n parlare in ca[u?]o[?]
 signs (page x): 150 x-stroked=et | 195 d=l | 222 n=i | 252 3=o | 288 n=i | 315 v=n | 348 d=l | 372 r=a  ("la") | 405 x-bar=et | 435 o-bar=t | 462 //=e | 492 g=n | 522 r=a | 550 x=d | 572 //=e  ("de") | 600 d=l | 632 p-str=t | 668 6=u | 702 z=r | 735 b=co  ("[de]l Turco") | 768 7=f | 808 z=r | 842 r=a | 870 o-bar=t | 895 //=e | 925 b^e/n^e = ne | 968 eps=o | 1000 x=d | 1025 r=a | 1038 n=i | 1058 d=l | 1092 p-str=t | 1122 6=u | 1155 z=r | 1188 b=co  ("il Turco") | 1222 x=d | 1255 eps=o | 1285 c=p | 1312 eps=o | 1342 n=i  ("dopoi") | 1375 n=i | 1398 8=n | 1428 c=p | 1452 r=a | 1480 z=r | 1510 d=l | 1538 n=i(?a) | 1565 q^e=re  ("par(l)are" or "dire") | 1600 n=i | 1628 8=n  ("in") | 1662 b-stroked=ca | 1698 6=u | 1722 eps=o | 1750 q=e
 (the find here is the two occurrences of "Turco": "d p-str 6 z b" = l-t-u-r-co after "x //" = de
  ("del Turco"), and "n d p-str 6 z b" = i-l-t-u-r-co ("il Turco"). The first pass had these as
  "d c e 6 3 b" and "e x n d e 6 z b". "dopoi" (x eps c eps n) also recurs here.)

L23: del re Ferdinando galiardamente, et co[n] tale modest[i]a che convi[e]ne a li e[?]
 signs (page x): 148 x=d | 178 //=e | 208 d=l  ("del") | 238 z=r | 268 //=e  ("re") | 302 7=f | 332 //=e | 358 z=r | 388 x=d | 415 n=i | 442 v=n | 472 r=a | 500 g=n | 528 x=d | 552 eps=o  ("Ferdinando") | 560 8=g | 582 r=a | 608 d=l | 638 n=i | 668 r=a | 695 z=r | 725 x=d | 755 r=a | 782 a=m | 808 //=e | 835 8=n | 865 L:=te  ("galiardamente") | 895 x-stroked=et | 925 s=c | 952 eps=o  ("co[n]") | 975 o-bar=t | 1002 r=a | 1028 d=l | 1058 //=e  ("tale") | 1092 a=m | 1122 eps=o | 1152 x=d | 1182 //=e | 1212 d + 1245 o-bar = st | 1278 g=n(?) | 1305 r=a  ("modest[i]a") | 1338 s=c | 1362 9=h | 1388 //=e  ("che") | 1398 s=c | 1420 eps=o | 1452 v=n | 1488 6=v | 1520 n=i | 1545 g=n | 1578 q=e  ("convi[e]ne") | 1608 r=a | 1635 r=a | 1662 d=l | 1690 n=i | 1718 //=e
 (big gain: the first pass had only "del re Ferdinando" here and left the rest unread. The line is
  "…galiardamente, et co[n] tale modest[i]a che convi[e]ne a li…" - the long run the first pass
  gave as "e 8 z d n | z z x r | z r | // 8 d n" is the adverb "galiardamente".)

L24: na[?]re[?] d'animo, de [?]ntilce[?] da se ... conte[?] ... [-]tione in [?] ... lo, de le
 signs (page x): 152 b^a=na | 195 q^e/q^s | 235 x=d | 265 r=a | 295 v=n | 328 n=i | 355 a=m | 385 3=o  ("d'animo") | 415 x=d | 442 //=e  ("de") | 470 c/eps | 512 v=n | 545 o-bar=t | 578 n=i | 612 d with a long bar = l(?) | 652 s=c | 680 //=e | 715 x=d | 748 r=a  ("da") | 785 m^e=se  ("se") | 830 - null | 865 b=co | 890 v=n | 928 o-bar=t | 958 //=e  ("conte"?) | 975 z=r | 1002 o-bar=t | 1030 n=i | 1058 eps=o  ("-tio-") | 1088 n=i | 1118 g=n | 1152 n=i | 1182 6=u | 1212 d=l | 1242 eps=o | 1272 n=i | 1302 d=l | 1340 b-stroked with a dot = ce | 1395 3=o | 1425 //=e | 1452 d=l | 1482 3=o  ("lo") | 1520 + null | 1560 x=d | 1595 //=e  ("de") | 1622 d=l | 1652 //=e  ("le") | 1690 ÷ null
 (gain: "d'animo" (x + r v n a 3) at 235-385, which the first pass had as the unread "x z 8 n r 3";
  "da se"; the rest of the line is still largely unread.)

L25: [ce?]l na[?]a[n]... che li sono date[?] apresso el [o-i-t-e-r-e?] ... d[i]o[?] lo li
 signs (page x): 152 b-stroked with a dot = ce | 188 d=l | 222 b^a=na | 255 r=a | 282 v=n | 312 n with a tilde = in | 350 //=e | 385 w null | 418 s=c | 445 9=h | 470 //=e  ("che") | 498 d=l | 522 n=i  ("li") | 555 m^u=so | 588 b^o=no  ("sono") | 625 x=d | 652 r=a | 682 L:=te  ("date") | 718 r=a | 745 c=p | 775 z=r | 802 //=e | 828 n=i | 858 n+4=ss | 895 eps=o  ("apresso") | 925 4=e | 952 d=l  ("el") | 982 eps=o | 1008 n=i | 1038 p-str=t | 1070 //=e | 1100 z=r | 1130 q=e | 1160 6=u | 1188 v=n | 1215 x=d | 1245 eps=o | 1272 d=l | 1300 n=i | 1330 x=d | 1360 //=e | 1388 r=a | 1430 x=d | 1458 n=i | 1485 3=o | 1515 d=l | 1542 3=o  ("lo") | 1570 d=l | 1598 n=i  ("li") | 1635 ÷ null | 1672 b-stroked | 1705 c=p
 (gains: "che li sono date apresso el …"; the first pass's "z 4 z // n r 4 e" resolves as
  "a-p-r-e-i-ss-o" = "apresso", and "L:" before it is "te", giving "date".)

L26: volendo la Santita[?] sua per [f-?-r-l-i-p-n-u?] ... [i]ara di la, in voce [?] ... sua [l-a-o-u-a-d-e?]
 signs (page x): 142 6=v | 172 eps=o | 205 d=l | 240 q=e | 278 v=n | 308 x=d | 340 eps=o  ("volendo") | 375 d=l | 402 r=a  ("la") | 435 d (straight) = s | 465 r=a | 492 v=n | 518 o-bar=t | 542 n=i | 568 L^a=ta  ("Santita"?) | 555 d (straight) = s | 582 s with a dot = u | 605 r=a  ("sua") | 632 c=p | 655 //=e | 692 z=r  ("per") | 725 7=f | 752 v=n/u | 782 z=r | 815 d=l | 842 n=i | 870 c=p | 898 v=n | 932 6=u | 958 s=c | 988 9=h | 972 n=i | 998 r=a | 1028 q^a=ra | 1062 x=d | 1092 n=i  ("di") | 1118 d=l | 1148 r=a  ("la") | 1175 n=i | 1205 g=n  ("in") | 1248 6=v | 1278 eps=o | 1308 s=c | 1335 4=e  ("voce") | 1368 6=v | 1398 n=i | 1428 v=n | 1458 r=a | 1490 d (straight) = s | 1518 s with a dot = u | 1545 r=a  ("sua") | 1580 d=l/s | 1608 r=a | 1635 3=o | 1665 s=u | 1695 r=a | 1728 x=d | 1760 q=e
 (gain: "volendo la Santita sua" (d r v o-bar n L^a = s-a-n-t-i-ta) for the first pass's unread
  "x z v o-bar v L^a"; "per", "di la", "in voce", "sua" confirmed.)

L27: ca[sa?] qua[e]r[?]... pare che questo M: (Ser.mo Re de Hungaria) de li o[g]ni[?] ... darli [?]nrnte
 signs (page x): 148 b-stroked=ca | 185 m^a=sa | 228 ) crescent = q | 260 s=u | 285 r=a | 312 q=e | 342 z=r | 372 L. = te(?) | 400 eps=o | 435 c=p | 465 n+4=ss | 522 4=e | 548 4=e | 590 6=u/co | 622 c=p | 650 z=r | 682 o-bar=t | 715 z=r | 745 c=p | 775 r=a | 800 z=r | 828 //=e  ("pare") | 855 s=c | 882 9=h | 908 //=e  ("che") | 935 ) crescent = q | 962 s=u | 975 d + 1002 o-bar = st | 1032 3=o  ("questo") | 1070 M: = Ser.mo Re de Hungaria | 1115 x=d | 1142 //=e  ("de") | 1170 d=l | 1198 n=i  ("li") | 1225 eps=o | 1252 n=i | 1280 8=g/n | 1312 r=a | 1345 z=r | 1400 8=g | 1430 x=d | 1458 r=a | 1488 z=r | 1518 d=l | 1545 z=r/n | 1580 n=i | 1610 8=n | 1638 z=r | 1665 8=n | 1700 L:=te
 (new: "pare che questo M:" at 745-1070 - the first pass had "c p̸ z o-bar z | c z z //" unread and
  only reached "che questo".)

L28: ad d[e/i] altri che [?] ... ad ... ve[r]g[o]t[o?] d[i]s[c]r[e]t[i]o[ne?] che ... possi[?] essere
 signs (page x): 145 r=a | 175 x=d  ("ad") | 208 x=d | 238 n=i | 278 r=a | 308 d=l | 345 o-bar=t | 375 z=r | 405 n=i  ("[d]i altri") | 442 s=c | 468 9=h | 492 //=e  ("che") | 518 6=u | 545 4=e | 568 b=co | 555 q=e | 592 b^o=no  ("ne"?) | 625 r=a | 652 x=d  ("ad") | 688 c/p-str | 715 4=e | 745 7=f | 785 d=l | 812 r=a | 845 c=p | 872 v=n | 908 //=e | 935 n=i | 962 z=r | 978 6=v | 1002 z=r | 1030 8=g | 1062 o-bar=t | 1092 3=o | 1125 x=d | 1152 s=c | 1178 z=r | 1208 o-bar=t | 1238 n=i | 1265 eps=o  ("d[i]s[c]r[e]t[i]o[ne]"?) | 1310 s=c | 1338 9=h | 1362 //=e  ("che") | 1398 3=o | 1440 n+4=ss | 1488 n=i  ("[p]ossi"?) | 1530 4=e | 1572 n+4=ss | 1618 4=e | 1662 q^e=re  ("essere")
 (the line still mostly resists; the certain ends are "ad", "che" twice, and the closing "essere",
  preceded by "o-ss-i" which is probably "possi" - the same word page 4 opens with
  ("quello che sapia et possi").)

## What this pass changed

Newly read or corrected against trans/v2831p3b_read.md:
- L15 "mandare"; the "i" (dotted) = a and "x" = d inside it.
- L17 "ancora" (not "r̸ b^a a"), and the whole line end "octo di, o dece al piu, et"
  - which also kills the "unexplained recurring group c n b": it is "c n 6" = "piu".
- L18 "…a la quale." (the crescent ) = q + small s = u).
- L20 "la singulare observantia de questo Ser.mo Re verso la …" - three unread runs of the first pass.
- L21 "prome[…]" and "per disponer(e/a) la".
- L22 "del Turco" and "il Turco" (twice), and "dopoi".
- L23 "galiardamente, et co[n] tale modest[i]a che convi[e]ne a li …" - the whole line after
  "del re Ferdinando", which the first pass left blank.
- L24 "d'animo".
- L25 "che li sono date apresso el …".
- L26 "volendo la Santita sua".
- L27 "pare che questo M:".
- Sign values: plain unbarred o = b (the barred o stays t); dotted i = a inside words;
  the ss ligature (n + crossed 4) is one sign; the "b with a macron" in "ancora" is just co.
Still open: the "q^s x̄" pair (three times on the page, twice straight after "ad" where a place-name
is wanted); the "♀" sign (L15); the "a with a long macron" (L18 x1520, L21 x505); the blot in L15;
and most of L24 and L28.
