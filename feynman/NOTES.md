# Feynman ciphers #2 and #3 — verification of the 2023 solution (2026-09-14)

Both were solved by David Vierra in May 2023 (https://codewarrior0.github.io/cipher-blog/2023/05/27/feynman-solved.html).
Method: two monoalphabetic substitution alphabets, alternating word by word (first word of each line/sentence uses
alphabet 1), even-length words written backwards after substitution, word boundaries dropped.
  A1 = MANYREQUS.HVBCID.OLWGZX.K.   A2 = JHAZTENYXMLOCUFBQVKPSGW.D.   (position i = cipher letter for plaintext A+i)

`verify.py` re-encrypts the claimed plaintexts and compares with the ciphertexts:
- #3 (Feynman 1953, "The behavior of liquid helium…"): 228/231 positions match; the 3 mismatches are one letter in
  "phenomenological" and a transposed pair in "principles" (encoder or transcription slips).
- #2 (Housman, "Terence, this is stupid stuff", ll. 19–32): first 118 characters exact; 208/261 overall. The
  mismatch regions decode directly to ENGLAND BREWS (both words under A2 — the documented exception) and to
  "…MAN ALE MAN ALE… THE STUFF … DRINK FOR FELLOWS WHOM IT HURTS TO THINK" (the encoder's wording of line 27
  differs slightly from Housman's printed text).
Verdict: the published solution is correct; there is nothing left to solve here.

## Independent decryption (`decrypt.py`)
Viterbi word segmentation over the two alphabets with the even-length-reversal rule recovers both plaintexts from
the ciphertexts alone (dictionary from the Gutenberg novels in `beale/lmcorpus`):
- #2: "WHY IF TIS DANCING YOU WOULD BE THERE IS BRISKER PIPES THAN POETRY SAY FOR WHAT WERE HOP YARDS MEANT OR WHY
  WAS BURTON BUILT [ON TRENT] OH MANY A PEER OF ENGLAND [BREWS] LIVELIER LIQUOR THAN THE MUSE AND MALT DOES MORE
  THAN MILTON CAN TO JUSTIFY GODS WAYS TO MAN ALE MAN ALE IS THE STUFF TO DRINK FOR FELLOWS WHOM IT HURTS TO THINK"
  (bracketed words garble where the encoder broke his own alternation rule; note "ale is", not Housman's "ale's").
- #3: "THE BEHAVIOR OF LIQUID HELIUM ESPECIALLY BELOW THE LAMBDA TRANSITION IS VERY CURIOUS THE MOST SUCCESSFUL
  THEORETICAL INTERPRET[ATION]S SO FAR HAVE BEEN LARGELY PHENOMENOLOGICAL IN THIS PAPER AND ONE OR TWO TO FOLLOW THE
  PROBLEM WILL BE STU[DIED] ENTIRELY FROM FIRST PRINCIPLES" (garbles at the two ciphertext slips).
