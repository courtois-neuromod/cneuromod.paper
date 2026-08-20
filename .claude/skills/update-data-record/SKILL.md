---
name: update-data-record
description: This skill should be used when a co-author wants to initialize or update paper/data_record.md by cross-referencing the canonical repository, BIDS, and derivatives documentation in the cneuromod.all submodule. It reads the current paper section and the relevant source docs, identifies new content or corrections, and proposes a revised paper section in the appropriate academic writing style with proper citations. Use it when someone mentions "update data record", "repository structure", "BIDS compliance", "submodule structure", or "preprocessing derivatives format".
---

# Update Data Record

## Purpose

To keep `paper/data_record.md` accurate and up-to-date by comparing it against the canonical documentation in the `cneuromod.all` submodule, then proposing targeted revisions that match the paper's style and citation conventions.

## Scope: this is NOT the dataset-by-dataset section

`paper/data_overview.md` already documents every dataset individually — report cards, subject
coverage, tasks, per-dataset citations. `paper/data_record.md` must not duplicate that. It covers
how the data is *organized and formatted*, not what each dataset contains:

- DataLad/git repository structure and submodule naming conventions
- BIDS compliance and deviations from the core specification
- Preprocessing derivatives: what each pipeline (fMRIPrep, sMRIPrep/FreeSurfer, PhysPrep) outputs
  and how those outputs are named/organized
- Data access and versioning mechanics (release tags, registered-access vs. open subjects)

Where a concrete example of submodule layout is useful, illustrate it with one or two datasets
(e.g. `friends/bids`, `friends/fmriprep`, `friends/mriqc`, `friends/physprep`) rather than
enumerating every dataset — that enumeration belongs in `data_overview.md`. If a full "Functional
datasets" style section listing all datasets is found in `data_record.md`, flag it for removal
(or collapse it into a single illustrative example) rather than updating it in place.

## Workflow

### 1. Read the current paper section

Read `paper/data_record.md` in full. Note any per-dataset description list that overlaps with
`paper/data_overview.md` — this is a removal candidate, not something to keep in sync.

### 2. Read the source documentation

Read the canonical source documentation:

```
source_data/cneuromod.all/docs/source/contents/downloading.md
source_data/cneuromod.all/docs/source/contents/bids.md
source_data/cneuromod.all/docs/source/contents/fmriprep.md
source_data/cneuromod.all/docs/source/contents/smriprep.md
source_data/cneuromod.all/docs/source/contents/physprep.md
source_data/cneuromod.all/docs/source/contents/access.md
```

`downloading.md` is the authoritative source for repository/submodule structure and DataLad
mechanics. `bids.md` covers BIDS compliance and deviations. `fmriprep.md`, `smriprep.md`, and
`physprep.md` describe derivative pipeline outputs and file naming. `access.md` covers the
open-vs-registered-access split and ethics approval, relevant to the versioning/access
subsection. These files are written for a technical documentation site and are more verbose
than the paper section — extract corrections and additions, don't copy verbatim.

### 3. Read the available references

Scan both bibliography files for citable entries relevant to the pipelines described in this
section (e.g. fMRIPrep, PhysPrep, Nipype):

```
source_data/cneuromod.all/docs/source/cneuromod_references.bib
references.bib
```

### 4. Identify discrepancies and gaps

Compare the two documents across each subsection:
- **Repository structure** — submodule count, naming conventions, YODA principles, recursive-install warning
- **BIDS compliance** — deviations (BEP001, BEP025/`bp-cspine`), session-index caveats
- **Preprocessing derivatives** — fMRIPrep version/flags, output spaces, file suffixes; sMRIPrep/FreeSurfer modes; PhysPrep output file suffixes and processed modalities
- **Data access and versioning** — open vs. registered-access subject counts, release-tag mechanism

For each subsection note:
- Details present in the source docs but absent or outdated in `data_record.md`
- Content in `data_record.md` that duplicates `data_overview.md` and should be cut
- Details too technical/verbose for the paper (omit or simplify)

### 5. Propose a revised paper section

Write out the full revised `paper/data_record.md`. Style rules:
- Match the existing paper prose style: concise, factual
- Do not add or retain a per-dataset description list — one or two illustrative submodule
  examples (e.g. `friends`) are enough to show the naming pattern
- Use MyST citation syntax: `{cite:p}\`key\``
- Only cite keys that exist in one of the two `.bib` files above; do not invent citation keys
- If a needed reference is missing from both `.bib` files, flag it explicitly with a
  `[MISSING REF: description]` placeholder
- Keep section headers and structure identical to the current file unless a new subsection is
  clearly warranted

### 6. Present changes to the user

Before writing to disk, present a summary of what changed and why. List:
- Corrections (parameter or structural values that were wrong)
- Additions (content present in source docs but missing from paper)
- Removals (duplicated per-dataset content cut in favor of `data_overview.md`)
- Missing citations that need to be added to `references.bib`

Ask the user to confirm before applying the changes.
