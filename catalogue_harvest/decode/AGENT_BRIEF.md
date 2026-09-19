# Brief: turn DECODE records into scored catalogue entries

You are helping refill the **catalogue of unsolved historical ciphers** in the repository at
`C:\Users\dbour\cypher` (site: dbourdeau.github.io/cyphersolver). The catalogue lists cipher letters that are not
yet read, each scored so the owner (Daniel) can pick what to attack next. You are given one batch of candidate
groups harvested from the DECODE database (de-crypt.org): ciphertext records marked *Non-decrypted* or *Partially
decrypted*, grouped by archive series, sender, receiver and half-century. None of them is referenced anywhere in
the repo yet.

Do **not** edit any file in the repository except your own output file. Do not commit. Do not download images.

## Input

`C:\Users\dbour\cypher\catalogue_harvest\decode\batch_<N>.json`: a list of groups. Each group has `key`
[city, series shelfmark, author, receiver, half-century], `ids` (DECODE record numbers), `records` (DECODE
metadata per record: holder/shelfmark, date, author, receiver, origin, cleartext and plaintext language, pages,
status, cipher types, symbol sets, access = public/login, `info` = DECODE's free-text field, which often carries
bibliographic references and archive comments), and `decode_keys` (key records on DECODE from the same archive
series within ±40 years; `decode_keys_total` counts them). A matching key is the single biggest factor in
solvability, but a key from the same series is not necessarily the key of this letter.

Useful references in the repo (read only what you need):
- `C:\Users\dbour\cypher\catalogue.json` — the existing 33 entries: the schema and the tone to match.
- `C:\Users\dbour\cypher\CATALOGUE.md` — the scoring text.
- `C:\Users\dbour\cypher\TARGETS.md` — targets already tracked; don't duplicate.
- `C:\Users\dbour\cypher\unsolved.htm` — a local copy of Tomokiyo's Unsolved Historical Ciphers list. If an item is
  on it, keep it but say so in `status` and set `"on_list": "Tomokiyo"`.
- A DECODE record's public page, `https://de-crypt.org/decrypt-web/RecordsView/<id>`, can be fetched without login
  and shows the same metadata. You rarely need it.

## What to produce

For each group, decide one of three things:

1. **Entry** — a coherent target: one letter, or a series that would be attacked together (same sender, same
   key, same few years). **Merge** groups in your batch that belong together, e.g. the same ambassador writing to
   two different recipients in the same years, or records split across decades. Split a group only if it clearly
   mixes unrelated things. Aim for entries a person could pick up as one job.
2. **Also noted** — a real cipher document with too little to go on (no author, no date, no context), or a very
   minor item. Emit it as an entry with `"counted": false`. Several of these can be merged into one "miscellany"
   entry per archive series.
3. **Exclude** — already read in print or online (you found the edition or solution), not actually a ciphertext
   (a key, a register, a cover sheet), a duplicate of an existing repo target, or a test/empty record. Emit an
   exclude line with the reason, so the owner can see it.

### Prior-solution check (important)

This repo has been burned twice by publishing "unsolved" items that had been solved: Perwich 1670, and ACA
Reserva 12, which DECODE marks Non-decrypted while its own References field cites Salas 1931, who printed the
full reading. So:
- Read each record's `info` field. If it cites an edition or an article that reads the text, the item is probably
  solved: exclude it or, if the reading is partial, say so in `status`.
- For every entry you score **importance ≥ 3**, run a web search (WebSearch) for a decipherment or edition, e.g.
  "<sender> <year> cipher deciphered", "<sender> <receiver> <year> letter edition", Calendar of State Papers,
  Nunziature editions, CODOIN, Lasry or Tomokiyo on cryptiana.web.fc2.com. Keep it proportionate: one or two
  searches per entry, about 30 in total for the batch. Record what you checked in `status`, e.g. "Web search
  (CSP Foreign 1562, Tomokiyo) found no decipherment."
- Know the traps. **BL Add MS 32253–32310** is the Deciphering Branch collection, and **TNA SP 106** holds ciphers
  and keys: 18th-century intercepts there were usually deciphered at the time, so DECODE's "Non-decrypted" often
  means only that no decipherment was uploaded. English State Papers ciphers of the 16th–17th centuries were often
  deciphered in the margin or printed in the Calendars. **Vatican Segreteria di Stato nunziature** usually have
  the deciphered copy ("decifrato") filed with the cipher. Such items are class A candidates with a warning, not
  open mysteries. Say this in `status` and `verify`.

## Entry schema (one JSON object per line)

