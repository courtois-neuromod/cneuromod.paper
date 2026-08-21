---
name: update-data-overview
description: This skill should be used when a co-author wants to initialize or update paper/data_overview.md by cross-referencing the canonical dataset and asset documentation in the cneuromod.all submodule. It runs a script that reads every dataset_info.yaml, README and CITATION.cff to regenerate the summary statistics, the per-dataset coverage subsections (condensed overview, reference) and the asset coverage table, then condenses the result into the paper's academic style. Use it when someone mentions "update data overview", "summary statistics", "dataset coverage", "asset coverage", or "hours per subject".
---

# Update Data Overview

## Purpose

To keep `paper/data_overview.md` accurate and up-to-date by regenerating it from the canonical
dataset statistics and asset documentation in the `cneuromod.all` submodule, then condensing the
generated scaffold into paper prose. This section is the quantitative inventory of the database:
how much data, from which paradigms, in which processed forms.

The section has three parts, in this order:

1. **Summary Statistics** — the CNeuroMod bubble-chart figure plus aggregate totals and coverage gaps.
2. **Dataset Coverage** — one subsection per dataset: condensed overview, reference.
3. **Asset Coverage** — the asset/datasets recap table plus a text description of each asset.

## Workflow

### 1. Read the current paper section

Read `paper/data_overview.md` in full, so that prose already refined by co-authors is preserved
rather than overwritten by regenerated scaffold.

### 2. Regenerate the scaffold

Run the bundled script from the repository root:

```bash
uv run python .claude/skills/update-data-overview/scripts/build_overview.py \
  > /tmp/data_overview_scaffold.md
```

It draws on two submodules, each for what it owns:

- `source_data/cneuromod.all` for narrative — it imports the submodule's own Sphinx extension
  (`docs/source/_ext/renderers.py`), so citation blocks are exactly what the documentation
  website renders.
- `source_data/dataset_comparison/output_data/*.csv` for every aggregate number, read through
  `paper/_stats.py`. No aggregation happens in the paper or in this script.

If the two checkouts of `cneuromod.all` sit at different commits, the script prints a warning to
stderr. Resolve that before writing the section — otherwise the prose and the numbers describe
different sets of datasets.

The scaffold is **input, not output**. Never paste it wholesale into the paper.

`--repo PATH` points at a different `cneuromod.all` checkout if needed.

### 2b. Never hardcode a number

Datasets are still being collected and released. Every count, hour total or subject tally must be
quoted through an inline expression so it refreshes on each build:

```markdown
```{code-cell} python3
:tags: [remove-cell]
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in (Path("paper"), Path(".")) if (p / "_stats.py").exists())))
from _stats import STATS
```

The database comprises {eval}`STATS.n_datasets` datasets acquired in
{eval}`STATS.n_subjects` participants, totalling {eval}`STATS.fmri_total_h` hours of fMRI.
```

`STATS` exposes `n_datasets`, `names`, `n_subjects`, `subjects`, `fmri_total_h`,
`fmri_per_subject_h`, `physiology_h()`, `total_h(modality)`, `per_subject_h(modality)`,
`incomplete`, `subjects_with_gaps()` and `datasets_for(subject)`. If the section needs a quantity
that is not there, add it to the `dataset_comparison` pipeline (`analysis/tables.py`) and expose it
in `paper/_stats.py` — never compute it inside the paper.

The scaffold's `<!-- AGGREGATES -->` comments show each value's current number next to the
expression that produces it; use them to sanity-check, then write the expression, not the digits.

Verify with an executing build:

```bash
uv run jupyter book build --html --execute
```

### 3. Summary Statistics

Embed the CNeuroMod bubble chart, which compares data volume across CNeuroMod's own datasets
(rows = datasets, columns = modality groups, bubble area = per-subject volume excluding repetitions):

```markdown
:::{figure} ../source_data/dataset_comparison/output_data/cneuromod_comparison_per_subject.png
:name: fig-cneuromod-volume
:width: 100%

**Per-subject data volume across CNeuroMod datasets.** [Caption text here.]
:::
```

