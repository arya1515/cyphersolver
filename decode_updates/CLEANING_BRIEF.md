# Brief: clean decryption files for DECODE

Each record in `decode_updates/queue.json` gets a decryption file uploaded to its public DECODE record. The builder
(`decode_updates/build.py`) adds the header; you write the body, one file per record:
`decode_updates/decryptions/R<id>.txt` (UTF-8, LF, no BOM). Work from the repository root
`C:\Users\dbour\cypher\.worktrees\decode-updates`. Read the target's `NOTES.md` first, then the source files listed
for your records.

## What the body is

Only the decoded text of that record, in the original language, as the letter runs. It is what a historian opening
the DECODE record wants: the letter, readable, with gaps marked honestly. Not our working notes.

Keep:
- the deciphered text, in reading order, divided by page or folio: a line `[p. 1]`, `[f. 95r]` or the image name
  (`[IMG 4843]`) before each page, as the source allows;
- passages written in clear on the document when the source has them, as `[clear: ...]`, in their place;
- line breaks at sense or at the source's line breaks, no longer than about 110 characters.

Leave out: headings, markdown (`#`, `**`, `>`, tables, backticks), English commentary, translations, summaries,
confidence discussion, key tables, token dumps, statistics, file names, "we"/"here" remarks.

## Conventions (the header states them; use exactly these)

- `<nnn>` a code group (number or sign) not read. Convert the source's own marks for an unread group to this.
- `[...]` illegible or not read (a stretch, or letters); `[?]` a single unreadable sign.
- `{word}` a value inferred from context, not from the key (a gloss, an unresolved code guessed from sense).
- `word?` an uncertain reading.
- Contemporary interlinear or marginal decipherments are not ours: if the source gives both, give our reading and
  do not append the clerk's text, unless our file only has the clerk's text for a passage, then
  `[contemporary decipherment: ...]`.

## Rules

1. Do not invent or improve readings. Every word must be in the source files. You may: split run-on letter
   streams into words (Italian, Spanish, French...), restore word division, drop nulls the source already marks
   as nulls, normalise the gap marks to the conventions, and join pages. You may not change letters, expand
   abbreviations the source does not expand, or fill gaps from sense (unless the source already gives that
   gloss, then `{...}`).
2. Word-splitting a machine stream: where you cannot split with confidence, leave the run joined and add `?`.
   Keep the source's bracketed nomenclator words (e.g. `[NOSTRO SIGNORE]`) as plain words in lower case
   (`nostro signore`); codes with no value become `<nn>`.
3. Where the source has two readings of the same passage (passes, versions), use the latest/final one named in
   NOTES.md.
4. Duplicate records (the queue note says "Duplicate of Rxxxx") get a copy of that record's body with a first
   line `[Duplicate copy of Rxxxx; the text below is the reading of Rxxxx.]`.
5. If a record's source holds nothing you can turn into a letter text (only analysis), write the file with the
   best stretch of decoded text the source does contain and report it; do not leave the record out.
6. Do not edit anything outside `decode_updates/decryptions/`. Do not commit. Do not touch other records.

## Report back

One line per record: `R<id>: done | done, thin (why) | problem (what)`, plus anything a human should check.
