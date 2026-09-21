# R9683 — f. 171r, Rome [x]vi June 1523, to the Emperor (read in part; cipher mostly unread)

**Image:** img/IMG_R9683_I45594_P.jpg. Right = f.171r (modern foliation 171, older 173).
**Docket (left page, written vertically):** "Al Rey — 1523 — de Roma / Del Protonotario [Lope Hurtado?] / diez de junio" (my first reading "Caracciolo" withdrawn — see cross-check).
Read as "Protonotario Caracciolo" (Marino Caracciolo?) — reading of the surname uncertain. NB the letter itself is
signed at the foot with an autograph subscription ending "…Lope Hurtado"(?) under a holograph courtesy formula;
the docket's sender and the signature need checking against each other (not resolved here). Docket date "diez de
junio" vs the letter's "vi de junio" (a digit before vi may be lost: xvi?).

## Clear text (f.171r)
S. C. C. Md. / Por las letras del Duque y despacho que embia entendera V. Md. las cosas de aca en el estado que estan
y la buena voluntad que Su Bt tiene a los negocios de V. Md. Spero que seran tales las obras y assi se ha visto en lo
que se offresce despues de la prision de Volterra, tanto que ya lo conocen todos en esta corte, y estan las cosas en
ella como conviene al servicio de V. Md. Los criados del papa muestran la voluntad que son obligados **[cipher a1–a5]**
esta bienquisto **[a4 cont.]** aprovecharia que V. Md. mandasse remediar lo de los beneficios del camarero y Francisco,
porque ha perado[?] mucho a su Santidad que V. Md. gelos haya quitado, y ellos y los otros estan agraviados. Asimismo
sera muy bien que V. Md. mande pagar al papa lo que se le deve alla, que contentando a su Bt en esto podria aprovechar
**[cipher b1]** y para otras cosas que V. Md. quiere. Y porque por otras tengo scripto a V. Md. largo, aqui no digo mas.
N. S. guarde la muy real persona de V. A. con acrescentamiento de muchos reynos y señorios. En Roma [x]vi de junio 1523.
(autograph subscription and signature, not transcribed)

## Cipher, token by token (`r9683_cipher.txt`) and mechanical decode
```
a1 de <t> <h> e o d ?&
a2 ?eo <i> c o que so l el ?ʃag r d ?σʇʇ x a ?ze esta mas ?zal
a3 a ?ʃag ?zef ?xin para ?tal <r> ?ʃibL y con lo <t> ?tod s <t> e
a4 <ha> da d o r <r> en a ?ʃ ?ʇʇo n d a el ?yib
a5 <t> e ?sid e ?zer ?ʑ para con s ?H r i/j a i/j ?& <t>
b1 para que la ?ʃʇ r u ?ï a d a <Roma> s ?D a de la d e ?H
coverage 67/91 = 74%
```
## Best reading
…que son obligados, de […] que sol[o] el […] esta mas […] para […] y con los otros […] el […] esta bienquisto
[…] aprovecharia … / …podria aprovechar para que la […] de la […] y para otras cosas…
Recognisable only: "que solo el", "esta mas", "para", "con los otros" (tod c = otros, 1522 key), "el [name] esta
bienquisto", "para que la". `yub yib` = "el" + an unknown group, probably a person (subject of "esta bienquisto").
`tuf` in b1 would be "Roma" if the R9867 value holds — it does not fit well here ("Romas"?), so tuf = Roma stays probable.

## English gist
Clear: the Duke [of Sessa]'s letters report the Pope's good will after the arrest of [Cardinal Soderini of] Volterra;
the papal household is well disposed; the Emperor should restore the benefices of the chamberlain [Pedro] and
Francisco, and pay the Pope what is owed him. The cipher passages (who is well liked, what the payment would serve)
are not read.

## Coverage
67 / 91 tokens (74 %) by script, but as words: under a third of the cipher reads. Read in part (clear text only).

## Cross-check with the other session's trans_R9683.md (C:\Users\dbour\cypher\lopehurtado1523, read-only)
- Docket: they read "Del Protonotario Lope Hurtado de diez de junio"; I first read the surname as "Carrazolo/Caracciolo".
  Theirs fits the signature (Lope Hurtado was protonotary) — adopted as probable. Letter date: they read "x de junio",
  I read "[x]vi"; the docket's "diez" favours x (10 June 1523).
- Tokens agree on ~85 %: a1 they `zar ∂ z 8 ɣ 9 &` vs mine `zar ∂ 3 8 y 9 &` (sign 3 vs z); a2 they `rub?` vs mine `yub`,
  `o#` (one sign) vs my `σʇʇ`; a4 `ʃ#o?` vs `ʃ ʇʇo`; a5 their first group `dd-e?` = my `∂ 8`; b1 their `gJ` = my `ʃʇ`,
  `Tb` = my `⊤`. Their count 84 tokens vs my 91 (they join some pairs). None of the disagreements changes a reading.
