# Session findings — fr. 3096 nos. 63, 65, 66 (17 Sept 2026)

What was established, and how each point was proved.

## 1. Same hand, same symbol set (the "verify first" step) — confirmed

The glyph repertoire of nos. 63, 65 and 66 is that of the control no. 62:
`Δ` c, `▽` q, `Ц`/`1`/`ʒ` o, `⊡` ll, `Ŧ`/`Ǝ` s, `Q` r, `π` n, `x` t,
`T`/`α`/`ɣ`/`H` u-v, `6` p, `S` g, `E` h. One secretary hand writes the clear
passages of all three. Lasry's key applies to all three, and does.

## 2. Nos. 65 and 66 are the duplicate pair, and they crib each other

No. 66 carries the docket **`duplicata`** (f. 121r, upper right). No. 63 opens
*"Il xxIII del p[rese]nte per n[ost]re duplicate l[ette]re a v[ost]ra M[aes]ta
al lungo scriuessimo ciò che haueuamo negociato con questo S[ignor] Duca"*.
Both 65 and 66 subscribe *Da Ferrara alli 23 Febraro 1529*.

They are independently drafted and **encipher different passages**. No. 66
writes in clear what no. 65 enciphers, and the reverse. So the pair reads
itself, and it also validates the decipherment:

| no. 65 (cipher, deciphered here) | no. 66 (clear on the leaf) |
|---|---|
| *maiesta, fato la reuerentia a madama Rainea et al signor don Hercole* | fatta che hebbimo la reuerentia a Madama Rainea et al s[ignor] Don Hercole |
| *…suadesimo… conforto… instantemente esortasimo et pregasimo…* | suadessemo confortassemo et instantementi essortassemo et pregassemo |

The second column was read off the leaf before the first column was decoded,
and neither was used to produce the other.

## 3. Two corrections to the key (both against glossed ground truth)

**(a) The crossbarred long-s is `e`, not `f`.** On f. 113r the run glossed
`de vn capitaneo suizari` opens `ꜿ f T π Δ V 6 p x υ π Γ 1`; the crossbarred
long-s in second position sits under the `e` of `de`. `f` proper is the double
`ſſ`. This one form accounts for about one letter in twelve.

**(b) There is a null** — a tall sign with a large top loop and long
left-curving descender, **absent from Lasry's table**, occurring in all three
targets and twice in no. 62's second glossed run. Three checks, each exact only
if the sign is dropped: `H 1 Ǝ x ɧ Q п` = vostra; `Δ ɧ 1 π ʃ ʈ Q x ʒ` =
conforto; `Δ E ɧ k` = che. `KEY.md`'s "no nulls observed" is struck.

**(c) The large double circle `◎` is a nomenclator for DUCA** (Alfonso I
d'Este), distinct from `⊙`, the single dotted circle, which is an `i` homophone
(the `i` of `aquila`, `V ▽ H ⊙ ϙ υ`). It reads through every context:
`con questo ◎`, `fusimo col deto ◎`, `andai dal deto ◎`. Falling as it often
does where the clear hand resumes, it is easily mistaken for a terminator — I
first read it that way, wrongly.

## 4. Readings produced

`n66_reading.md` — no. 66 through its subscription.
`n65_reading.md` — no. 65 complete and continuous, with English summary;
`n65_transcription.md` line by line.
`n63_reading.md` — no. 63 as far as the leaves go, with the unreadable runs
marked; `n63_transcription.md` line by line. Substance of all three: the duke
refuses to take the kingdom of Naples for himself or the captaincy of the
French army, offers only to accept whatever accord the King negotiates for
him with the Pope, and pleads the want of provisions; the agents judge his
difficulties pretexts and fall back on Ercole and on Trivulzio.

## 5. Codicology

No. 63 breaks off mid-sentence at the foot of f. 116v. f. 117 is a different
paper in another hand, wholly unciphered, so the continuation is elsewhere; the
end of no. 63 and its date have still to be located.

## 6. What did not work, and why it is recorded

An unsupervised k-means over 18,273 glyph boxes plus hand-labelled clusters
(`cluster.py`, `labels.py`) yields a k-NN classifier of about 77% letter
accuracy (`classify.py`). That is a scaffold, not a reading: the draft renders
*acioche conclusion si facese secondo il desiderio di vostra* as
`aciocseconclvsmnsafaceseisoconioiliesiieraoiieasteera`. The segmentation is
also unreliable — the line-band detector emits one physical line twice
(n65 f. 119r L8/L9). Every reading above was made by eye from magnified strips,
with the classifier used only to suggest word shapes.
