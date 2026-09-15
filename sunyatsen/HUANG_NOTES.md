# Huang Xing to Lin Hu and Li Genyuan, 25 May 1916 (JACAR B03050731500) — scheme identified

Catalogue status on cryptiana: **"Solved but Specific Scheme Unknown"**. Tomokiyo found a memo that the
Japanese Foreign Ministry had filed a decode with the telegram, but reported he could not read the
handwritten Chinese and could not identify the encryption scheme. This note supplies both.

## 1. The file

JACAR **B03050731500** = Gaimushō record 1.6.1.75-1_015, reel 1-0955, frames 0244–0302 (59 images).
Fetched as a PDF from `…/content/item/aj12/C200138859200/raw/B03050731500.b10148.1-0955.00000244.pdf`
(the viewer is a single-page app; the `raw` path is in the page's `data-src`/JSON).

Covering note (frame 0244–0245), 電送第一九八〇号, cipher, **25 May 1916, 4.35 p.m.**, Foreign Minister
**Ishii** → Consul **Ōta at Zhaoqing (肇慶)**, no. 22:

> 黄興ヨリ林虎李根源宛電報依頼アリタルニ付同人ニ伝達アリタシ　内容ハ先日来電ノ挨拶ナリ（以下支那側暗号）

"Huang Xing has asked that a telegram be sent to Lin Hu and Li Genyuan; please pass it to them. The content
is an acknowledgement of the telegram received the other day. (Chinese-side cipher follows.)"

| frame | content |
|---|---|
| 0246 | the telegram itself, on an **Imperial Government Telegraphs** forwarded-message form |
| 0247 | **電稿** — the decoded Chinese text, cursive, five columns |
| 0248 | the clerk's **annotated reading** in Japanese word order, on 外務省 ruled paper |

## 2. The plaintext

From frames 0247 and 0248 together. The clerk's own glosses are in brackets.

> 隱印崧蕘邕行諸兄鑒　〔林虎・李根源等ノ字ナラン＝probably the courtesy names of Lin Hu, Li Genyuan and others〕
> 正發書翰之際，適接哿〔二十日〕電，敬悉一切。
> 護國軍能速入湘贛〔＝湖南江西〕甚好。
> 章行嚴〔Zhang Shizhao〕何日東渡〔日本ニ来ルヤ〕？速令出發，並望預電。
> 興　徑〔二十五日〕

"To brothers Yin, Yin, Song, Yao and Yongxing: just as I was sending a letter, your telegram of the 20th
arrived, and I have respectfully noted it all. It would be excellent if the National Protection Army could
move quickly into Hunan and Jiangxi. What day does Zhang Xingyan cross to Japan? Have him start at once,
and please wire me in advance. — Xing, the 25th."

Both date characters are 韻目代日 rhyme-codes: **哿 = 20**, **徑 = 25**, and 徑 matches the dispatch date
on the covering note exactly. Several characters of the cursive are still uncertain; the column lengths are
2 + 12 + 11 + 12 + 11, i.e. **46 characters** of message after the 電稿 heading. (Tomokiyo's note gives the
same column lengths but sums them as 68; they add to 48.)

## 3. The scheme

139 kana, no voicing marks, packed into ten-letter telegraph words. 46 characters into 138 kana is
**three kana per character**, with one kana left over at the end.

The gojūon syllabary is a 10 × 5 grid: ten consonant rows (—, k, s, t, n, h, m, y, r, w) by five vowels.
Group the kana in threes and ask which part carries the information (`huang.py`):

| reading | collisions in 46 groups | expected by chance | permutation p |
|---|---|---|---|
| consonant row | **7** | 1.03 | **0.006** |
| vowel | 8 | 8.28 | 0.70 |
| literal kana | 1 | — | — |

**Each kana carries one decimal digit in its consonant row; the vowel is a free homophone.** Every digit can
be written five ways, which is what makes the cipher look like pronounceable Japanese and why the surface
text almost never repeats. The repeated triples show the mechanism directly — the same character written
two different ways:

```
S K N   at 4, 35    SE-KA-NA  /  SHI-KO-NU
R - H   at 9, 13    RE-U-HO   /  RE-O-HI
T - H   at 2, 22    TA-U-HO   /  TE-U-HI
S K H   at 12, 18   SA-KU-FU  /  SHI-KI-HE
```

Three digits per character means a **private codebook of at most 1000 entries** — not the four-digit
standard Chinese telegraph code, and not Yamada's 20 × 5 condenser used in the Swatow telegram
(`NOTES.md`), which packs two digits into each kana-like syllable. This is a different and simpler design.

## 4. What is left

* the permutation mapping the ten consonant rows to the ten digits (10! but heavily constrained once any
  codebook is assumed, and constrained already by the repeat pattern);
* the codebook itself. With 46 characters of known plaintext aligned to 46 code triples, 46 entries of it
  are directly recoverable — the blocker is an exact character-by-character transcription of the cursive
  on frame 0247, where several glyphs remain uncertain.

Reproduce: `python huang.py` (no data files needed; ciphertext is in the script).
