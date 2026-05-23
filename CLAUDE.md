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
  cneuromod.all/       # Git submodule: https://github.com/courtois-neuromod/cneuromod.all
```

## Source Data

`source_data/cneuromod.all` is a non-recursive git submodule tracking branch `issue1_docs_integration`. Initialize it with:

```bash
git submodule update --init source_data/cneuromod.all
```

The path is registered in `myst.yml` under `project.options.source_data`. The submodule's bibliography (`docs/source/cneuromod_references.bib`) is also listed under `project.bibliography` so its citations are available throughout the book.

## Common Commands

```bash
uv run jupyter book start          # Serve the book as a local website
uv run jupyter book build --pdf paper/intro.md   # Build PDF for a single file
uv run jupyter book build --all    # Build all configured exports
```
