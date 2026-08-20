#!/usr/bin/env python3
"""Emit a MyST scaffold for paper/data_overview.md from the CNeuroMod submodules.

Two sources, each used for what it owns, with no aggregation duplicated here:

- `source_data/cneuromod.all` — narrative and per-dataset metadata. Its own Sphinx extension
  renderers are reused so the "report card" (Key facts table) and the citation block are
  byte-for-byte what the documentation website shows.
- `source_data/dataset_comparison/output_data/*.csv` — every aggregate number, read through
  `paper/_stats.py`. That pipeline is the single place where `dataset_info.yaml` files are
  summed; see its `analysis/tables.py`.

Everything printed here is a starting point: the prose is meant to be condensed and edited
by hand afterwards.

Usage:
    uv run python .claude/skills/update-data-overview/scripts/build_overview.py [--repo PATH]
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "paper"))
from _stats import STATS  # noqa: E402  (path set above)

REPO_DEFAULT = Path("source_data/cneuromod.all")


def load_renderers(repo):
    """Import the submodule's own renderers (_render_key_facts, _render_citation)."""
    sys.path.insert(0, str((repo / "docs" / "source").resolve()))
    from _ext.constants import _DATASET_EMOJI, _COMPONENT_ICON, _ROOT_MD_EXCLUDE, _ROOT_MD_MANUAL
    from _ext.renderers import _render_key_facts, _render_citation, _extract_component_title
    return {
        "emoji": _DATASET_EMOJI,
        "component_icon": _COMPONENT_ICON,
        "root_exclude": _ROOT_MD_EXCLUDE,
        "root_manual": _ROOT_MD_MANUAL,
        "key_facts": _render_key_facts,
        "citation": _render_citation,
        "component_title": _extract_component_title,
    }


def datasets(repo):
    """Dataset directories, i.e. those carrying a dataset_info.yaml."""
    return sorted(p.parent for p in repo.glob("*/dataset_info.yaml"))


def overview_text(readme):
    """The '## Overview' section of a dataset README, admonitions stripped."""
    if not readme.exists():
        return ""
    body = readme.read_text(encoding="utf-8")
    m = re.search(r"^##\s+Overview\s*$(.*?)(?=^##\s|\Z)", body, re.M | re.S)
    text = m.group(1) if m else body
    text = re.sub(r":::.*?:::", "", text, flags=re.S)
    return "\n\n".join(p.strip() for p in text.strip().split("\n\n") if p.strip())


def first_para(body):
    """First real paragraph of an asset page, skipping any leading sub-heading."""
    for para in body.split("\n\n"):
        # drop heading lines that sit flush against the paragraph they introduce
        para = "\n".join(l for l in para.split("\n") if not l.startswith("#")).strip()
        if para:
            return para
    return ""


def components(repo, R):
    """(global_assets, local_assets, per_dataset) discovered the same way the docs do."""
    global_assets = [
        (f.stem, f)
        for f in sorted(repo.glob("*.md"))
        if f.stem[0].isupper() and f.name not in R["root_exclude"] | R["root_manual"]
    ]
    local_assets = [
        (f.stem, f, ds.name)
        for ds in datasets(repo)
        for f in sorted(ds.glob("*.md"))
        if f.stem[0].isupper() and f.name != "README.md"
    ]
    per_dataset = {
        ds.name: [stem for stem, _ in global_assets if (ds / stem.lower()).is_dir()]
        for ds in datasets(repo)
    }
    return global_assets, local_assets, per_dataset


