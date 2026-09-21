# Kurz von Senftenau cipher, 1638-39: the rebuilt key

Rebuilt 19 Sept 2026 from the contemporary interlinear decipherment on R3811 p.1 and the structure it shows, then
extended with a German n-gram model and read-through. `key.json` is the machine form (H41 = consonant of 41-45, etc.).

## Consonant+vowel signs 41-100

Each ten is split into two halves with one consonant each, in reverse alphabetical order from 41 (r p n m l k h g d c b).
Units 1-4 of a half run o i e a with that half's consonant. The fifth place of every half is a separate series of
consonant+u signs in its own order (pu lu mu hu ku du gu bu cu . us ru), found from context, not from the table pattern.

| | +1 o | +2 i | +3 e | +4 a | +5 |
|---|---|---|---|---|---|
| 41-45 | ro (68) | ri (173) | re (433) | ra (185) | pu (21) |
| 46-50 | po (57) | pi (24) | pe (74) | pa (47) | lu (55) |
| 51-55 | no (59) | ni (258) | ne (229) | na (51) | mu (33) |
| 56-60 | mo (26) | mi (120) | me (132) | ma (154) | hu (31) |
| 61-65 | lo (78) | li (207) | le (168) | la (109) | ku (7) |
| 66-70 | ko (60) | ki (10) | ke (33) | ka (29) | du (29) |
| 71-75 | ho (59) | hi (72) | he (203) | ha (126) | gu (27) |
| 76-80 | go (13) | gi (48) | ge (329) | ga (37) | bu (51) |
| 81-85 | do (21) | di (213) | de (517) | da (135) | cu (28) |
| 86-90 | co (114) | ci (65) | ce (17) | ca (35) | cu (1) |
| 91-95 | bo (15) | bi (20) | be (301) | ba (34) | us (17) |
| 96-100 | ? (0) | is (24) | es (24) | e (17) | ru (68) |

Irregular: 97 = is, 98 = es, 99 = e (uncertain), 100 = ru; 96 not seen.

## Single signs (numbers 1-40, letters, graphic signs)

| sign | value | count |
|---|---|---|
| `28` | r | 1421 |
| `31` | n | 1392 |
| `27` | s | 1265 |
| `26` | t | 1145 |
| `39` | c | 856 |
| `35` | h | 670 |
| `18` | e | 608 |
| `19` | e | 514 |
| `17` | i | 511 |
| `33` | l | 499 |
| `#z-tail` | n | 497 |
| `w` | n | 470 |
| `9` | te | 456 |
| `37` | f | 428 |
| `36` | g | 342 |
| `15` | i | 341 |
| `25` | u | 309 |
| `22` | a | 302 |
| `π` | m | 298 |
| `ψ` | z | 258 |
| `38` | g | 244 |
| `#s-long` | t | 240 |
| `40` | b | 225 |
| `21` | a | 223 |
| `10` | u | 222 |
| `x` | i | 212 |
| `6` | se | 204 |
| `20` | e | 200 |
| `13` | o | 195 |
| `11` | u | 189 |
| `23` | a | 186 |
| `16` | i | 183 |
| `c` | si | 183 |
| `#4-hook` | w | 173 |
| `24` | w | 165 |
| `34` | k | 160 |
| `α` | m | 151 |
| `p` | null / unread | 134 |
| `30` | p | 131 |
| `d` | so | 123 |
| `n` | ve | 119 |
| `12` | o | 98 |
| `14` | o | 97 |
| `32` | m | 95 |
| `#l-loop` | tu | 68 |
| `#s-loop` | null / unread | 60 |
| `29` | qu | 53 |
| `φ` | z | 45 |
| `Δ` | e | 44 |
| `#dot` | null / unread | 42 |
| `1` | i | 29 |
| `3` | null / unread | 27 |
| `m` | null / unread | 23 |
| `4` | null / unread | 22 |
| `#sect` | w | 18 |
| `7` | s | 17 |
| `k` | ti | 15 |
| `λ` | null / unread | 13 |
| `5` | sch | 11 |
| `v` | s | 8 |
| `2` | null / unread | 8 |
| `0` | ti | 8 |
| `#s-cross` | t | 7 |
| `e` | null / unread | 7 |
| `2?` | ? | 6 |
| `8` | s | 4 |
| `3?` | ? | 4 |
| `4?` | ? | 4 |
| `#hash` | s | 4 |
| `r` | i | 3 |
| `?` | ? | 3 |
| `#z-bar` | e | 3 |

Values of signs seen fewer than 3 times are in key.json and are uncertain. Two-letter values for single signs (9 te, 6 se,
c si, n ve, d so, k ti, #l-loop tu) were fixed from context and the glosses.


## Revisions, 21 Sept 2026 (second pass)

- α (small upright a) = **sa**, not m; the larger looped ℒ-form is a separate sign, `#a-loop` = **m**.
- `#f-cross` (crossed ƒ-like sign, R3813) = **ta**; pass 1 had merged it with `x` (i).
