# The unsolved ADFGVX messages of 1918 — a working decoder, and page 100 reproduced

Twenty-two ADFGVX radio messages from the Eastern Front sit on Klaus Schmeh's Top 50 as unsolved.
They are not unbroken ciphers. George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker broke the James
Rives Childs corpus and **published the keys** — fourteen three-day periods, 618 cryptograms
recovered. What defeats these twenty-two is mutilation in transmission, and ADFGVX is unforgiving
about length: the columnar stage splits the stream by the key length, so one lost letter moves every
column boundary after it.

In the comment thread under Schmeh's 2017 post, readers solved twelve or thirteen of the twenty-two.
Schmeh announced a consolidating article and never wrote it, so those readings exist only as
scattered comments and no table has ever been published.

## What this session built

**The keys, machine-readable.** `keys.json` has all fourteen. Three of them do not survive a naive
read of Lasry's PDF: their substitution squares contain runs of hyphens for unrecovered cells, and the
PDF text layer collapses those runs into en- and em-dashes, leaving squares of 34 or 35 characters
instead of 36. Expanding the dashes back to the length that makes 36 recovers all three.

**The transposition convention, settled.** Two readings of the key numbers are possible: `perm[i]` is
the column emitted i-th, or `perm[i]` is the position at which column i is emitted. Both round-trip
self-consistently, so a round-trip test cannot tell them apart. Decrypting a real message can, and it
is the **second**.

**Page 100, reproduced from scratch.** The published reading is

> KEINE STOERUNG DURCH FEIND X MITTAGS 2 FEINDL X DIV X IM MARSCH AUF BELGRAD X

That is 62 characters, so 124 ADFGVX letters, but only 122 were received. Searching every way of
inserting two placeholders, against all fourteen keys, returns it at a score of 140.7 against a field
where nothing else clears 7:

```
KEINESTOER?NGDURCHFEINDXMITTAGS2FEINDLXDIVXIMMARSCH?UFBELGRAD?
```

Key: **Nov 1–3, length 19**. The placeholders land on the three characters shown as `?`. This
validates the whole pipeline end to end.

## What it found

Running all twenty-two against all fourteen keys, allowing up to two insertions or one deletion:

| page | letters | key | reading |
|---|---|---|---|
| **100** | 122 | Nov 1–3, len 19 | **solved**, as above, score 140.7 |
| **132** | 153 | Nov 4–6, len 17 | **key identified**: `WIEDERHOLE` … `TELEG` emerges cleanly |
| 146 | 244 | len 17 | partial: `STELLEN`, `RICHTIGEN` |
| 189 | 84 | len 18 | weak |
| the other 18 | — | — | nothing above noise |

The page 132 result is worth stating carefully. Neither **WIEDERHOLE** nor **TELEG** is in the
scorer's word list, so they were not being optimised for — they emerged. "Wiederhole Telegramm",
repeat the telegram, is exactly the kind of traffic these stations sent. The key for that message is
therefore the Nov 4–6 one, and what remains is deeper reconstruction rather than a key search.

## Honest limits

Only one of the twenty-two is fully read here, and it is one that was already read in 2017. The
search allows at most two insertions or one deletion; messages mutilated more heavily than that, or
mutilated by substitution rather than by loss, are out of its reach. Several of the twenty-two carry
explicit gap marks in the printed transcription, and one is labelled "missing 10 letters" — those
need the Childs originals, not a wider search.

What is new and reusable is the decoder, the machine-readable keys with the three damaged squares
repaired, the settled transposition convention, and the identification of page 132's key.

Reproduce: `python repair.py validate` (page 100), `python repair.py solve` (all), `python deep.py
132 17 3` (the deeper search on page 132).
