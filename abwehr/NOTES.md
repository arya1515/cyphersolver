# The Koehler cryptograms (Abwehr, New York → Hamburg → Paris, February 1944) — attempted, skipped as intractable

Schmeh's Top 50 No. 47. Five letter-cipher messages (237, 178, 140, 140 and 229 letters; the one headed "137"
has 140) are quoted in a German teleprinter letter: *An Abwehrleitstelle Frankreich, Paris Funkstelle — Sofort
vorlegen! — Betr.: Koehler*. David Kahn published them in *Cryptologia* 5(2), April 1981, from a copy in the
British archives. `msgs.py` holds the text, checked against the Cryptologia printing. The check corrects one
letter in every circulating copy: message 137, group 17 is `ayddq`, not `ayddg`.

## Background that matters for the system

*Koehler* is Walter Koehler, a Dutch engineer the Abwehr sent to New York in 1942. He surrendered to US
officials in Madrid, and the FBI then ran his radio link to Hamburg. Hoover wrote in 1946 that the traffic used a
book cipher based on a **Dutch-language prayer book** the Abwehr had given him. David Alan Johnson's account
(Schmeh 2021) says Koehler also passed true reports to the Abwehr behind the FBI's back.

Schmeh reads these five messages as Koehler's secret reports, and so not in the prayer-book cipher. The routing
allows a second reading. The letter goes from Hamburg, the station that received the New York radio traffic, to
Paris, "Subject: Koehler", with the text forwarded unread for decryption there. That is what relayed traffic of
the FBI-run channel would look like. Either way, the statistics below constrain the system without deciding who
wrote the text.

## What was tested (`periodic.py`, `msgs.py`, `lm.py`)

| hypothesis | test | result |
|---|---|---|
| monoalphabetic substitution, transposition, ABC-Verfahren | index of coincidence | 0.0398 over 924 letters (German 0.076, random 0.0385): **excluded** |
| periodic Vigenère / Beaufort / variant Beaufort, periods 1–26 | quadgram hill-climb per period in German, English and Dutch, against shuffled ciphertext at the same setting | best keys score at shuffle level, hundreds of points below real text: **excluded**. The weak period-IoC peaks (237 at 17, 140 at 9; p ≈ 0.04 after correction) yield nothing when solved |
| ciphertext autokey, offsets 1–40 | undone directly, IoC of the result | 0.039 at best: **excluded** |
| running key from natural-language book text (standard tableau) | likelihood of the ciphertext letter counts under every plaintext-and-key combination (de/en/nl × de/en/nl × 3 variants) | all models score **below uniform** (−4.0 nats), while 924-letter true running-key ciphertexts score ≥ +7.5 in 95% of trials (median +18): **excluded** |
| Gronsfeld (digit shifts 0–9, e.g. from book page numbers) | same test, all offsets | ≤ +3.3 nats: **excluded** |
| **any Enigma**, not only the G-31, G-312, G-260 and G-111 wirings searched in 2017 | letter counts: χ² = 57.9 against uniform; simulated Enigma-like output of German (flat, no self-encipherment) has median 26 | **p = 0.0003: excluded**. The transcription was checked against the printing. The result is driven by `c` (14 against 35.5 expected) and `z` (55) |

Depth between messages: the best cross-message coincidence rates, 0.073–0.091 over 61 offsets, are what short
overlaps give by chance. There is no sign of key reuse.

## Why it is skipped

The letter counts are too flat for any language-shaped hand cipher and too uneven for a machine. Two systems
survive:

1. **A book key through a mixed alphabet table** (a running key on a keyed Vigenère tableau). The counts are
   skewed, but not in the shape a language gives on a standard alphabet, which is what this system would
   produce. It is also a plausible form for the documented prayer-book system of the Koehler channel.
2. **A hand-made one-time pad or random key table**, slightly non-uniform from the way it was drawn.

Without the book, a mixed-tableau running key over 924 letters in five unrelated messages has no practical
ciphertext-only attack, and a one-time pad has none. There is no crib either: the contents are unknown, and the
FBI's plaintexts for the channel are not published.

## What would reopen it

* **The FBI case file on Koehler** (NARA RG 65, possibly released under the Nazi War Crimes Disclosure Act). If
  these messages belong to the FBI-run channel, the FBI's own plaintexts and the prayer-book procedure are in
  it, and this becomes a known-plaintext check.
* **Kahn's source file in The National Archives.** The Hamburg–Paris letter was itself presumably an intercepted
  Abwehr message, and its reference would show whether the British read the inner text.
* **The prayer book itself**, if the edition is ever named.
