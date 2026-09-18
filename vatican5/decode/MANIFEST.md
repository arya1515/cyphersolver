# DECODE downloads needed for Vatican Challenge Part 5 (ASV Segr. Stato Spagna 1A)

Public metadata read 2026-09-16 from `https://de-crypt.org/decrypt-web/RecordsView/<id>`. All images and documents
are "Access mode: Authentication required"; the file server is `https://de-crypt.org/decrypt-custom/filesrv/?file=<name>`
(thumbnail names carry a `TH_` prefix; the full image is the same name without it). Save everything into this folder,
keeping the DECODE file names.

## Record 92 — ASV_i1025_SdS_Spain_IA-2 (Part 5 itself, 8 pages, ff. 69v-73r, Non-decrypted)  **priority 1**

| file | what |
|---|---|
| IMG_R92_I691_P1.jpg … IMG_R92_I698_P8.jpg | the eight page images (069v cleartext frame, 070r onward cipher) |
| DOC_R92_D1633_1633.txt | DECODE transcription (compare with the MysteryTwister text `../ASV_i1025_SdS_Spain_IA-2.txt`) |
| DOC_R92_D1211_1211.png | document image attached to the record (probably the transcription rendered or a key sketch) |

## Record 91 — Spain IA-1 sibling letter (5 pages, ff. 62v-66v, Non-decrypted)  **priority 2**

| file | what |
|---|---|
| IMG_R91_I682_P1.jpg … IMG_R91_I686_P5.jpg | page images (062v, 063r, 063v, …, 066v) |
| DOC_R91_D2341_2341.txt | transcription |
| DOC_R91_D1207_1207.png … DOC_R91_D1210_1210.png | four document images |

## Record 93 — Cardinal Alessandrino to the nuncio, 1570, Partially decrypted (key S6)  **priority 3**

| file | what |
|---|---|
| DOC_R93_D1664_1664.txt, DOC_R93_D3287_3287.txt | transcription and `s6key.txt` (the record lists s6key.txt) |
| DOC_R93_D1212_1212.png … DOC_R93_D1219_1219.png | eight document images (ff. 3v-11r) |
| IMG_R93_I700_P1.jpg | page image |

## Record 94 — same series, 1570, Partially decrypted  **priority 3**

| file | what |
|---|---|
| DOC_R94_D1665_1665.txt, DOC_R94_D3285_3285.txt | transcription / key |
| DOC_R94_D1220_1220.png … DOC_R94_D1237_1237.png | eighteen document images (ff. 37v-52r) |
| IMG_R94_I709_P1.jpg | page image |

Also listed on every record: `Heder_111_32898863_ny.pdf` and `decode-histocrypt-2019.pdf` (project papers, not needed).

## How to fetch

Option A (by hand): open each RecordsView page while logged in, click each image and each document link, save into
this folder. Record 92 alone is 10 files and is enough to start.

Option B (script): in the browser's developer tools, copy the `Cookie:` request header of any de-crypt.org request
into a file named `cookie.txt` in this folder (one line, the header value only), then run

    python fetch_decode.py 92          # or: python fetch_decode.py 92 91 93 94

The script never prints or stores the cookie anywhere else; delete `cookie.txt` afterwards (it is git-ignored).

**Fetched 2026-09-18** (records 92 and 91, all files; 93-94 not fetched). Results in `../NOTES.md`, section
"2026-09-18": DECODE's R92 transcription is byte-identical to the MysteryTwister text; the image re-read is
`reread/*.txt` → `../IA-2_reread.txt`; IA-1 is a different key.

## What the files settle

George Lasry (e-mail to Daniel, 16 Sep 2026, copying Beata Megyesi): in the Challenge 5 documents, unlike other
collections, **there are no visual separators (dots, commas, wider spaces) between logical tokens**; recognising
variable-length tokens is the challenge, and that is why it is rated Level X. So the images will *not* restore a word
division, and NOTES.md "Final status" point (b) must be dropped. What they can still settle:

1. Dot placement: whether each `^.` sits over the digit before or after the mark, and whether any dots were missed
   (202 dotted digits in the transcript; the Meister key-1 mechanic hangs on which digit carries the dot).
2. The 13 uncertain readings and any digit-shape confusions (1/7, 0/6, 5/9) in the transcript.
3. Whether IA-1 (record 91) uses the same key family: double the ciphertext in one chancery hand, and if the
   DECODE transcription of IA-1 marks tokens, its tokenisation is a model for IA-2.
4. Whether s6key.txt (1570) is a design relative of the 1542 key.
5. The 069v cleartext frame: sender, date, addressee, to fix the crib vocabulary.

The statistical separator already found here (digit 4 as null / word end, NOTES.md "Established facts") is
consistent with Lasry's statement: the separator is a cipher element, not a visual one.
