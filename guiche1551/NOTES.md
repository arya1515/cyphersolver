# La Guiche (Rome 1551), Noailles (Venice 1558), Seure (Lisbon 1558): catalogue no. 10

Catalogue entry 10 ("La Guiche (Rome), Noailles (Venice), Seure (Lisbon)", class C). Three ambassadors' letters
with cipher in two BnF recueils. Worked 2026-09-21 (one session, Claude Opus 5).

Outcome: **La Guiche read in part (new reading); Noailles read at the time (marginal decipherment, partly
lost in the gutter); Seure not attempted: a five-letter corpus, too large for this pass.**

## 1. La Guiche → Montmorency, Rome, 22 Nov 1551 (fr. 3138 no. 22)

Gallica btv1b90601662, view 65 (f. 60v–61r; the cipher is all on f. 60v, signature "Claude de la Guiche e. de
Mirepois" on f. 61r). About 13 lines of cipher set inside clear text. The first two lines are struck through by
the writer. No decipherment on the leaf, the next leaf or in the margin.

- Transcription: `guiche_ct.txt`, 406 signs, 22 distinct (sign codes in the file header). Made from full-resolution
  crops of each line.
- System: a simple substitution, one sign per letter, no word division. 22 signs map onto the 22-letter alphabet
  of the period. `3`=e is 16% of the text.
- Attack: `solve1.py` (permutation annealing with swap moves, `fr-1530-despatches` 5-gram, no spaces, 16 restarts)
  gave "le conte sainctefiore est mal satisfaict" on its best restart. The first free many-to-one annealer
  (`solve.py`) collapsed onto i/x and failed. `refine.py` then fixed the confirmed signs and re-annealed the others.
  Corrections were made by hand from context: F=qu ("que facilement"), 8=p ("party pour", "pourroit"), P=y ("avec
  moy", "roy"), A=v ("vous", "service").
- Key: 3=e t=r #=i e=u Q=t B=s r=a f=d d=n 4=o o=o (second o) p=c W=l (also g in "Diego") F=q D=m P=y A=v g=f
  8=p X=g; c and 5 (1–2 occurrences) are unassigned.
- Reading (`reading_raw.txt`, then the text below with the clear words around it). Normalised, [?] = unsure:

  > [struck: Dom Diego (a faict) constituer prisonnier en ce(ste ville) … un Siennois … croy que … est au dit …]
  > le procès duquel j'ay trouvé moien de veoir, *affin de informer led. Sr cardinal du contenu en icelluy pour
  > selon cela mettre tel fondement qu'il advisera* : la m… de ceux de Sienes qui estoit icy, lequel est party
  > pour s'en retorner a Sienes avec Dom Diego. … Le conte [de] Sainte Fiore est mal satisfaict de […], et que
  > facilement se reduiroit au service du roy … *[clear: de la Seance]* … le service … *Car ledict personnage qui
  > estoit icy tractant* avec moy la faire du sieur +arna+e a dorne[?] *la responce qu'a…* … vous informer du …
  > que le roy pourroit avoir du dict sieur +arna+e et aux [?] … des conditions qu'il demanderoit.

- The subjects are the Sienese envoy leaving Rome with Dom Diego (Diego Hurtado de Mendoza, imperial ambassador and
  master of Siena, a few months before the Sienese rising of July 1552), and the Count of Santa Fiora (a Sforza,
  the pope's relation) being discontented and ready to come over to the king's service, on conditions. This is the
  Parma war winter.
- Open: the name "sieur +arna+e" (signs `t r t d r t 3`; the `t` there may be a plain + distinct from the barred
  sign read r); signs c and 5; the struck-through first two lines, which read only in part. Grade: key C (secure
  for the 15 signs above), text M where marked.
- Prior art: web search found no edition of this letter; no decipherment in the volume.

## 2. Noailles → Cardinal de Lorraine, Venice, 13 Nov 1558 (fr. 3151 no. 33)

Gallica btv1b9059865k, views 60–61 (f. 59–60). The letter is in clear (Levant galleys, Candia, Corfu) with two
short cipher passages (3 and 3 lines) on f. 60r. **The court's decipherment is written beside each block in the
inner margin** ("…mauluaise … gouvernement … affaires"; "grand seigneur … ne luy … de la fortune …"), but the
binding has swallowed the start of each gloss line. Read at the time; the cipher itself (about 150 signs, a
different symbol alphabet) was not attacked. A full reading would need the page opened flat, or a solve using the
visible gloss words as cribs.

## 3. Seure → de Fresne / Henri II, Lisbon, Dec 1558 (fr. 3151 nos. 39–44)

The catalogue says "no siblings", which is wrong. The volume holds six Seure letters of 12 and 27 Dec 1558 (nos.
39–44, Gallica views ~72–88), and nos. 40/41 and 43/44 are duplicate copies. Each mixes clear text with long cipher
blocks, about eight pages and roughly 2,000 signs in all: a homophonic symbol alphabet of about 60 signs plus
numerals (12, 13, 23, 100), so a nomenclator. There is no decipherment on the leaves.
The duplicates do not simply swap clear and cipher: the fleet passage (22 ships at Havana, Florida) is in clear in
both copies seen. This is solvable in principle with a full transcription (large corpus, one key), but that is a
multi-session job. It is left open and should be split off as its own catalogue item.

## Files

- `guiche_ct.txt`: La Guiche transcription. `reading_raw.txt`: decryption per line with the key above.
- `solve.py` (failed free annealer), `solve1.py` (permutation annealer), `refine.py`.
- Images: `gallica_sweep/btv1b90601662/`, `gallica_sweep/btv1b9059865k/`, `gallica_sweep/hi/` (git-ignored).

## Remaining gaps

- La Guiche f. 60v: the name 'sieur +arna+e', signs c and 5 - blocker: open-codes; sign t there may be a plain + distinct from barred r; c and 5 occur only once or twice
- La Guiche f. 60v: the two struck-through first lines - blocker: illegible; struck through by the writer; read only in part
- Noailles fr. 3151 no. 33 (f. 60r), start of each marginal gloss line - blocker: needs-physical-access; swallowed by the binding; needs the page opened flat
- Noailles fr. 3151 no. 33, the cipher itself (about 150 signs) - blocker: not-attempted; not attacked; the visible gloss words could serve as cribs
- Seure fr. 3151 nos. 39-44 (about 2,000 signs, homophonic with numerals) - blocker: not-attempted; left as a multi-session job; not transcribed

## Escalation

- [x] siblings: leaf, next leaf and margin of La Guiche checked; fr. 3151 searched and the six Seure letters (nos. 39-44, duplicates 40/41, 43/44) found
- [x] clear-pages: Noailles's marginal decipherment identified; La Guiche has none
- [ ] known-keys: not done — no French diplomatic key of the 1550s (Tomokiyo's Henri II pages, Lasry's GL.htm) was tried on La Guiche's leftover signs, Noailles or Seure
- [ ] print: not done — only a web search; Ribier, Lettres et memoires d'estat (1666), and the Noailles ambassade edition (Vertot 1763) not grepped for these letters
- [x] key-rebuild: permutation anneal (solve1.py) plus refine.py with fixed signs; qu, p, y, v fixed by context
- [ ] retry: not done — rerun reading_raw.txt after settling the + / barred-r question; solve Noailles's cipher with the visible gloss words as cribs; transcribe and anneal the Seure corpus
