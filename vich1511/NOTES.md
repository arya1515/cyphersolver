# Ferdinand the Catholic → Jerónimo de Vich (Rome), AHN Estado 8715

PARES search "Vich cifrada" lists the ciphered letters in the Vich archive (AHN, Archivos privados):

| Signature | Date | PARES id | Status on PARES |
|---|---|---|---|
| 8714 N.12 | 1508-09-30 | 12751356 | with decipherment |
| 8714 N.26 | 1509-07-28 | 12751370 | with decipherment |
| 8714 N.39 | 1510-05-13 | 12751383 | with decipherment |
| 8715 N.41 | 1510-05-22 | 12751386 | with decipherment |
| 8715 N.45 | 1511-04-04 | 12751390 | **cipher only** |
| 8715 N.46 | 1511-07-05 | 12751391 | with decipherment (used for the key) |
| 8715 N.52BIS | 1512-03-01 | 12760824 | with decipherment (used for the key) |
| 8715 N.57 | 1512-06-05 | 12751402 | **cipher only — read here** |
| 8715 N.60 | 1512-09-01 | 12751405 | **cipher only**, same system (same code groups: `fak`, `diz`, `pef`, `sub`, `goy`, `fol`) |
| 8715 N.73 | 1515-10-26 | 12751418 | **cipher only**, *different* system (groups `xed`, `yob`, `tok`, `zre`) |
| 8715 N.74 | 1519-01-30 | 12751419 | Charles I, with decipherment, different system |
| 8715 N.79 | "1500" | 12751424 | "Clave de cifra" (2 images, not yet examined) |

No publication of N.57's text was found (web search, 2026-09-18).

## The 1511–12 system

A small code (three-letter lowercase pseudo-syllables, CVC: `pef` que, `diz` de, `fak` el, `fem` es,
`fan` en, `hor` la, `has` lo, `mix` papa, `hib` guerra, `fef` emperador, `sap` venecianos …) mixed
with a homophonic alphabet of figures and marks (`40` r, `4h`/`3` e, `ah`/`T` o, `to`/`7`/`b` a,
`ch` c, `oo` d, `d`/`eh` s, `11`/`W` n, `X`/`g`/`9` t …). Words are spelled out when not in the code.
Values: `decode.py`. They come from lining up N.46 and N.52BIS against the clerk's decipherments.
The glyph labels are my own ASCII names for the symbols; the legend is at the top of
`n57_transcription.txt`.

## N.57, Burgos, 5 June 1512: reading

The decode (`n57_decode_v1.txt`) runs as continuous Castilian for about 90% of the text. About 40
groups are still unassigned. They are shown in brackets there and marked "…" below.

The subject is the **battle of Ravenna (11 April 1512)**. Ferdinand blames the viceroy
(*nuestro capitán general*, Ramón de Cardona) for accepting battle against every rule of war. He says
the army was pushed into it by the papal side's threats that the Pope would stop paying and come to terms
with France. He tells Vich not to repeat the mistake, to get the Pope and Venice to pay their share,
and to arrange a matter secretly, "without the Pope feeling it", and report back.

Normalised reading, with gaps:

> … los de nuestro campo que vieron … y los que nos escrivieron … que las cosas que vos … continuo
> les escrevistes, apretando lo sobre … con grandíssima … de su capitán general, muy principalmente
> que no cumpliese sino lo que yo por tantas cartas les he enviado a dezir, y según … encarecidamente
> me escrevía de antes de la batalla, que por la vida no convenía que se retirasen … diziéndole que
> assí ge lo he escrito a mi aviso. Conozco que dizen verdad, y que el miedo que tenían de los que
> estavan … y las cosas que de[b]í escrevía del nuestro campo el capitán general, que los que estavan
> en él pervirtiessen toda la orden de guerra; porque la verdad es que todo … del comienço … el cabo …
> contra toda orden de guerra. Y dizen que … por vos … assí, porque a cada cosa … les dezía que si no la
> hazían el Papa no cumpliría la paga y que se concertaría con … y por otra … mi cabo escrevía … que se …
> si se retirassen; que estas cosas lo apretaron a que se pusiessen en la … y desaventajados que se
> pusieron, ya que no fiziessen lo que yo les he enviado a dezir. Que claro está que no se … no
> retirarse, que está lo que vos les escrevíades de ponerse en … donde no viniesse a batalla, que está lo
> que yo les … conocía que en esto estava la … porque lo … y tened por cierto que las cosas de guerra es
> muy peligroso … lo que están ausentes dellas, que siempre se ha de remitir a los que las tienen
> presentes. … Todo esto digo porque de aquí adelante miréys mucho en no caer en tal yerro, que sería
> echar la soga tras el caldero. Lo que en este caso de la guerra toca a vos, es procurar que el Papa y
> venecianos cumplan … su parte de la paga, que por la … negociar muy bien lo … y la conclusión de lo
> del Emperador y … las otras negociaciones, que puede[n] daño … para el bien de la empresa, y la de …
> no la tengáys en poco … que hazía se bien aquella en ella … Y digo que la tratéys … sin que la sienta
> el Papa, y teniéndola concertada hazédmelo saber, que yo daré orden cómo se efectúe.
> — En Burgos a v de junio de dxij.

**Checks that the key is right:** the key taken from N.46 and N.52BIS reads a letter it was not built
from. Place and date agree with the clear-text subscription (Burgos, 5 June 1512). The topic fits the
date: Ravenna, and the payment dispute inside the Holy League. The proverb *echar la soga tras el
caldero* comes out of spelled-out letters, which are not code words.

## Still open

- About 40 unassigned groups in N.57 (`sil`, `goe`, `gue`, `rug`, `hno`, `fep`, `sig`, `mag`, `feg` …).
  More sibling alignment would close most of them; N.41 and the 8714 decipherments are untouched.
- N.45 and N.60 are in the same system and are the next letters to read.
- N.73 (1515) is a different key.
- N.79 "Clave de cifra" is not yet examined.
