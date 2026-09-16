# Thomas Urquhart's encrypted poems — the provenance objection, checked independently

Two numeric cryptograms attributed to Sir Thomas Urquhart (1611-1660): a distich of 64 numbers in two
lines of 32, values to 70, and an octastich of about 272 numbers, values to 201. Number 28 on
Schmeh's Top 50.

There is a live dispute. In August 2026 a published claim solved the distich as a book cipher on
Urquhart's *Proquiritations*, the i-th number indexing a word in the i-th Proquiritation with first
letters taken, giving "O GOD UPHOLD KING CHARLS THE SECOND / AND MAKE HIM THE SUPREME RULER OF THIS
LAND". A rebuttal of 1 September 2026 argued the rule fails at ten of the sixty-four positions, scores
at chance across tokenisations, and - the part that can be checked independently - that the distich
**does not appear in the verified 1653 text at all**.

## The structure of the claim is right

Wilcock's 1899 biography describes the end of *Logopandecteision*:

> "The volume concludes with requests or 'proquiritations' from **thirty-two distinct petitioners**,
> who modestly conceal themselves from public notice under the shelter of the **initial letters of
> their names**."

Thirty-two proquiritations; the distich is two lines of thirty-two; and the petitioners are already
hidden behind initial letters. The 1653 text itself, through its ruined OCR, still shows Urquhart
fussing over the number - "there can no number like that of Twe and thirty ... so apposite for
Crowning the sum of these subsequent Proquiritations, according to the tenour of this Algebraical
Hexastick". So the *shape* of the claimed cipher matches the book.

## The provenance objection holds, on an independent copy

The rebuttal cites the British Library copy. This check used a different one - the Early English
Books scan, Internet Archive item
`bim_early-english-books-1641-1700_logopandecteision-or-an_urquhart-sir-thomas_1653` - and reaches
the same place.

* The book ends with the printer's apology and then an **errata table**. There is no numeric poem.
* Across the whole 1653 text there are **zero** runs of eight or more numbers.
* Across the whole of Wilcock 1899, likewise **zero**.

So neither the source the claim rests on nor the nineteenth-century biography that is supposed to
transmit the cryptograms contains, in their digitised form, any numeric sequence of the right shape.

**Honest limit.** This is OCR of a 1653 black-letter book and it is genuinely dreadful - the prose is
barely readable in places. A printed table of numbers usually survives OCR better than prose does,
which is why the total absence of long numeric runs is worth something; but absence in OCR is not
absence on the page, and settling it properly needs the page images.

## Status

The claimed solution could not be tested here, because the ciphertext could not be located in the
source it is said to come from. That is not a refutation of the reading - it is a statement that the
provenance has to be established before the reading can be judged, which is what the rebuttal said.
The octastich remains untouched by anyone.

## The octastich, measured (2026-09-15, second session)

Schmeh's transcription (`../top50/arts/28.txt`) gives nine lines of 33, 27, 38, 39, 32, 28, 31, 34 and 10 numbers,
272 in all, 82 distinct, maximum 201. The distribution is steeply skewed to small values: 108 of the 272 are ten
or less (1 occurs 15 times, 2 and 5 thirteen times each), 76 lie in 11-30 and 88 above 30. Index of coincidence
0.021, against 0.038 for uniform-over-26 and about 0.066 for a monoalphabetic substitution of English, so this is
not a simple substitution with a few nulls; it is either heavily homophonic or an index into a text. The distich
shares 31 of its 32 distinct values with the octastich and has the same skew (5, 3 and 20 are its commonest), so
the two poems are in one system.

The shape (small integers dominating, occasional values to 201, line sums 327-1470) is what a book cipher of the
word-index or line-and-word kind produces, and what the August 2026 claim assumed for the distich. It is not
attackable without the key text, and the provenance question of the previous section applies with more force
here: nobody has said where the octastich was printed. Nothing further can be done online; the item stays where
the previous section left it.
