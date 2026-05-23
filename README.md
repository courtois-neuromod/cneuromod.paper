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

This clones [`courtois-neuromod/cneuromod.all`](https://github.com/courtois-neuromod/cneuromod.all) (branch `issue1_docs_integration`) into `source_data/cneuromod.all/`, which provides the shared bibliography used by this book.

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

## Project Structure

| File / Folder | Description |
|---|---|
| `myst.yml` | Book configuration and table of contents |
| `references.bib` | BibTeX references (paper-specific) |
| `source_data/cneuromod.all/` | Git submodule — shared dataset docs and bibliography |
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
