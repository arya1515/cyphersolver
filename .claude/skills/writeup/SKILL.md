---
name: writeup
description: Write up a finished cipher target on the site and in every ledger, in this repository's convention. Use when a target is read, solved, explained or closed, when the Stop hook or `docs/_check_writeup.py` reports a finished target with no write-up, or when the user says "write it up". Argument is the target's folder name, e.g. /writeup gramont1529.
argument-hint: <folder or slug>
---

# Write up a finished target

A result is not finished until it is on every one of these surfaces. Concurrent sessions in this repo commit each
other's folders with `git add -A`, so the commit log never announces a solve; the only reliable signal is the
checker. Work through the list, then run `python docs/_check_writeup.py <slug>` until it prints `complete`.

Target: `$ARGUMENTS`. Read `<folder>/NOTES.md` and the reading files first; the write-up is written from the notes,
not from memory. The slug is the folder name unless a page already exists under another name (check
`python docs/_check_writeup.py --audit` and the README row's link). Never invent a second page for the same target.

## 0. Before writing

- `git status -sb`: know which branch the shared checkout is on. Other sessions switch it. If it is not `main`,
  work in your own worktree: `git worktree add <scratchpad>/wt-main -b writeup-<slug> origin/main`, do everything
  there, push `HEAD:main`, then `git worktree remove`. Never `git commit --amend` during a rebase.
- `git fetch origin` and read `origin/main:docs/_build_site.py`, not the branch copy, if they differ: main's is newer.
- Read one recent page for tone and structure: `docs/gramont1529.html` (solved), `docs/lorraine1592.html`
  (partly read), `docs/orpo1942.html` (attempted, not solved).
- Decide the outcome class. `st` in the manifest is one of `solved` (read end to end or nearly), `partial`
  (partly read), `found` (explained, or found already solved by others), `stuck` (attempted, not solved). The README
  section, solved.html and SOLVED_* rows follow from it.
- Dates: "Date" is the document's date. The work date is the day the finding first landed in the repository
  (`git log --diff-filter=A --format=%ad --date=short -- <folder>/ | tail -1` if it was not today).

## 1. The page: `docs/<slug>.html`

Copy the skeleton of a recent page. The builder regenerates nav, footer, contents strip, lead figure, byline date
and version stamps; you write everything else. Required parts, in order:

1. `<head>`: `<title>Short name (dates) — Read / Read in part / Not a cipher / Attempted</title>`, a one-paragraph
   `<meta name="description">`, `<link rel="stylesheet" href="style.css">`.
2. `<!-- site:nav -->` on its own line right after `<body>`.
3. `<section class="hero">`: optional `<div class="cipherstrip">` (a line of the cipher, a line of its reading,
   a few key equivalences); `<p class="kicker">place → recipient · cipher type · dates · outcome</p>`; `<h1>`;
   one or two `<p class="sub">` with shelfmark, what it is, what was done; `<p class="meta">Daniel Bourdeau</p>`
   (the builder adds the dates; a contributor's credit goes in the callout, not the byline).
4. `<main>` opening with `<div class="callout"><strong>Summary.</strong> …</div>`: what was catalogued, what was
   found, how, what stays open. Five to ten sentences.
5. Numbered `<h2><span class="num">01</span> …</h2>` sections: the documents and keys; the reading (one section
   per letter, with the text in the original language and, where useful, a translation); method; what remains
   uncertain (list every unread group and the grade of every doubtful reading, H/C/M/I as in README Conventions);
   Sources (archive links with view numbers, editions, prior keys with their authors).
6. Figures: `<figure><img src="<slug>_<what>.jpg" alt="…" loading="lazy"><figcaption>…</figcaption></figure>`, cut
   from the scans at the width of the text column (about 1100 px), JPEG, under 400 KB each, named `<slug>_…`.
   Page images themselves are never committed; crops for the site are.
7. Close with `<p class="muted">` pointing to the repository folder, then `<!-- site:footer -->`.

Write the HTML with the Write tool, not a Bash heredoc (long payloads fail to parse). HTML entities for accents
in attribute and manifest strings (`&eacute;`, `&rsquo;`, `&mdash;`), plain UTF-8 in the body is fine.

## 2. The manifest: `docs/_build_site.py`

- Add a `dict(slug=…, label=…, year=…, y=…, place=…, st=…, stt=…, title=…, blurb=…, quote=…, rights=…)` to
  `PAGES`, in chronological position. `y` is the sort year (float for a range), `stt` the badge text
  (`read`, `read in part`, `not a cipher`, `already in print`, `double pass not broken`…), `blurb` three or four
  sentences, `quote` one line from the reading, `rights` the archive's credit line.
- Add the slug to `IMAGES`: `('<slug>_lead.jpg', 'caption', 'credit')`, or `None`. Every page needs the key.
- If the page is solved or partly read, update the `solved` survey entry's blurb and quote counts.

## 3. The ledgers in the repository root

- `README.md`: one row in the matching `## Results` table (Solved / Explained / Partly read or adjudicated /
  Found already solved by others / Attempted and closed). Five columns: Target (name, place, dates, shelfmark,
  catalogue item and class), Date (of the document), work date, Result (bold outcome, then what was read and
  what is open), Where: `` [`<folder>/`](<folder>/) · [write-up](https://dbourdeau.github.io/cyphersolver/<slug>.html) ``.
  The Where link is what marks the row as written up; without it the row lists as "notes only".
- `SOLVED_CATALOGUE.md` (solved and partly read only): next number, same columns as the rows above it.
- `SOLVED_RANKING.md` (solved and partly read only): a `pN` provisional row with the six axis scores and the
  weighted score, and the sentence in the preamble that places it; add the score line at the foot.
- `TARGETS.md`: if the target was in the open list, move it to "Done elsewhere in this repo" with the status text.
- `catalogue.json` (catalogue items only): the catalogue holds open targets only, so **take the entry out**.
  If the target was read, partly read, resolved or found already in print, delete its entry (ids are never
  reused) and add its id to the list in `CATALOGUE.md` under "Read or resolved here, and removed". If the entry
  covers several items and only some were read, narrow it to the unread ones (title, date, shelfmark, status)
  and set `"outcome": "attempted, open"`; a target attempted and closed unread keeps its entry with the same
  outcome. Before deleting, make sure the README row or `SOLVED_CATALOGUE.md` carries everything the entry's
  status said. Also look for the target under another name: DECODE entries carry `decode_ids`, so match the
  record numbers (`R1234`) in the folder's NOTES against them. Dump with `indent=1, ensure_ascii=False` and a
  trailing newline.
- `docs/index.html`: a new `<li>` at the top of the first `<ul class="findings">` under Recent findings:
  `<li><b>Who to whom, date</b> &mdash; <span class="fnd">outcome in one line</span> … <a href="<slug>.html">write-up</a></li>`.
  The builder dates it and folds the list.
- `unpublished/solved.html` (solved and partly read only; optional while the page is unpublished): a `<tr>` in the right table, then recount the sentences in
  "The short version" (items, read in full, in long stretches, to a solver, to a sibling or key).

## 4. Build, check, commit

From `docs/`, with UTF-8 forced (the stats builder crashes on the cp1252 console otherwise):

```
cd docs
PYTHONUTF8=1 python _catalogue_page.py     # only if catalogue.json changed
PYTHONUTF8=1 python _build_stats.py
PYTHONUTF8=1 python _build_site.py
cd ..
python docs/_check_writeup.py <slug>
```

The builder prints `note: <slug>.html has no README row`, `note: README links <slug>.html, which is not in the
manifest` and `note: <slug>.html has no hero section` when the surfaces drift; fix and rebuild. The checker must
end with `result: complete` (warn lines are allowed, MISS lines are not). Then check `git diff HEAD -- CATALOGUE.md`
shows only the intended rows.

Stage by explicit path: the new page and its images, `_build_site.py`, `_dates.json`, every regenerated
`docs/*.html`, the ledgers touched. Never `git add -A`: the shared tree carries other sessions' work. Commit subject
`Site: write-up for <who to whom>, <dates> (<shelfmark>)`, body listing what each surface got, as in `git log
--grep='^Site:'`. Push to `main` (`git push origin HEAD:main` from a worktree) and confirm
`https://dbourdeau.github.io/cyphersolver/<slug>.html` after the Pages build.

## 5. If the target is not actually finished

Put `Status: in progress` (or `Status: no write-up`, with the reason) in the first forty lines of the folder's
`NOTES.md`. The audit and the Stop hook read that line and stop asking.
