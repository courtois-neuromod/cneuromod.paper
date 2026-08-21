#!/usr/bin/env python3
"""Emit a scaffold for paper/acknowledgements.md and myst.yml authors from contributors.json.

Each dataset repository in `source_data/cneuromod.all/*/contributors.json` carries an
all-contributors file naming who contributed to that dataset and in what capacity. This
script unions those files across datasets: per person, it collects the set of roles (mapped
to CRediT) and the list of datasets they touched.

Identity is resolved through the curated `contributors_aliases.yaml` next to this script —
never guessed. A raw key (GitHub `login`, or `name` when there is no login) missing from
that file is emitted as `[UNMAPPED: <key>]` in the output and listed on stderr; it is never
silently dropped or aliased to its GitHub handle.

Not every dataset carries a contributors.json. The set of datasets that don't is an upstream
gap in cneuromod.all, printed to stderr so it can be fixed there.

Usage:
    uv run python .claude/skills/update-acknowledgements/scripts/build_contributors.py [--repo PATH]
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_DEFAULT = Path("source_data/cneuromod.all")
ALIASES_PATH = Path(__file__).resolve().parent / "contributors_aliases.yaml"

# all-contributors contribution key -> CRediT role(s).
CREDIT_MAP = {
    "ideas": ["Conceptualization"],
    "design": ["Methodology"],
    "code": ["Software"],
    "tool": ["Software"],
    "infra": ["Software"],
    "data": ["Data curation", "Investigation"],
    "projectManagement": ["Project administration"],
    "financial": ["Funding acquisition"],
    "doc": ["Writing – original draft"],
    "content": ["Writing – original draft"],
    "review": ["Writing – review & editing"],
    "question": ["Writing – review & editing"],
    "mentoring": ["Supervision"],
    "userTesting": ["Validation"],
    "bug": ["Validation"],
    "maintenance": ["Validation"],
    "talk": ["Visualization"],  # [REVIEW: confirm this mapping with the user]
}


def datasets_with_contributors(repo):
    return sorted(p.parent for p in repo.glob("*/contributors.json"))


def all_dataset_dirs(repo):
    return sorted(p.parent for p in repo.glob("*/dataset_info.yaml"))


def raw_key(entry):
    """The identity key for a contributors.json entry: login if present, else name."""
    return entry.get("login") or entry.get("name")


def load_aliases():
    if not ALIASES_PATH.exists():
        print(f"ERROR: alias map not found at {ALIASES_PATH}", file=sys.stderr)
        sys.exit(1)
    return yaml.safe_load(ALIASES_PATH.read_text(encoding="utf-8")) or {}


def credit_roles(contributions):
    roles = []
    for c in contributions:
        for role in CREDIT_MAP.get(c, []):
            if role not in roles:
                roles.append(role)
    return roles


def build(repo):
    aliases = load_aliases()

    ds_dirs = all_dataset_dirs(repo)
    ds_with = datasets_with_contributors(repo)
    ds_without = sorted(set(d.name for d in ds_dirs) - set(d.name for d in ds_with))

    people = {}          # canonical key -> {"contributions": set(), "datasets": set(), "raw_keys": set()}
    unmapped = set()

    for ds in ds_with:
        data = json.loads((ds / "contributors.json").read_text(encoding="utf-8"))
        for entry in data.get("contributors", []):
            key = raw_key(entry)
            if key is None:
                continue
            if key not in aliases:
                unmapped.add(key)
                continue
            record = people.setdefault(
                key, {"contributions": set(), "datasets": set(), "raw_keys": set()}
            )
            record["contributions"].update(entry.get("contributions", []))
            record["datasets"].add(ds.name)
            record["raw_keys"].add(key)

    if unmapped:
        print("UNMAPPED identity keys (add to contributors_aliases.yaml):", file=sys.stderr)
        for key in sorted(unmapped):
            print(f"  - {key}", file=sys.stderr)

    if ds_without:
        print(
            f"Upstream gap: {len(ds_without)} dataset(s) have no contributors.json: "
            + ", ".join(ds_without),
            file=sys.stderr,
        )

    return aliases, people, unmapped, ds_without


def render(aliases, people):
    persons = {k: v for k, v in people.items() if aliases[k]["group"] != "institution"}
    institutions = {k: v for k, v in people.items() if aliases[k]["group"] == "institution"}

    core_order = ["julieaboyle1", "bpinsard", "MarieStLaurent", "lunebellec"]
    core_keys = [k for k in core_order if k in persons]
    consortium_keys = sorted(
        (k for k in persons if k not in core_order),
        key=lambda k: (aliases[k]["family_name"] or aliases[k]["full_name"]).lower(),
    )

    out = ["# Contributor scaffold (input for paper/acknowledgements.md and myst.yml)", ""]

    out.append("## Ordered author list")
    out.append("")
    for k in core_keys:
        a = aliases[k]
        star = "" if k == "lunebellec" else " *"
        out.append(f"- {a['full_name']}{star} — {a['affiliation'] or '[MISSING: affiliation]'}")
    for k in consortium_keys:
        a = aliases[k]
        out.append(f"- {a['full_name']} — {a['affiliation'] or '[MISSING: affiliation]'}")
    out.append("")
    out.append("(`*` = shared co-first authorship; core team ordered Boyle, Pinsard, St-Laurent, "
                "then consortium alphabetically by family name, Bellec last as senior/corresponding author.)")
    out.append("")

    out.append("## Author Contributions")
    out.append("")
    for k in core_keys + consortium_keys:
        a = aliases[k]
        p = persons[k]
        roles = credit_roles(p["contributions"])
        ds_list = sorted(p["datasets"])
        ds_str = ", ".join(f"*{d}*" for d in ds_list)
        out.append(
            f"- **{a['full_name']}**: {', '.join(roles) if roles else '[no mapped CRediT role]'}. "
            f"Contributed to the {ds_str} dataset{'s' if len(ds_list) != 1 else ''}."
        )
    out.append("")
    out.append("[TODO: writing contributions (original draft / review & editing per paper section) "
                "are not derivable from contributors.json — add by hand.]")
    out.append("")

    if institutions:
        out.append("## Funding-relevant non-person entries")
        out.append("")
        for k, p in institutions.items():
            a = aliases[k]
            out.append(f"- {a['full_name']}: contributions={sorted(p['contributions'])}, "
                        f"datasets={sorted(p['datasets'])}")
        out.append("")

    out.append("## Raw audit table (person x raw contributions x datasets)")
    out.append("")
    out.append("| Person | Raw contributions (all-contributors) | Datasets |")
    out.append("|---|---|---|")
    for k in core_keys + consortium_keys:
        a = aliases[k]
        p = persons[k]
        out.append(
            f"| {a['full_name']} | {', '.join(sorted(p['contributions']))} | "
            f"{', '.join(sorted(p['datasets']))} |"
        )

    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=REPO_DEFAULT)
    args = ap.parse_args()
    repo = args.repo.resolve()

    aliases, people, unmapped, ds_without = build(repo)
    print(render(aliases, people))


if __name__ == "__main__":
    main()
