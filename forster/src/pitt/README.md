# Forster cipher — 13 May 1644

A reproducible AI-assisted reconstruction of the French passage dated
**13 May 1644** in the Richard Forster papers: ciphertext, proposed key, Python
decoder, literal output, and an edited French reading with an English translation.

**Earlier decipherments:** Karen Britland has informed Robert Pitt that George
Lasry supplied a decipherment after publication of her article, and that Norbert
Biermann independently reached the same solution. This project acknowledges their
earlier work and makes no claim to the first decipherment.

The supplied key decodes **207 encrypted tokens using 34 fixed symbol assignments**.
Four letters require editorial repair in the readable version. This repository's
specific key and editorial choices have not been verified against the handwritten
manuscript or independently reviewed.

## Update — 15 September 2026

Britland's reply identifies the earlier work by **George Lasry** and **Norbert
Biermann**. The reading she supplied agrees with the overall meaning of the
reconstruction here, with some differences in wording:

| Passage | Earlier reading supplied by Britland | This repository's edited reading |
| --- | --- | --- |
| Opening | `aucune voie de scrupule` | `aucun sujet de scrupule` (literal: `aucun subiet`) |
| Prudence clause | `preveu seulement` | `prenez seulement` (literal: `prenez sdulement`) |
| Final verb | `soupir` | `subir` (the supplied source plaintext also says `soupir`) |

The reply did not include the earlier keys, working notes, or a manuscript image.
It therefore provides evidence of prior decipherment and broad agreement in
meaning, while the differences above and the four disputed cipher-derived letters
remain unresolved. The original input, proposed key, and literal decoder output
are retained for comparison.

Source: Karen Britland's correspondence with Robert Pitt, reported by Pitt in
this update. The correspondence is not a published source or a review of this
repository's exact key.

## Files and reproduction

| File | Purpose |
| --- | --- |
| [ciphertext_source.txt](ciphertext_source.txt) | Supplied transcription, preserved unchanged, including existing plaintext and date. |
| [recovered_key.json](recovered_key.json) | Proposed token-to-letter key and uncertainty notes. |
| [decode_forster.py](decode_forster.py) | Deterministic decoder; applies the supplied key without editorial repairs. |
| [decoder_output.txt](decoder_output.txt) | Complete literal output and numbered alignment of all 37 encrypted groups. |
| [test_decoder.py](test_decoder.py) | Checks coverage, input validation, key use, and preservation of disputed letters. |

Requires Python 3.9+ and only the standard library. From the repository directory:

```sh
python3 decode_forster.py
python3 decode_forster.py --alignment
python3 -m unittest -v
```

Check that a fresh run exactly reproduces the committed output:

```sh
python3 decode_forster.py --alignment | diff -u decoder_output.txt -
```

## How the cipher and key work

The proposed key is a **homophonic substitution**: each number or letter token
maps to one plaintext letter, and several tokens can share a letter. For example,
both `0` and `2` mean `e`; `4 30 q 30 19` gives `a u c u n` → `aucun`.
Comma-separated groups can contain several words: `descrupule` is read as
`de scrupule`. Word spacing within groups is editorial.

| Plaintext letter | Cipher tokens |
| --- | --- |
| a | `4`, `p` |
| b | `f` (tentative) |
| c | `12`, `q` |
| d | `7`, `a` |
| e | `0`, `2` |
| f | `70`, `n` |
| g | `5`, `e` |
| i | `16`, `d` |
| l | `80`, `c` |
| m | `u` |
| n | `19`, `t` |
| o | `s` |
| p | `90`, `y` |
| q | `88` |
| r | `20`, `l` |
| s | `40`, `x` |
| t | `8`, `50`, `b` |
| u | `30` |
| y | `g` |
| z | `14` |

The two existing plaintext spans, beginning `ie vous en responds` and
`et mesurer a cela`, pass through unchanged. The date is already plaintext.
The decoder applies the supplied key; it does not automate recovery of the key.

## Edited reading

These are this project's readings, incorporating the editorial choices documented
below. They are not a transcription of Lasry's or Biermann's original working.

**Modernised French**

> Il n’y a aucun sujet de scrupule de manquer à Dieu ; je vous en réponds, et même
> dans les règles de perfection. Prenez seulement les voies de prudence pour
> conserver votre vie, pour en faire à Dieu un plus grand sacrifice, par la
> multiplication de vos services pour le salut de vos frères, et mesurez à cela
> s’il est meilleur d’agir ou de subir.
>
> 13 mai 1644

