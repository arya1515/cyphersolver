# JQA at St Petersburg: the despatches are NOT in the Armstrong code; his own code rebuilt, and Ford's
# "not decyphered" passage of No. 88 (25 June 1812) read

## 1. The premise, checked

- Madison editors on Armstrong's letters (Founders Madison/02-10-02-0369, 02-12-02-0197): code "also used by John
  Quincy Adams at St. Petersburg and by Jacob Lewis at Saint-Domingue; key not found but substantially reconstructed by
  the editors". On JQA to Madison, 7 Jan 1811 (Founders 03-03-02-0121): "a code provided by the State Department to
  John Armstrong in France and to both William Short and Adams" (citing Ford, Writings of JQA 3:328).
- Ford 3:327-28 (Smith's instructions, 1809) says JQA's own cypher was **the London minister's** (Pinkney's), and JQA
  was to *obtain a copy of Armstrong's* at Paris to correspond with him. JQA acknowledges receiving "the copy of General
  Armstrong's cypher" (Ford 3:~370). So JQA held both; the despatches to Washington use the other one.
- NARA M35 reel 3 (naId 188725601): every coded despatch checked (1812: frames 0182, 0189-0190, 0206-0207, 0211) uses
  a code with **the = 1385, of = 1576, that = 1384, and = 668, I = 1401**. THE=972 (Armstrong) has the = 972,
  of = 1354. The 592-entry Armstrong table renders these pages as noise (`../armstrong/decode972.py`). Reel 2 frame
  0155 (1810) is in the same JQA code. **The table we already hold cannot read JQA's despatches.** The Founders note on
  the 7 Jan 1811 letter to Madison (a private letter, not a despatch) was not checked against its manuscript (Forbes
  collection, not online).

## 2. JQA's code rebuilt (the roll-13 method)

`pairs_jqa.txt`: ~300 entries. H = the State Department clerk's interlinear decode on M35 reel 3 frames 0206 (No. 88)
and 0189 (1812); M = aligned but uncertain; I = inferred from the code's structure + context. **Structure:** an
alphabetical syllabary cut into blocks of ~50 numbers, blocks shuffled, alphabetical inside each block (e.g.
1151-1200 w- [1168 weeks ... 1199 would]; 1301-1350 b- [1305 Bal, 1308 bass, 1310 be, 1317 been, 1331 between, 1349
both]; 1384-1399 th- [that, the, then, there, they, this]; 1501-1550 a- [a, ad, af, agree, ain, al, am, an, ance];
1-100 whole words [16 Emperor, 21 Minister, 44 negotiation, 49 U.S., 92 measures]). This makes slot inference
(as done for Armstrong's code) strong. `render.py FILE` applies the table.

## 3. No. 88, 25 June 1812 (the day after Napoleon crossed the Niemen): Ford 4:357 "[Nine lines of this paragraph
## not decyphered.]"

Triplicate, M35 reel 3 frame 0206 (the clerk's decode stops exactly where Ford's gap starts). Groups: `gap88.txt`.
124 of 134 groups now read (`python render.py gap88.txt`); inferred syllables in [ ], unread groups as {n}:

> [Certainly negotiation then was his wish] and expectation. But the {1434} {168} it {1081} of the Emperor
> [Alex]an[der] to Wilna was im-{1425} {83} to the [Chan]cel[lor], and {1575} {1405}, and [if] his [active]
> influ[ence] had not been im[paired] {1112}-tion-ed before it, [it can] scarcely [fail] to have been [af]fected
> {by} his ill[ness] im[medi]ately [af]ter his ar[riv]al [thither], which was undoubtedly an apo[plec]tic
> {1060} s-tr-[oke]. Since then he has had a [second] and a more [seve]re one. In the German Gazettes even his
> [death] has been an-no-[un]ced; but that was a [mis]take. At all [events] it is scarcely possible that he should
> [rem]ain [much] [long]er in the department of [foreign] [affairs].

"He" is Count Rumyantsev (Romanzoff), Chancellor and foreign minister, who had gone to Wilna with Alexander. The
passage reports his apoplectic stroke at Wilna, a second and worse one since, a false report of his death in the
German papers, and JQA's judgment that he cannot long stay at the foreign ministry. That fits the known history: he
suffered a stroke in 1812 that cost him his hearing, and retired in 1814. It differs on timing. Standard accounts
(Britannica, Wikipedia) tie the stroke to the news of the Niemen crossing on 24 June. JQA, writing at St Petersburg on
25 June before that news could have reached him, says the first stroke came soon after Rumyantsev reached Wilna, and
a second, worse one followed before 25 June. Ford printed none of this.

Grades: the skeleton (his, illness, immediately, arrival, which was undoubtedly, stroke, since then he has had a,
and a more, one, In the German Gazettes, even his, has been, but that was a, take, it is scarcely possible that
he should, in the department of) rests on clerk-attested groups. [bracketed] syllables are slot inferences that fit
block and context; they are not attested.

## 4. The "remainder of letter ... undecyphered" (Ford 4:358)

It is on frame **0207** (left leaf): 13 lines of code, then clear sentences (Manifestos of both parties expected;
Peace with Turkey signed a third time; "It is not General Kutuzoff but Count Rostopchin who is appointed Governor,
civil and Military, of Moscow"), then 5 more lines of code. Groups: `rem88.txt`; 210 of 250 groups render. Readable
threads, not yet a clean text:
- "[if] this proposition has in any [form] been disclosed to the Russian government, it was cer[tain]ly ... nor ...
  [con-sis]t[ent] with a sys-tem rig-our-ous-ly and ... [de-fen-sive] (underlined in the MS) ... with a proposition
  for the [eva]cuation of [P]russia by the French troops as ... [pre]li[mi]na[ry] to negotiation. But the very
  [point] upon which the ambassador ... Prince Kurakin's last note was that it ... a propo[sition] with which it would
  be dis[hon]ourable in France to ... he ... it as a [dem]on[str]ation that the Emperor Alexander had de[ter][min]ed
  not to [ne]go[ti]ate ... such a proposal as France had ... ."
- after Moscow: "an [army] of re[serve] is [form]ing there, and it is ... on the side of the French ... the
  commencement of the war the Emperor Napoleon ... to pe[ne]trate directly ... of the system ... the side of the
  Baltic."

## Next

- Read more clerk-decoded pages (0182-0185, 0190, 0194-0199, 0211; reel 2 1810-11) into `pairs_jqa.txt`; this
  should settle the {n} groups and the remainder page.
- Ford's other gaps: No. 51 (26 May 1811, "[One line and a half of cypher not decyphered]") and No. 55 (22 June
  1811, "[one-half line of cipher not deciphered]"), both on reel 3.
- Reel 2 frame 0155 (1810): a long coded passage with no decode on the NARA copy; compare with Ford vol. 3.