```json
{"type": "entry",
 "decode_ids": [1234, 1235],
 "counted": true,
 "year": 1562,
 "date": "30 Oct 1562",
 "title": "Throckmorton (Paris) to Cecil",
 "correspondents": "Sir Nicholas Throckmorton, English ambassador in France → Sir William Cecil",
 "place": "Paris → London",
 "language": "English",
 "region": "England",
 "period": "1560-1589",
 "shelfmark": "BL Add MS 4136 ff. 135-136",
 "folio_note": "",
 "cls": "B",
 "status": "DECODE R1234 (Non-decrypted, 2 pp., numerical nomenclator, login). ... prior art found or not ...",
 "why": "One sentence on what a reading could add, grounded in the date and people. No invented facts.",
 "importance": 3, "solvability": 3, "difficulty": 3,
 "score_note": "One or two sentences justifying the three scores.",
 "verify": "The concrete check to make before attacking it.",
 "on_list": ""}
```

Exclusions: `{"type": "exclude", "decode_ids": [...], "reason": "..."}`

Field rules:
- `date`: "13 Jul 1572", "Jan–Jul 1586", "1520s", "c. 1590". `year`: an integer (first year); null if unknown.
- `title`: English, short: "Sender (place) to Receiver"; for a series "…, five letters".
- `correspondents` uses →. `language`: the plaintext language if known, else the cleartext language + "?".
- `region`: one of England, France, Germany, Italy, Papacy, Spain, Portugal, Low Countries, Poland, Hungary,
  Bohemia, Austria, Scandinavia, Ottoman, Russia, Savoy, Lorraine, Switzerland, Americas, Other — the political
  sphere of the sender.
- `period`: one of "before 1497", "1497-1559", "1560-1589", "1589-1598", "1598-1610", "1611-1650", "1651-1700",
  "1701-1800", "1801-1900", "unknown".
- `shelfmark`: the archive's own reference, shortened (BL, TNA, BnF, AGS, ASV = Vatican archive, BAV, RAH, ASMo…).
- `status` starts with the DECODE record(s), status, page count, cipher type and symbols, and access, then prior
  art. At most ~600 characters. Nothing here has been viewed on the image, so never describe the leaf's content
  as if seen.
- Plain, factual English. No hype. En dashes for ranges.

## Scores (1–5, judgements from metadata and the literature)

- **importance** — what a full reading would add to the historical record. 5: a principal's first-hand report of
  a major event (a viceroy during the Siege of Malta; an ambassador at a royal election). 4: a senior envoy's
  despatch at a known turning point. 3: ordinary high diplomacy. 2: routine business or a minor agent. 1: nothing
  identifiable.
- **solvability** — odds of a full reading with material online. 5: the decipherment or the key is available (a
  matching key record, a deciphered duplicate). 4: a key or a deciphered sibling from the same series and years is
  on DECODE. 3: a known family or partial key in print, or a long text in a known language. 2: moderate text, no
  key. 1: very short, or unknown language or system.
- **difficulty** — the technical work at the keyboard. 1: align a known key or sibling. 2: a small homophonic
  cipher with a crib. 3: a mid-size nomenclator with siblings. 4: a large nomenclator or code, or a hard script. 5:
  statistics only, on a large or unusual system.
- **cls** — A: a decipherment or a key for the same series is on DECODE or filed with the letter. B: a partial key,
  a related key or a known family in print. C: no key, no sibling.

Calibration from the existing catalogue: Toledo to Philip II during the Siege of Malta, 1565: 5 / 5 / 2 (it fell
in a day). Mondoucet to Charles IX, 1572, with glossed siblings: 4 / 3 / 4, class A. Catherine de Médicis to the
bishop of Rennes, 1563, with sibling keys by Tomokiyo: 3 / 4 / 2, class B. Be honest and spread the scores: most
single letters with no key should come out around 2–3 importance, 2 solvability, 4 difficulty. Reserve 5s.

## Output

Append each line to `C:\Users\dbour\cypher\catalogue_harvest\decode\out_<N>.jsonl` **as soon as it is decided**
(use Bash with a heredoc `cat >> file <<'EOF'`, or Python, UTF-8). Don't hold everything until the end: if you are
cut off, what's written survives. Every DECODE id in your batch must appear in exactly one line (entry or exclude).
Before finishing, check that with a short Python script and fix any gaps or duplicates.

Finish with a short report (under 200 words): counts of entries, also-noted and excluded; the five highest-scoring
entries in one line each; anything surprising, e.g. an item you found already solved.
