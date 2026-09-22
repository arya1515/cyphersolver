# Unknown sender ("Yorke") to General Goring, 5 June 1645 — TNA SP 106/10 ff. 251–252 — NOTES

Status: no write-up

**Verdict: already READ, by George Lasry (DECODE R932, key "TNA SP106-3" and plaintext uploaded 2020-10-23).**
Catalogue entry 61 is resolved; nothing about the text is added here. Session 2026-09-21.

## What DECODE holds

The record page links four text files (fetched with the shared cookie into `decode/`, git-ignored as DECODE's and
Lasry's work):

- D2358: manual ciphertext transcription by "FL", 3 Jan 2020 (two strips, images 4929 and 4930);
- D3077: Lasry's plaintext, with the note that "caracter" means cipher key and that 60–79 look like nulls/space;
- D3078: the plaintext interlined under the ciphertext; D3079: the reconstructed key. It is a plain homophonic
  alphabet, 1–2 digit values with 1–4 homophones (E = 52|55|56, H = 35|36|37, P = 9|10|11|12), 60–79 nulls,
  and one code group, 106 = GENERAL. 104 (before the signature) and 46 are unresolved.

The text starts on image 4930 and ends on 4929; DECODE's image order is reversed. Lasry's reading:

> Sr I pray you present my humblest service to [his Highness?] [and] excuse me for not writing to his Highnes because
> I doubt whether hee can decipher my caracter. Noane inform him wee are strongly beseidged on all sides; if his
> Highnes doe not give us releif shortly wee shall perish. I am confident of his Highnes care of us. Desire to heare
> when hee can bee here certainely. So I am yor servant <104> Yorke June fifth. For General Goring.

## Check done here

`check.py` applies the D3079 key to FL's raw transcription (D2358), independently of Lasry's plaintext. It reads
the same English throughout. The only misses are tokens that the transcription's spacing and `^` insertion marks run
together (`424` = 4·24 "RS", `243` = 24·3 "SR", `449` = 4·49 "RK"). `ciphertext.txt`: 338 groups, 64 distinct
(`_check_profile.py --measure`).

## Open points (not pursued)

- DECODE's origin "York" comes from the signature line. York had been in Parliament's hands since July 1644, so
  "Yorke" may be the writer's name, or the <104> group may hide it. "His Highnes" is presumably the Prince of Wales
  (in the West with Goring's army in June 1645) or Rupert. The besieged garrison is not identified.
- Codes 104 and 46, and the exact role of the 60–79 groups, remain as Lasry left them.
