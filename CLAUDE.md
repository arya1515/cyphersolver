# cyphersolver

Historical cipher targets, one folder per target with a `NOTES.md`, and a GitHub Pages site in `docs/`.
The layout, the build scripts and the reading conventions are in `README.md` (Repository layout, The website,
Conventions). Read them before touching `docs/`.

## Shared assets

Language models live in `lang/` (`lang/README.md`): a corpus registry, a model registry and one n-gram engine, e.g.
`from lang import lm; lm.load('fr-1600-letters')`. Use one of its models, or add a corpus/model there, rather than
writing a new `<target>/lm.py`. `lm.best_language(text)` is a quick language check on a decrypt.

## A target is finished only when it is written up

Finishing a cipher (read, read in part, explained, found already solved, or attempted and closed from the
evidence) is the first half of the job. The second half is the write-up, and it is done in the same session:

1. Run the `/writeup <folder>` skill (`.claude/skills/writeup/SKILL.md`). It lists every surface a result must
   reach: the `docs/<slug>.html` page, the `PAGES` and `IMAGES` manifest in `docs/_build_site.py`, the README
   results row with its write-up link, the Recent findings line on `docs/index.html`, the `unpublished/solved.html` row (optional while unpublished),
   `SOLVED_CATALOGUE.md`, `SOLVED_RANKING.md`, `TARGETS.md`, `catalogue.json`, and the rebuild.
2. `python docs/_check_writeup.py <slug>` must print `result: complete` before the work is reported as done.
3. `python docs/_check_writeup.py --audit` lists finished targets that never got a write-up. The SessionStart hook
   shows it at the start of each session; the Stop hook blocks a stop once when a target this session worked on
   reads as finished in its NOTES but has no README row and no page.

If a target is genuinely not finished, or deliberately not written up (found solved by others with nothing added
here), put `Status: in progress` or `Status: no write-up` in the first forty lines of its `NOTES.md`.

## Working in the shared checkout

- Several sessions share this working tree and switch its branch. Run `git status -sb` before committing; if the
  branch is not the one you mean, commit from your own worktree and push `HEAD:main`.
- Stage by explicit path, never `git add -A`.
- Build from `docs/` with `PYTHONUTF8=1` set; `_build_stats.py` crashes on the cp1252 console without it.
- Write long HTML with the Write tool, not a Bash heredoc.
