# The Courtois NeuroMod (CNeuroMod) Dataset

This repository contains the source for the CNeuroMod dataset paper, written in [MyST Markdown](https://mystmd.org) and compiled with [Jupyter Book v2](https://next.jupyterbook.org).

## Setup

Install dependencies with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

Initialize the source data submodule:

```bash
git submodule update --init source_data/cneuromod.all
```

This clones [`courtois-neuromod/cneuromod.all`](https://github.com/courtois-neuromod/cneuromod.all) (branch `issue11_automate_dataset_info`) into `source_data/cneuromod.all/`, which provides the shared bibliography used by this book.

## Compiling the Article

### Preview as a website

```bash
uv run jupyter book start
```

This launches a local development server with live reload. Open the URL printed in the terminal.

### Build a static HTML site

```bash
uv run jupyter book build --html
```

Output is written to `_build/html/`.

### Build a PDF

```bash
uv run jupyter book build --pdf
```

### Build all export formats

```bash
uv run jupyter book build --all
```

## Claude Code Skills

This project includes [Claude Code](https://claude.ai/code) skills to help co-authors draft and update paper sections. Skills are located in `.claude/skills/` and are automatically available to all collaborators who open this repo in Claude Code.

| Skill | Trigger | Description |
|---|---|---|
| `update-data-acquisition` | "update data acquisition" or `/update-data-acquisition` | Cross-references `paper/data_acquisition.md` against the `cneuromod.all` MRI docs, identifies corrections and new content, and proposes a revised paper section with proper citations. |
| `update-intro` | "update intro", "figure 1", "depth vs breadth", or `/update-intro` | Cross-references `paper/intro.md` against `participants.md`, `datasets.rst`, and the dataset comparison figure (`source_data/dataset_comparison/output_data/dataset_neuroimaging_depthvsbreadth.png`), and proposes a revised intro with Figure 1 embedded. |
| `paper-skill-creator` | "create a skill for [paper section]" or `/paper-skill-creator` | Creates a new skill for drafting or updating any `paper/*.md` section, following the same pattern as `update-data-acquisition`. Also updates this README table. |

## Project Structure

| File / Folder | Description |
|---|---|
| `myst.yml` | Book configuration and table of contents |
| `references.bib` | BibTeX references (paper-specific) |
| `source_data/cneuromod.all/` | Git submodule — shared dataset docs and bibliography |
| `source_data/dataset_comparison/` | Git submodule — depth-vs-breadth dataset comparison figure |
| `source_data/qa_figures/` | Git submodule — MRIQC/tSNR data quality analysis |
| `source_data/connectome_stats/` | Git submodule — longitudinal stability / state-dependence of connectomes |
| `paper/intro.md` | Introduction / Background |
| `paper/statement_of_need.md` | Statement of Need |
| `paper/data_acquisition.md` | Data Acquisition |
| `paper/data_record.md` | Data Record |
| `paper/data_overview.md` | Data Overview |
| `paper/technical_validation.md` | Technical Validation |
| `paper/usage_notes.md` | Usage Notes |
| `paper/data_availability.md` | Data Availability |
| `paper/code_availability.md` | Code Availability |
| `paper/acknowledgements.md` | Acknowledgements, Author Contributions, Funding & Competing Interests |
