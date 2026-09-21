# Percy to Cecil, Norham 23 July 1559 (BL Add MS 4136 f.172, DECODE R9256)

Status: attempted and closed, not read (21 Sept 2026) — the key or Cecil's interlined decipherment on the original (TNA SP 52/1) is needed

## What the record is

The single DECODE image (IMG_R9256_I43281_P.jpg, git-ignored) is a page of the Forbes Papers volume, not
the original letter. The top half has a tracing of four short cipher passages numbered (1)–(4), with Percy's
signature traced between (3) and (4), headed "Sr Hen: Percy to Sr Wm Cecill from Norham 23 July 1559". A second
heading, "…from Norham 22 July 1559 · A", has only the signature. The bottom half is an unrelated key, "Sturmius's
Cipher 4 March 1562" (letters, name codes, nulls); DECODE files it separately as R9257. It is not Percy's key:
its signs are Greek-like letters, not the box shapes below.

The four passages are 13 words, 63 signs (19 distinct sign+mark combinations, measured), in a pigpen-like box script: nine box shapes (⅃ ⊔ L □ ⊏ 7 ⊓ Γ, an I-bar)
modified by an underline, one dot or two dots, plus five other signs (a crossed 4, a boxed cross, a trident, a
tailed 6, a house). Transcription in `transcription.txt`.

## Prior art and context

- CSP Foreign I no. 1051 and Bain, CSP Scotland I no. 501 (downloaded to `sources/cspscot1.txt`, git-ignored)
  calendar the letter: "1 p. A few words in cipher, deciphered by Cecill." The calendared text mentions Mr Knox,
  Whytlaw, the Lord Prior, Lord Hume, Merse and Tevedale, the Dowager ("Dyogre"), the Congregation and Haddington;
  which of these were in cipher is not said. So the content was read at the time and is in print in summary;
  the cipher system itself is not described anywhere I found.
- CSP Foreign no. 1045 (Percy, 22 July): "Knox" is "expressed by a cipher" — a name sign.
- Bain no. 480: Kirkcaldy's 1 July letter to Percy has a cipher postscript deciphered by Percy.
- Laing, *Works of John Knox* VI (1864), pp. 33–35, prints Percy's 1 July 1559 postscript (Bain no. 480 says it
  was in cipher, deciphered by Percy): "The letter that Knoxe wrythe to you is by the meanes of the hole
  Congregatione, the names of whome I sende yowe here inclosed." So Percy's cipher spelled out whole sentences;
  the ciphered form of that postscript is on the TNA original only. Laing does not print the 23 July letter.
  His p. 61 prints Percy (4 Aug) telling Cecil he sent the Lord Prior "a cipher".
- No key in the sibling key records R9257, R9260–R9262 (Throckmorton, Smith, Sturmius) matches the box script.
  Not on Tomokiyo's pages or GL.htm as far as a search showed.

## Attempts (21 Sept 2026)

1. Pattern search of each cipher word against a Sadler/Forbes vocabulary plus the calendar's names
   (`pattern_search.py`): many words fit individually (e.g. "C E B G. E" = prior/merse, (1) w1 = answer/lordes).
2. Rosicrucian hypothesis (each shape a cell of three consecutive letters, marks choose the letter), all cell
   layouts and mark orders, 24- and 26-letter alphabets (`rosi.py`): no layout gives any dictionary word. Ruled out.
3. Joint constraint search for one consistent substitution over all 13 words (`csp.py`, `csp2.py`), with marks
   significant, dots ignored, underlines ignored, marks ignored, homophones allowed: no consistent solution.
4. Trigram annealing (`anneal.py`): only noise; 63 signs over 19 symbols is far below the unicity distance.
5. Cribs tried by hand: "prior"/"lord prior", "knox", "whytlaw", "norham castle", "castel/castell"; none gives a
   consistent alphabet across all four lines.

Conclusion: the passages are probably names and code signs rather than plain letter-for-letter English, and the
text is too short to break without the key. What would move it: Cecil's interlined decipherment on the original,
TNA SP 52/1 (Bain no. 501), which is not online.

6. Word-level annealing against a vocabulary of the period (Sadler, Laing) plus the calendar's names, homophones
   allowed (`anneal_w.py`); reversed reading direction (`csp_rev.py`); constraint search leaving up to six words
   free as name codes (`csp3.py`, timed out). All noise or nothing.

Closed 21 Sept 2026 as attempted, not read.