**English**

> There is no reason to worry that you are failing in your duty to God; I assure
> you of this, even according to the rules of spiritual perfection. Simply take
> prudent steps to preserve your life, so that you may offer it to God as a
> greater sacrifice by multiplying your services for the salvation of your
> brethren. Judge by that whether it is better to act or to endure.
>
> 13 May 1644

## Findings and uncertainties

Four literal letters conflict with the proposed reading. Positions are numbered
from 1 across encrypted tokens only, as in the output alignment.

| Token position | Cipher → literal | Editorial repair |
| --- | --- | --- |
| 70 | `a` → `d` | `sdulement` → `seulement` |
| 97 | `16` → `i` | `piur` → `pour` |
| 103 | `q` → `c` | `conceruer` → `conseruer` |
| 151 | `g` → `y` | `sacrifiye` → `sacrifice` |

These repairs are confined to the edited reading. Changing the key globally
would alter other occurrences of the same symbols. Their cause remains unresolved.

- **Tentative assignment:** `f` appears once, at token 13. Assigning `f` → `b`
  produces `subiet`, a historical spelling corresponding to `sujet`.
  [Nicot’s 1606 dictionary](https://fr.wikisource.org/wiki/Page:Thresor_de_la_langue_francoyse_-_1606_-_1_-_Nicot.djvu/217)
  attests the spelling; it does not establish this cipher assignment.
- **Additional editing:** `des uos` becomes `de vos`, omitting the `s` at token
  174. The key always gives `30` → `u`; `u/v` and `i/j` distinctions, modern
  spellings, accents, apostrophes, and sentence punctuation are editorial.
  Examples include `subiet` → `sujet`, `reigles` → `règles`, `uoyes` → `voies`,
  `ie` → `je`, `responds` → `réponds`, and `mesmes` → `même`. The existing
  plaintext `mesurer` is edited to `mesurez`.
- **Uncertain ending:** the supplied transcription ends with `soupir`.
  The [article abstract displayed by ResearchGate](https://www.researchgate.net/publication/260410273_Reading_between_the_lines_royalist_letters_and_encryption_in_the_English_civil_wars)
  gives `soubir`. The edited `subir` / “endure” follows that variant and remains
  uncertain. This word is already plaintext and supplies no evidence for the key.
- **Verification scope:** all 207 encrypted tokens are retained, every observed
  symbol is mapped, and the decoder applies no position-specific substitutions.
  Tests establish mechanical reproducibility. The archive’s 203/207 agreement
  with a proposed comparison reading measures internal consistency, not
  independently established accuracy or statistical confidence.

The interpretation is counsel to preserve one’s life for continued service to
God and one’s brethren. It does not identify the correspondent or establish a
specific political event. The published passage may be only part of a letter;
no missing text is supplied here.

## Sources and provenance

Prepared from `forster_end_to_end_evidence.zip`. Its 13 manifest checksums were
verified; the input, key, decoder, tests, and stored output retain their supplied
contents. The narrative and editorial notes are consolidated in this document.
Robert Pitt, a software engineer experimenting with modern AI, assembled this
AI-assisted reconstruction and reproducible repository. The earlier decipherments
are credited in the update above.

- Karen Britland, [“Reading between the lines: royalist letters and encryption
  in the English civil wars”](https://onlinelibrary.wiley.com/doi/10.1111/criq.12072),
  *Critical Quarterly* 55(4), 15–26 (December 2013 issue; published online
  21 January 2014), DOI: 10.1111/criq.12072. Note 1 identifies the Forster papers
  as **Archives départementales (Val-d’Oise), MS 68.H.8, troisième liasse**.
  This is the published reference; no manuscript image was available for verification.
- [Publisher’s first-page image](https://onlinelibrary.wiley.com/cms/asset/74d4d7e9-abb5-4ab0-95ba-a9a271a1d09c/criq.12072.fp.png):
  the typeset transcription identified in the supplied evidence, rather than
  a photograph of the manuscript.
- [Cryptiana, September 2021 archive](https://cryptiana.blogspot.com/2021/09/):
  the supplied evidence identifies the 21 September entry as a reproduction of
  Britland’s ciphertext, not an independent manuscript transcription.

## License

This repository’s code, key, and editorial documentation are released under the
[MIT License](LICENSE), permitting free use, modification, and redistribution,
including commercial use. The historical passage is attributed above; the license
does not extend to external publications linked as sources.
