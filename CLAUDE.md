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
  statistics/             # Git submodule: per-dataset CNeuroMod statistics and bubble chart
  qa_figures/             # Git submodule: MRIQC/tSNR data quality analysis
  connectome_stats/       # Git submodule: longitudinal stability / state-dependence of connectomes
  anat_stability/         # Git submodule: longitudinal stability of grey matter volume
  reuse_stats/            # Git submodule: reuse of the dataset (papers by year and type)
```

## Source Data

`source_data/cneuromod.all` is a non-recursive git submodule tracking branch `main`. Initialize it with:

```bash
git submodule update --init source_data/cneuromod.all
```

The path is registered in `myst.yml` under `project.options.source_data`. The submodule's bibliography (`docs/source/cneuromod_references.bib`) is also listed under `project.bibliography` so its citations are available throughout the book.

### Authors and contributions

`scripts/build_authors.py` regenerates, from `source_data/cneuromod.all` (`AUTHORS.yaml` and `*/contributors.json`), the `authors` block of the PDF export in `myst.yml` (not `project.authors`, which MyST would show in every page header) (between the `BEGIN/END authors (generated)` markers), the author table in `paper/index.md`, and `paper/_contributions.md` (the per-dataset CRediT recap included by `paper/acknowledgements.md`). Do not hand-edit those generated parts. Author order, co-first/corresponding authors and fallback affiliations live in `paper/authors_extra.yaml`. Run `uv run python scripts/build_authors.py` after bumping the submodule.

### Live numbers — never hardcode a statistic

Datasets are still being collected and released, so any count, hour total or subject tally typed
into `paper/*.md` goes stale silently. Numbers flow through one chain:

```
cneuromod.all/*/dataset_info.yaml     (raw metadata, upstream)
  └─ statistics analysis/dataset_info.py   (the ONLY place aggregation happens)
       └─ statistics/output_data/cneuromod_*.csv   (git-tracked upstream)
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
extending the pipeline in `statistics`, not by computing them in the paper.

Inline expressions are only evaluated when the build executes the kernel:

```bash
uv run jupyter book build --html --execute
```

Refresh the tables after `cneuromod.all` moves (in the `statistics` submodule, then commit and
push its outputs there and bump the submodule here):

```bash
cd source_data/statistics && uv run invoke fetch && uv run invoke run --force
```

:::{warning}
Three places depend on the upstream `cneuromod.all` repository:
`source_data/cneuromod.all` (narrative, per-dataset READMEs and report cards), the commit the
`statistics` tables were generated from (recorded in `source_data/statistics/source_data/MANIFEST.json`;
the numbers) and `source_data/dataset_comparison/source_data/cneuromod` (the comparison figures).
If they sit at different commits they describe different sets of datasets. Keep them pinned
together; the `update-data-overview` script warns when they drift.
A difference confined to `cneuromod.all`'s own `analysis/cneuromod.all.statistics` pointer is
expected (the tables are always generated one pointer bump earlier) and is not reported.
:::

`source_data/dataset_comparison/` is a git submodule (invoke + uv analysis project) that compares dense neuroimaging datasets by depth (brain recording hours per subject) vs. breadth (number of subjects). Its pre-generated figures live in `source_data/dataset_comparison/output_data/`. The key figure for the paper is:

- `output_data/dataset_neuroimaging_depthvsbreadth.png` — Figure 1 of the intro: scatter plot of depth vs. breadth across datasets, with CNeuroMod highlighted in red.

See `source_data/dataset_comparison/CLAUDE.md` for pipeline details. Do not modify files in that directory without running `uv run invoke run` inside it to regenerate outputs.

`source_data/statistics/` is a git submodule (invoke + uv analysis project, from `courtois-neuromod/cneuromod.all.statistics`) that computes per-dataset CNeuroMod statistics; the per-dataset comparison moved here from `dataset_comparison`. Its tracked tidy tables (`cneuromod_tidy_per_subject.csv`, `cneuromod_tidy_total.csv`, `cneuromod_subjects.csv`) are what `paper/_stats.py` reads. Its main output is:

- `output_data/figure_cneuromod_comparison_per_subject.png` — the per-subject data volume bubble chart in Data Overview, rows grouped and colored by cognitive category (its `CATEGORIES` mirror the paper's; keep them in sync).

Regenerate its outputs with `uv run invoke fetch && uv run invoke run` inside that directory; do not hand-edit its outputs.

`source_data/qa_figures/` is a git submodule (invoke + uv analysis project) that computes MRIQC image-quality metrics and per-run/atlas tSNR from the `cneuromod.all` Datalad superdataset. Its main output is:

- `output_data/qa_figure.png` — the fMRI data quality montage used in Technical Validation.

Regenerate its outputs with `uv run invoke fetch && uv run invoke run` inside that directory; do not hand-edit its outputs.

`source_data/connectome_stats/` is a git submodule (invoke + uv analysis project, currently private) that computes per-session, per-network functional connectomes from the `cneuromod.all` parcelled timeseries and measures both longitudinal stability and cognitive-state dependence. Its main output is:

- `output_data/connectome_figure.png` — the connectome stability/state-dependence montage used in Technical Validation.

Regenerate its outputs with `uv run invoke fetch && uv run invoke run` inside that directory (fetching the parcelled timeseries content needs S3 credentials); do not hand-edit its outputs.

`source_data/anat_stability/` is a git submodule (invoke + uv analysis project, from `courtois-neuromod/anat.stability_grey_matter`) that measures how stable grey matter volume is across each participant's longitudinal FreeSurfer sessions, per region and network. `paper/_anat_stats.py` reads its tracked tables (`stability_per_region.tsv`, `volume_trajectories.tsv`, `trajectory_slopes.tsv`) for the live numbers in "Stability of brain structure". Its main output is:

- `output_data/fig_anat_stability.png` — the grey matter stability montage used in Technical Validation. It is committed upstream so the CI build can render it; commit it again after each pipeline run that changes it.

Regenerate its outputs with `uv run invoke fetch && uv run invoke run` inside that directory (`invoke fetch --cneuromod-source /path` links an existing `cneuromod.all` checkout; sub-04's native-space label volumes need credentials); do not hand-edit its outputs.

`source_data/reuse_stats/` is a git submodule (invoke + uv analysis project) that counts papers using CNeuroMod data, by year and publication type, from the `cneuromod.all` reference list. Its main output is:

- `output_data/figure_montage.png` — the reuse figure shown at the beginning of Usage Notes.

Regenerate its outputs with `uv run invoke fetch && uv run invoke run` inside that directory; do not hand-edit its outputs.

## Common Commands

```bash
uv run jupyter book start          # Serve the book as a local website
uv run jupyter book build --pdf paper/intro.md   # Build PDF for a single file
uv run jupyter book build --all    # Build all configured exports
```