Read `source_data/dataset_comparison/output_data/CONTENT.md` and
`source_data/dataset_comparison/CLAUDE.md` for how the figure is produced, and never edit files in
that submodule by hand — regenerate with `uv run invoke run` inside it.

Alongside the figure, write:

- **Aggregate totals** — number of datasets and participants; total and per-participant fMRI hours;
  total physiological (ECG, respiration, plethysmograph, EDA) and eye-tracking hours. Write these as
  `{eval}` expressions over `STATS`, never as digits.
- **Per-subject completeness** — which subjects are `partial` or `not_collected` and why (e.g. `sub-04`
  stopped participating partway through, so many datasets have fewer subjects; Friends season 7 fMRI is
  withheld as a held-out test set). `STATS.subjects_with_gaps()` and `STATS.datasets_for(subject)` give
  the current picture. Summarize the pattern in prose; do not enumerate every entry.

### 4. Dataset Coverage

One `###` subsection per dataset, in the order the scaffold emits (alphabetical), each containing:

- **A condensed overview.** The scaffold carries the full `## Overview` section of the dataset's
  `README.md`. Cut it to two or three sentences: what was acquired, from whom, and what makes the
  paradigm distinctive. Drop installation notes, challenge announcements, and file-layout detail.
- **The reference** — the `preferred-citation` from the dataset's `CITATION.cff`. Prefer a MyST
  `` {cite:p}`key` `` if a matching entry exists in either bibliography; otherwise keep the rendered
  "How to cite" admonition and flag the gap as `[MISSING REF: description]`.

Skip contributors entirely — they belong in `paper/acknowledgements.md`.

Datasets without a `dataset_info.yaml` are not released and must not appear.

### 5. Asset Coverage

Reproduce the recap table (Asset × Datasets) from the scaffold, then give each asset a short text
description under its own `###`. Cover both:

- **Global assets** — the uppercase root-level pages in the submodule (`BIDS.md`, `FMRIPREP.md`,
  `PHYSPREP.md`), available across many datasets.
- **Dataset-local assets** — pages living inside one dataset directory: `anat/SMRIPREP.md`,
  `floc/ROIS.md`, `mario/SCENES.md`, `retinotopy/PRF.md`, `shinobi/TRAINING.md`. Name the dataset each
  belongs to.

Note that `source_data/cneuromod.all/docs/source/contents/{fmriprep,smriprep,physprep,rois,prf,scenes,training}.md`
are build-time **symlinks** to those files; edit nothing there. Likewise `datasets.rst` and
`components.rst` are templates whose tables are placeholders (`_datasets_table_placeholder_`,
`_components_table_placeholder_`) — they carry framing prose, not numbers.

Keep asset descriptions at inventory level: what the asset is and which pipeline produced it.
Quality metrics and pipeline validation belong in `paper/technical_validation.md`.

### 6. Read the available references

Scan both bibliography files:

```
source_data/cneuromod.all/docs/source/cneuromod_references.bib
references.bib
```

Match each dataset's `CITATION.cff` `preferred-citation` and each pipeline (fMRIPrep, sMRIPrep,
Physprep, analyzePRF, BIDS) against them. Only cite keys that exist; never invent citation keys.

### 7. Style rules

- Concise, factual, past tense for completed acquisitions
- Use MyST citation syntax: `` {cite:p}`key` ``
- Flag missing references as `[MISSING REF: description]`
- Keep the three top-level headers (`## Summary Statistics`, `## Dataset Coverage`, `## Asset Coverage`)
- Avoid duplicating `paper/data_record.md` (BIDS file organisation) or `paper/data_acquisition.md`
  (scanner and sequence parameters); this section is about scope, totals and available assets

### 8. Present changes to the user

Before writing to disk, summarize:

- Corrections (values that changed, old → new — and whether the fix was to the prose or to a
  hardcoded number that should have been an `{eval}` expression)
- Additions (datasets or assets newly present in the submodule)
- Omissions (detail intentionally cut from the scaffold and why)
- Missing citations to add to `references.bib`

Ask the user to confirm before applying changes.
