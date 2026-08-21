---
name: update-acknowledgements
description: This skill should be used when a co-author wants to initialize or update paper/acknowledgements.md by cross-referencing contributor and funding documentation in the cneuromod.all submodule. It runs a script that unions every dataset's contributors.json into a per-person CRediT contribution scaffold and an ordered author list, then reads AUTHORS.md, HOWTOCITE.rst, and access.md to draft the Acknowledgements, Author Contributions, Funding, and Competing Interests subsections. Use it when someone mentions "update acknowledgements", "author contributions", "contributor list", "funding", "CRediT", or "competing interests".
---

# Update Acknowledgements

## Purpose

To keep `paper/acknowledgements.md` accurate by deriving the author list and Author
Contributions from data rather than writing them by hand. Every dataset repository in
`source_data/cneuromod.all/` carries an all-contributors `contributors.json` naming who
contributed and in what capacity. Taking the union across datasets yields, per person, a set
of CRediT roles and the datasets they touched — the material for the author list and the
CRediT statement. Funding, Acknowledgements prose, and Competing Interests come from the
submodule's narrative docs and are added by hand.

## Scope

This section covers who did what and who paid. It does not cover:
- License and access mechanics — `paper/data_availability.md`
- Software repository details — `paper/code_availability.md`
- Ethics review, beyond a one-line participant acknowledgement — `paper/data_availability.md`
  owns the substantive access/ethics discussion; here it's just a thank-you.

## Workflow

### 1. Read the current paper section

Read `paper/acknowledgements.md` and the `## Authors` section of `paper/index.md` in full. If
co-authors have already refined prose here — especially manually-added writing contributions
under Author Contributions — preserve it rather than clobbering it with regenerated scaffold.

### 2. Regenerate the contributor scaffold

Run the bundled script from the repository root:

```bash
uv run python .claude/skills/update-acknowledgements/scripts/build_contributors.py \
  > /tmp/acknowledgements_scaffold.md
```

It unions `source_data/cneuromod.all/*/contributors.json` across datasets, resolves each raw
`login`/`name` key through the curated
`.claude/skills/update-acknowledgements/scripts/contributors_aliases.yaml`, maps
all-contributors roles to CRediT, and prints:
- the ordered author list (core team starred, consortium alphabetical by family name, Bellec
  last),
- one Author Contributions line per person,
- a raw audit table (person x raw contributions x datasets) for spot-checking.

Datasets missing a `contributors.json` are printed to stderr as an **upstream gap** — flag
these in the summary in step 7 rather than papering over them.

Any raw key not yet in the alias map is printed as `[UNMAPPED: <key>]` in the output and
listed on stderr. **Resolve every `[UNMAPPED: …]` by extending `contributors_aliases.yaml`
before drafting** — never guess an identity or drop a contributor silently. The alias map
records two GitHub logins (`RainyFields`, `cyrand`) with no matching name anywhere in the
docs; leave them as distinct, flagged entries rather than merging them into a guessed
identity.

The scaffold is **input, not output**. Never paste it wholesale into the paper.

`--repo PATH` points at a different `cneuromod.all` checkout if needed.

### 3. Read the source documentation

```
source_data/cneuromod.all/docs/source/HOWTOCITE.rst      # required acknowledgement paragraph
source_data/cneuromod.all/docs/source/AUTHORS.md         # funding, team roster, alumni, affiliations
source_data/cneuromod.all/docs/source/OVERVIEW.rst       # consortium framing
source_data/cneuromod.all/docs/source/contents/access.md # ethics / consent (Ethics section)
```

`HOWTOCITE.rst` carries the acknowledgement paragraph the team asks every publication to
reproduce verbatim. `AUTHORS.md` supplies the Funding paragraph, team roster, and
affiliations for most contributors — but the fixed core team defined below deliberately
overrides its Core section (it lists Arnaud Boré as data manager and Marie St-Laurent under
Vision). `access.md`'s `## Ethics` section supports one line about participant consent and
ethics approval (CER-VN, project number CER VN 18-19-22, renewed 2022-10-21).

### 4. Draft each subsection

- **Acknowledgements** — reproduce the Courtois paragraph from `HOWTOCITE.rst` faithfully;
  thank participants; note UNF/CRIUGM infrastructure; list alumni and non-author
  contributors from `AUTHORS.md`'s Alumni section and the scaffold's institution entries
  (e.g. Courtois Foundation).
- **Author Contributions** — from the scaffold, in CRediT terms, plus a marked
  `[TODO: writing contributions]` block for the manual additions (Formal analysis and
  Resources have no all-contributors equivalent either — flag them the same way).
- **Funding** — 6.3M CAD (2018–23, PI Bellec) Courtois Foundation donation, administered by
  FIGM / CIUSSS du Centre-Sud-de-l'île-de-Montréal and Université de Montréal; CIMAQ and
  PRISME consortia. Flag any grant number not present in the source docs as
  `[MISSING: grant number]` — do not invent one.
- **Competing Interests** — default to "The authors declare no competing interests.",
  explicitly flagged for the user to confirm.

### 5. Propose the ordered author list for `paper/index.md`

`myst.yml`'s `project.authors` renders on *every* page of the book (header/footer chrome) —
never put the full author list there. Keep it fixed at:

```yaml
authors:
  - name: The CNeuroMod team
```

The full, ordered author list belongs only on the landing page, `paper/index.md`, under an
`## Authors` heading: one paragraph or list, name plus affiliation in parentheses, `*` marker
for the three shared co-first authors and a note below the list explaining the marker, `†`
(or "corresponding author" in prose) for Bellec. Present this list as a separate, explicitly
confirmable change before writing it — do not edit `paper/index.md` or `myst.yml` without the
user agreeing to it.

**Core team** (fixed, user-specified — overrides `AUTHORS.md`): Julie Boyle (project
manager), Basile Pinsard (data manager), Marie St-Laurent (data scientist), Lune Bellec
(scientific director). Author order: core minus Bellec, each marked `*` for shared
co-first authorship (Boyle, Pinsard, St-Laurent) → consortium alphabetically by family
name → Lune Bellec last as senior/corresponding author.

### 6. Style rules

Concise, factual prose. MyST citation syntax `{cite:p}\`key\`` for any citation, using only
keys present in `references.bib` or `cneuromod_references.bib`; flag anything else as
`[MISSING REF: description]`. Keep the four existing section headers unchanged.

### 7. Present changes to the user

Before writing to disk, summarize:
- People added or renamed relative to the current file
- Any `[UNMAPPED: …]` keys resolved (and how) while extending the alias map
- Datasets still missing `contributors.json` upstream
- Items still needing user input: writing contributions, missing affiliations
  (`[MISSING: affiliation]`), missing grant numbers, competing-interests confirmation, and
  the `cyrand`/`RainyFields` identity gaps
