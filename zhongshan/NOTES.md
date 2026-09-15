# Telegrams from the sunken Zhongshan (c.1938) — no corpus, and the premise was wrong

The gunboat *Zhongshan* was sunk by Japanese aircraft in 1938. In October 2008 the Zhongshan Warship
Museum published a call for help with encrypted telegrams recovered from her; by 2009, **352 of 891**
had been read.

## There is nothing to work on

Tomokiyo's catalogue entry says it plainly: *"I have not located the primary sources of these
telegrams."* Nothing beyond a single five-group opening has ever been published, and the museum's
corpus is not online. Like the Marmont letter, this item is blocked at the source rather than at the
cryptanalysis.

## What the one published fragment gives, verified here

The published opening is `7115 6752 7022 0735 1378`. Run through the standard Chinese telegraph code
(the table already in `sunyatsen/cn.csv`) it reads

> **陳部長 和密** — "Minister Chen, *He Mi*"

which confirms Tomokiyo's identification of the addressee as Chen Shaokuan, Minister of the Navy, and
adds something his summary leaves implicit: **the cipher names itself in its own preamble**. 和密
*He Mi* is written out in clear as groups `0735 1378`, in the conventional code, before the message
switches into it.

The closing `7456 0582` reads **馬午** — 馬 being the 21st day in the 韻目代日 rhyme-code day system
and 午 the double-hour 11am–1pm. That reproduces his "11 am to 1 pm of the 21st" exactly, from the
tables here rather than from his reading.

## The premise for this item was wrong

The tracker put this high on the ground that "Chinese telegraph code again, so the machinery built
for the two 1916 telegrams applies unchanged", with the stated risk being "a commercial codebook with
an additive rather than a systematic condenser, which would end it quickly."

That risk has materialised. **He Mi is a separate codebook, not a transformation of the standard
one.** It belongs to a family of independently compiled Nationalist codebooks — Qing Mi 清密, Liang Mi
亮密, Tong Mi, Yi Mi, replaced in January 1937 by Sheng Mi and Li Mi — and Tomokiyo shows for its
sibling Qing Mi that the character ordering differs from the standard *Dian bao Xin bian* in ways a
digit permutation cannot produce: characters sharing a radical sit together on one page of Qing Mi
while the conventional assignment puts one of them in the appendix.

The Sun Yat-sen attack worked because that cipher was the *standard* telegraph code passed through a
systematic condenser, so the condenser family was small enough to enumerate. Here there is no
condenser to find. There is a bespoke codebook, and a codebook is recovered from traffic, not from
a key space — which needs the 891 telegrams that are not published.

## Status

Not attempted beyond verification, because the corpus does not exist publicly. The item should be
reclassified: not "same toolkit as Sun Yat-sen" but "blocked on the Zhongshan Warship Museum's
holdings", alongside the Marmont letter.
