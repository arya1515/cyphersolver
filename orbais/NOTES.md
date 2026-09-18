# BnF fr. 3413 no. 62 — letter to the abbé d'Orbais (Rome, 23 August [1589])

Catalogue item: "Letter to the abbé d'Orbais, with three loose keys in the volume" (Gallica `btv1b52510705j`).

## The letter

- ff. 126r–127r (canvases 259–261), address on f. 127v (canvas 262): "A Monsieur / Monsieur l'Abbé d'Orbais Con[seill]er
  au Conseil estably a Paris pour la S[ain]te Union / A Paris". The abbé d'Orbais is Jean de Piles, the League's envoy to Rome
  in 1589.
- The letter is **almost entirely in clear**. It is dated "du lieu que vous sçavez ce xxiij d'Aoust" and written from Rome,
  by a secretary of Cardinal Pellevé. It carries the news of Henri III's death. A courier from Spain passed through Lyon
  on the 12th. A courier from the Grand Duke of Tuscany arrived on the 20th. The Duke of Lorraine's letter from
  "le s. Bardin, son agent à Paris", dated 8 August, says: "le Roy a esté tué, et c'est le Roy de Navarre qui l'a faict faire;
  l'on a proclamé Roy à Paris Mons. le Cardinal de Bourbon"...
- There are about 10 short cipher groups, roughly 90 signs in all, including the writer's own name at the signature.
- The writer apologises that Cassin, "son aisné de mesme charge", is ill: "Mons. [Cassin] detenu d'une fiebvre dès il y a
  quinze jours". So the writer is Cassin's junior colleague in Pellevé's household.

## The three bound keys: none fits

| no. | folio (canvas) | what it is | test on no. 62 |
|---|---|---|---|
| 53 | f. 109 (227) | Numeric French key: letters → 2-digit numbers, nomenclator 1–99 (Tomokiyo: = Nevers collection no. 42) | No. The letter has no numbers. |
| 61 | f. 125 (257) | Italian key (Savoy/Piedmont: Birago, Saluzzo, Carmagnola…), symbol alphabet, nomenclator 80–204 | No. Its alphabet does not give c-a-s-i-n, and has no W, ÷ or ◻ in those values. |
| 69 | ff. 137–138 (281–284) | French League key: place-name nomenclator 1–171 plus boxed numbers, symbol alphabet written sideways on f. 138 | No. Here ◻ = e, there is no W, and "Cassin" does not come out. |

## The cipher: Tomokiyo's "Nevers-Piles" alphabet

Tomokiyo (cryptiana `nevers.htm`, section BnF fr. 3413) already said that no. 62 "appears to employ the Nevers-Piles
Cipher, which reveals the name of Mons. Cassin". His partial table was reconstructed from fr. 3612 f. 9, which is not digitised.
A copy is in `NeversPiles.png`. It confirms these readings:

- "Mons. **W V ÷ 9 ◻**" = **Cassin** (W=c, V=a, ÷=s, 9=i, ◻=n).

These readings are new (cribs from context, all mutually consistent):

- "Il ne fault oublier [Θ v] **b ⊡ m ooo Θ W 8 φ tt ◻** que vous sçavez pour beaucoup de raisons" = **la protection**.
  So b=p, ⊡ (dotted square)=r, m=o, ooo=t, Θ (crossed tt)=e, 8=t, φ=i, tt=o, ◻ (plain square)=n.
- "Maintenant que vous serez à **ɔ tt ÷ ooo ⊡ Θ** [na æ η ◻ Θ] si l'histoire est vraye" = **vostre** (ɔ=v). The next group
  ends -gne (η=g), for example "…aigne". "Champaigne" is only a guess; Orbais is in Champagne.
- Signature: "vostre treshumble servit[eu]r **2 V ⊡ m ħ** p[rese]nte ses treshumbles recommandations": b-a-r-o-? (2=b as in
  the key). The name is probably **Baron** or Barot. The annealer also lands on "baron" in every run.

## Open groups

Transcription labels as in `solve.py`:

1. "Les jugemens de Dieu sont fort profons et inscrutables. **b 1 6 Θ ÷ | W 4 æ ⊡ − ʃ** dedans deux jours
   **Ƒ 3 tt ħ Θ ◻**." The first group is plausibly "…se sçaura" (÷ W 4 æ ⊡ − = s-ç-a-u-r-a), but 4=a and æ=u go against the table.
   Unread.
2. "Il ne vous fault rien dire pour ce qui touche **φ tt o v æ ʃ ÷**." Unread. It looks like "?o pa?ts" / "vos …".
3. "Depuis que **⌘ Ƒ τ æ Θ ◻ ∇ V 9 | ooo ◻ Θ** a esté retiré **ʃ ɔ Θ φ ɔ ◻ η − 7 6 φ 2** qui **W Θ ◻ Θ 9 ⊡ æ æ**
   plus particulierement que nul aultre." ⌘ is a decorated square, probably a title code ("Mr"/"Card.").
   The first group ends "…n ? a i t n e". Unread.

The glyph values in Tomokiyo's table are partial and some disagree with the cribs (his b=u, m=r, 8=c; the cribs give p, o, t).
So the table can't be applied blindly.

## Other sources tried

- **BnF fr. 4715 f. 2** (Gallica `btv1b52509819x`, canvas 17): Cardinal de Guise to Nevers, Soissons, 6 Oct 1586. Tomokiyo
  says it is in the same Nevers-Piles cipher, and it has an interlinear decipherment. It is a full page (~900 signs) in the
  same glyph family (W, ÷, ◻, 9, φ, æ, ooo, 3, 1, 7, ∇, η). The clear text is written *above* each cipher line: "Certes"
  sits over W c e ɔ o ✕, so W=c. But the interlinear is sparse and cursive, and not letter-aligned. Recovering the key from it
  would need a full transcription of the page (the sormano-style segment/cluster pipeline). That is the next step if this
  letter is to be finished.
- **fr. 3612** (Tomokiyo's source for the table): catalogue notice `cc50062c` has no Gallica link, so it is not digitised.
- Nevers-Pellevé and Nevers-Guise tables (`NeversPelleve.png`, `NeversGuise.png`): different glyph sets, no fit.
- `solve.py` anneals the unread signs under a 6-gram French LM, with each group scored in its clear-text context.
  The groups are too short: it only stabilises the signature ("baron").

## Status

The bound keys are **tested and none fits**. The cipher is identified as Tomokiyo's Nevers-Piles alphabet. The letter's
substance is in clear (above). The cipher groups are read **in part**: Cassin, "la protection", "vostre", the signature
b-a-r-o-?. About 5 groups (~55 signs) remain unread. They need the fr. 4715 f. 2 transcription or the fr. 3612 key.

Images: `img/` (git-ignored). Crops `grp_*.jpg` show each cipher group at native resolution.
