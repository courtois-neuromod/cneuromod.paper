# CNeuroMod Paper — Project Overview

This is a scientific article about the Courtois NeuroMod (CNeuroMod) dataset, written as a Jupyter Book v2 (MyST) project.

## Build System

- Dependencies are managed with **uv** (`pyproject.toml`).
- The book is built with **Jupyter Book v2**, using MyST markdown.
- The CLI syntax is `jupyter book XXX` (with a space), not `jupyter-book XXX`.
- Always prefix commands with `uv run`: `uv run jupyter book build ...`

## Project Structure

```
myst.yml               # JB2 project config and table of contents (options.source_data points to submodule)
references.bib         # BibTeX references
paper/
  intro.md             # Introduction / Background
  statement_of_need.md
  data_acquisition.md
  data_record.md
  data_overview.md
  technical_validation.md
  usage_notes.md
  data_availability.md
  code_availability.md
  acknowledgements.md  # Acknowledgements, Author Contributions, Funding & Competing Interests
source_data/
  cneuromod.all/          # Git submodule: https://github.com/courtois-neuromod/cneuromod.all
  dataset_comparison/     # Git submodule: depth-vs-breadth neuroimaging dataset comparison
  qa_figures/             # Git submodule: MRIQC/tSNR data quality analysis
  connectome_stats/       # Git submodule: longitudinal stability / state-dependence of connectomes
```

## Source Data

`source_data/cneuromod.all` is a non-recursive git submodule tracking branch `issue11_automate_dataset_info`. Initialize it with:

```bash
git submodule update --init source_data/cneuromod.all
```

The path is registered in `myst.yml` under `project.options.source_data`. The submodule's bibliography (`docs/source/cneuromod_references.bib`) is also listed under `project.bibliography` so its citations are available throughout the book.

### Live numbers — never hardcode a statistic

Datasets are still being collected and released, so any count, hour total or subject tally typed
into `paper/*.md` goes stale silently. Numbers flow through one chain:

```
cneuromod.all/*/dataset_info.yaml     (raw metadata, upstream)
  └─ dataset_comparison analysis/tables.py   (the ONLY place aggregation happens)
       └─ dataset_comparison/output_data/cneuromod_*.csv
            └─ paper/_stats.py             (thin pandas reader, no computation)
                 └─ {eval}`STATS.…` in the prose
```

In a paper file, load the reader once in a hidden cell and quote values inline:

```markdown
```{code-cell} python3
:tags: [remove-cell]
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in (Path("paper"), Path(".")) if (p / "_stats.py").exists())))
from _stats import STATS
```

... a collection of {eval}`STATS.n_datasets` datasets ...
```

`STATS` exposes `n_datasets`, `names`, `n_subjects`, `subjects`, `fmri_total_h`,
`fmri_per_subject_h`, `physiology_h()`, `total_h(modality)`, `per_subject_h(modality)`,
`incomplete`, `subjects_with_gaps()` and `datasets_for(subject)`. Add new quantities by
extending the pipeline in `dataset_comparison`, not by computing them in the paper.

Inline expressions are only evaluated when the build executes the kernel:

```bash
uv run jupyter book build --html --execute
```

Refresh the tables after the submodule moves:

```bash
cd source_data/dataset_comparison && uv run invoke run-cneuromod-tables
```

:::{warning}
Two submodules check out the same upstream `cneuromod.all` repository:
`source_data/cneuromod.all` (narrative, per-dataset READMEs and report cards) and
`source_data/dataset_comparison/source_data/cneuromod` (the numbers). If they sit at different
commits they describe different sets of datasets. Keep them pinned together; the
`update-data-overview` script warns when they drift.
:::

`source_data/dataset_comparison/` is a git submodule (invoke + uv analysis project) that compares dense neuroimaging datasets by depth (brain recording hours per subject) vs. breadth (number of subjects). Its pre-generated figures live in `source_data/dataset_comparison/output_data/`. The key figure for the paper is:

- `output_data/dataset_neuroimaging_depthvsbreadth.png` — Figure 1 of the intro: scatter plot of depth vs. breadth across datasets, with CNeuroMod highlighted in red.

See `source_data/dataset_comparison/CLAUDE.md` for pipeline details. Do not modify files in that directory without running `uv run invoke run` inside it to regenerate outputs.

`source_data/qa_figures/` is a git submodule (invoke + uv analysis project) that computes MRIQC image-quality metrics and per-run/atlas tSNR from the `cneuromod.all` Datalad superdataset. Its main output is:

- `output_data/qa_figure.png` — the fMRI data quality montage used in Technical Validation.

Regenerate its outputs with `uv run invoke fetch && uv run invoke run` inside that directory; do not hand-edit its outputs.

`source_data/connectome_stats/` is a git submodule (invoke + uv analysis project, currently private) that computes per-session, per-network functional connectomes from the `cneuromod.all` parcelled timeseries and measures both longitudinal stability and cognitive-state dependence. Its main output is:

- `output_data/connectome_figure.png` — the connectome stability/state-dependence montage used in Technical Validation.

Regenerate its outputs with `uv run invoke fetch && uv run invoke run` inside that directory (fetching the parcelled timeseries content needs S3 credentials); do not hand-edit its outputs.

## Common Commands

```bash
uv run jupyter book start          # Serve the book as a local website
uv run jupyter book build --pdf paper/intro.md   # Build PDF for a single file
uv run jupyter book build --all    # Build all configured exports
```