def check_in_sync(repo):
    """Warn when the paper's cneuromod.all and the pipeline's cneuromod are different commits.

    Both submodules track the same upstream repository. If they drift, the narrative in this
    scaffold and the numbers in the CSVs describe different sets of datasets.
    """
    other = STATS.output_data.parent / "source_data" / "cneuromod"
    heads = []
    for path in (repo, other):
        try:
            heads.append(
                subprocess.run(
                    ["git", "-C", str(path), "rev-parse", "HEAD"],
                    capture_output=True, text=True, check=True,
                ).stdout.strip()
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return
    if heads[0] != heads[1]:
        print(
            f"WARNING: cneuromod checkouts differ.\n"
            f"  {repo} @ {heads[0][:8]}\n"
            f"  {other} @ {heads[1][:8]}\n"
            f"  Numbers come from the second, narrative from the first. Sync them before publishing.",
            file=sys.stderr,
        )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=REPO_DEFAULT)
    args = ap.parse_args()
    repo = args.repo.resolve()
    R = load_renderers(repo)
    check_in_sync(repo)

    out = ["# Data Overview", "", "## Summary Statistics", ""]
    out += [
        "<!-- Figures live in the dataset_comparison submodule; do not edit them by hand. -->",
        ":::{figure} ../source_data/dataset_comparison/output_data/cneuromod_comparison_per_subject.png",
        ":name: fig-cneuromod-volume",
        ":width: 100%",
        "",
        "**Per-subject data volume across CNeuroMod datasets.** [Caption to write.]",
        ":::",
        "",
        "<!-- AGGREGATES — read from dataset_comparison/output_data via paper/_stats.py. -->",
        "<!-- Do not retype these into the prose: use {eval}`STATS...` so they stay live. -->",
        f"<!-- STATS.n_datasets = {STATS.n_datasets} -->",
        f"<!-- STATS.n_subjects = {STATS.n_subjects} ({', '.join(STATS.subjects)}) -->",
        f"<!-- STATS.fmri_total_h = {STATS.fmri_total_h} -->",
        f"<!-- STATS.fmri_per_subject_h = {STATS.fmri_per_subject_h} -->",
    ]
    for label, hours in STATS.physiology_h().items():
        out.append(f"<!-- STATS.physiology_h()['{label}'] = {hours} -->")
    out += ["", "<!-- Coverage gaps (STATS.subjects_with_gaps / STATS.datasets_for): -->"]
    for subject, n in STATS.subjects_with_gaps():
        out.append(f"<!-- {subject}: missing or partial in {n} dataset(s) -->")

    out += ["", "## Dataset Coverage", ""]
    for ds in datasets(repo):
        emoji = R["emoji"].get(ds.name, "📦")
        out += [f"### {emoji} {ds.name}", "", overview_text(ds / "README.md"), ""]
        facts = R["key_facts"](ds / "dataset_info.yaml")
        out += [facts.replace("## Key facts", "").strip(), ""]
        cff = ds / "CITATION.cff"
        if cff.exists():
            out += [R["citation"](cff).strip(), ""]

    global_assets, local_assets, per_dataset = components(repo, R)
    out += ["", "## Asset Coverage", "", "| Asset | Datasets |", "|---|---|"]
    for stem, path in global_assets:
        _, title, _ = R["component_title"](path.read_text(encoding="utf-8"))
        users = [n for n, comps in sorted(per_dataset.items()) if stem in comps]
        out.append(f"| {R['component_icon'].get(stem.lower(), '')} {title or stem} | {', '.join(users)} |")
    for stem, path, ds_name in sorted(local_assets):
        _, title, _ = R["component_title"](path.read_text(encoding="utf-8"))
        out.append(f"| {R['component_icon'].get(stem.lower(), '')} {title or stem} | {ds_name} |")
    out.append("")
    for stem, path in global_assets:
        _, title, body = R["component_title"](path.read_text(encoding="utf-8"))
        out += [f"### {title or stem}", "", f"<!-- condense from {path.relative_to(repo)} -->", first_para(body), ""]
    for stem, path, ds_name in sorted(local_assets):
        _, title, body = R["component_title"](path.read_text(encoding="utf-8"))
        out += [f"### {title or stem} ({ds_name})", "", f"<!-- condense from {path.relative_to(repo)} -->", first_para(body), ""]

    print("\n".join(out))


if __name__ == "__main__":
    main()
