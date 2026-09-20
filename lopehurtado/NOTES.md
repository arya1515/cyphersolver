# Lope Hurtado de Mendoza (Rome) to Charles V, 1522 — RAH Salazar 9/26, DECODE R9634–R9656

Status: in progress (key being rebuilt from a contemporary decipherment; first values fixed)

Catalogue entry 144 ("Lope Hurtado de Mendoza (Rome) to unknown recipient, 8 ciphertexts",
RAH Signatura 9/26). Opened 2026-09-20, after the sanchez1522 session established that these letters
are **not** in Alonso Sánchez's cipher.

## Why this is a separate target

The nine Lope Hurtado records are bound in Salazar 9/26 among Sánchez's, were catalogued with them,
and look at first like more of the same: same months, same recipient, cipher mixed with clear inside
the sentence, code groups of the same shape. They are in a different cipher. Sánchez's codes end
strictly in `b c d f g h l m n`; Hurtado's take finals `p` and `z` (`tep`, `tap`, and groups ending
`-z`). See `../sanchez1522/NOTES.md`.

## Prior art: none

Tomokiyo's *Correspondence in Cipher of Imperial Ambassadors Alonso Sanchez and Juan Manuel (1522)*
(Cryptiana, 6 Sept 2025) reconstructs **Sánchez's** and **Juan Manuel's** ciphers. It does not mention
Lope Hurtado, and his records R9634–R9656 fall outside both ranges it lists. A web search for a
decipherment of his cipher returns nothing. **This key has not been published.**

## The records

| DECODE | 9/26 ff. | date 1522 | pp | DECODE status |
|---|---|---|---|---|
| R9634 | 14–16 | Sept | 6 | Non-decrypted |
| R9644 | 237–243 | 1 Nov | 14 | **Decrypted** |
| R9645 | 243–244 | Nov | 4 | Non-decrypted |
| R9646 | 252 | — | 2 | Non-decrypted |
| R9648 | 260–265 | 9 Nov | 12 | Non-decrypted |
| R9649 | 266–268 | 9 Nov | 6 | Non-decrypted |
| R9650 | 269–272 | — | 10 | **Decrypted** |
| R9652 | 295–296 | Nov | 2 | Partially decrypted |
| R9656 | 334–335 | Nov | 4 | Non-decrypted |

Images in `img/` (git-ignored; RAH material, fetched from DECODE 2026-09-20).

## The crib: R9644 carries its own decipherment

R9644 is the way in. The record holds **both** the ciphered letter (ff. 238–239) **and a full clear
version of it** (f. 242), the clear headed and closed with *Claro* section by section, and keyed to
the cipher by **marginal letters A, B, C** written against the matching passages on both.

So the attack is a straight crib: align the cipher against the clerk's own plaintext, token by token,
wherever the word counts match exactly.

## First values, fixed against the clear

The clear (f. 242) reads:

> … y que los que le tienen por frances veen si sus officios y fortalezas y servicio de su casa lo
> haze con franceses o castellanos. Su Sa[ntidad], a lo que yo pienso, espera lo que hara el
> arçobispo de Bari, y no gastar nada si ser pudiesse, porque esta tan escasso **que nunca hombre lo
> fue mas**; hasta que el arçobispo venga creo que sera mejor **no apretallo mucho**.

The cipher (f. 238) runs, with *hasta que el arçobispo venga creo que sera mejor* standing in the
clear on the cipher page itself:

```
… ton  tab    xud     xul  ɣm   xon  │ hasta q el arçobispo venga creo q sera mejor │ tu  ᵷʒ℔ʒ ʒ7 ∞ʒ ɸeɋ
    que nunca hombre  lo   fue  mas                                                    no  a-p-r-e-t-a-ll-o  mucho
```

Six tokens against six words, in a sentence with no room for slippage:

| code | value |
|---|---|
| `ton` | **que** |
| `tab` | **nunca** |
| `xud` | **hombre** |
| `xul` | **lo** |
| `ɣm` | **fue** |
| `xon` | **mas** |
| `tu` | **no** |

`ton` = *que* settles the point that this is not Sánchez's key, where *que* is `ho`.

Carried in `key_codes.tsv`.

## A second anchor, on the same leaf

Lower on f. 238 the cipher runs `… ɣof ∞7∞ᵷLʒ#8ʃ3m zun top │ descargo de los q │ …`, with
*descargo de los q* standing in the clear on the cipher page. The plaintext at that point (f. 242)
reads:

> … las obras ningun servidor de v. ma la esta satisfecho; **da por descargo** de lo que dexa de
> fazer la obligacion que tiene a procurar la paz …

So `zun top` = **da por**, which

- **confirms `top` = *por*** in a second, independent context (the first was `top ton` = *porque*);
- gives **`zun` = *da***;
- and shows the ten-sign run `∞7∞ᵷLʒ#8ʃ3m` standing where *satisfecho* must be, and the eight-sign
  run `Ɉ℔ɸʒx℔4` where *servidor* must be — so long words are spelled out letter by letter between the
  codes, as in Sánchez's cipher.

Nine values are now confirmed against the clerk's own plaintext, twelve more probable. The
`key_codes.tsv` file keeps the two apart in a `confidence` column; nothing probable is being used to
derive anything else.

## The key is shared across his letters

R9650 (9/26 ff. 269–272, the other *Decrypted* record) carries the same forms. On f. 270:

> `ᵹᵹʒ` **`ton` `tab` `xud`** `ɣifLᵹ` `zil` `tod` · **`tu`** `ʃʃ℔℔ᵹLᵷ9ʒ7` `zun℔` `xil` `to7` **`top`** ·
> *disimular en este caso v. Mt.*

`ton tab xud` stands there in identical forms, and `top` again immediately precedes clear words in a
slot that reads *por disimular en este caso* — a **third** independent context for `top` = *por*.
`tu` and `zun` recur too.

So Hurtado used one key across these letters, and values won on R9644 carry to the rest. That is what
makes the six non-decrypted records reachable once the key is far enough along.

## Next

- Work the rest of the R9644 alignment section by section, using the marginal A/B/C keys.
- Then R9650 (also *Decrypted*) and R9652 (*Partially decrypted*) as further cribs.
- Then apply the rebuilt key to the six non-decrypted records.
- Test whether the key is Juan Manuel's: Tomokiyo's Juan Manuel table has `ton` unassigned, so the
  values above do not yet contradict it, and the question stays open.
