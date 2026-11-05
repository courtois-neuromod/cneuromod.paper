#!/usr/bin/env python3
"""Regenerate the author list and per-author contribution recap.

Reads source_data/cneuromod.all/AUTHORS.yaml and */contributors.json and rewrites:
  - the generated `authors` block of the PDF export in myst.yml
  - the author table in paper/index.md
  - paper/_contributions.md and paper/_dataset_funding.md (included by paper/acknowledgements.md)

Paper-specific settings (first authors, corresponding author, fallback
affiliations) live in paper/authors_extra.yaml. Run: uv run python scripts/build_authors.py
"""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'source_data' / 'cneuromod.all'
sys.path.insert(0, str(SRC / 'docs' / 'source'))
from _ext.constants import CREDIT_ROLES  # noqa: E402
from _ext.validator import collect_contributions, load_authors as load_index  # noqa: E402


def load_authors():
    authors = yaml.safe_load((SRC / 'AUTHORS.yaml').read_text(encoding='utf-8'))['authors']
    extra = yaml.safe_load((ROOT / 'paper' / 'authors_extra.yaml').read_text(encoding='utf-8'))
    first, last = extra['first_authors'], extra.get('last_author')
    by_id = {a['id']: a for a in authors}
    middle = sorted(
        (a for a in authors if a['id'] not in first and a['id'] != last),
        key=lambda a: (a['last_name'].lower(), a['first_name'].lower()),
    )
    ordered = [by_id[i] for i in first] + middle + ([by_id[last]] if last else [])
    for a in ordered:
        a['affs'] = a.get('affiliations') or (
            [extra['fallback_affiliations'][a['id']]] if a['id'] in extra['fallback_affiliations'] else []
        )
        a['name'] = f"{a['first_name']} {a['last_name']}".strip()
        a['equal'] = a['id'] in first
        a['corr'] = a['id'] in extra['corresponding']
    return ordered, by_id


def replace_block(path, begin, end, text):
    s = path.read_text(encoding='utf-8')
    pat = re.compile(re.escape(begin) + r'.*?' + re.escape(end), re.S)
    assert pat.search(s), f'markers missing in {path}'
    path.write_text(pat.sub(lambda m: begin + '\n' + text + end, s), encoding='utf-8')


def extra_email(author_id):
    # MyST only accepts `corresponding: true` together with an email; set one under
    # `emails:` in paper/authors_extra.yaml to enable it in the PDF header.
    extra = yaml.safe_load((ROOT / 'paper' / 'authors_extra.yaml').read_text(encoding='utf-8'))
    return (extra.get('emails') or {}).get(author_id)


def myst_authors(ordered):
    entries = []
    for a in ordered:
        e = {'name': a['name']}
        if a.get('orcid'):
            e['orcid'] = a['orcid']
        if a['affs']:
            e['affiliations'] = a['affs']
        if a['equal']:
            e['equal_contributor'] = True
        if a['corr'] and extra_email(a['id']):
            e['corresponding'] = True
            e['email'] = extra_email(a['id'])
        entries.append(e)
    return yaml.safe_dump(entries, allow_unicode=True, sort_keys=False, width=1000)


def index_table(ordered):
    rows = ['| Name | ORCID | Affiliations |', '|---|---|---|']
    for a in ordered:
        mark = ('\\*' if a['equal'] else '') + ('†' if a['corr'] else '')
        orcid = f"[{a['orcid']}](https://orcid.org/{a['orcid']})" if a.get('orcid') else ''
        affs = '; '.join(a['affs']) if a['affs'] else '[MISSING: affiliation]'
        rows.append(f"| {a['name']}{mark} | {orcid} | {affs} |")
    return '\n'.join(rows) + '\n\n\\* shared co-first authorship. † corresponding author.\n'


def author_contributions(ordered):
    """One line per author: each CRediT role followed by the datasets it applies to."""
    extra = yaml.safe_load((ROOT / 'paper' / 'authors_extra.yaml').read_text(encoding='utf-8'))
    roles = extra['paper_contributions']
    default = extra['paper_default_roles']
    contrib = {}
    for a in ordered:
        for r in roles.get(a['id'], default):
            contrib.setdefault(a['name'], {}).setdefault(r, []).append('paper')
    paths = {p.parent.name: p for p in sorted(SRC.glob('*/contributors.json'))}
    index = load_index(SRC / 'AUTHORS.yaml')
    for dataset, entries in collect_contributions(paths, index).items():
        for author, key, rs in entries:
            name = f"{author['first_name']} {author['last_name']}".strip() if author else key
            for r in rs:
                contrib.setdefault(name, {}).setdefault(r, []).append(dataset)
    names = [a['name'] for a in ordered]
    names = [n for n in names if n in contrib] + sorted(n for n in contrib if n not in names)
    out = []
    for n in names:
        parts = [f"{r} ({', '.join(contrib[n][r])})"
                 for r in sorted(contrib[n], key=lambda r: (CREDIT_ROLES + [r]).index(r))]
        out.append(f"- **{n}**: {'; '.join(parts)}.")
    return '\n'.join(out) + '\n'


def dataset_funding():
    """Funders beyond the Courtois Foundation (the project-wide funder), grouped by funder."""
    by_funder = {}
    for p in sorted(SRC.glob('*/contributors.json')):
        for f in json.loads(p.read_text(encoding='utf-8')).get('funding') or []:
            if f['name'] != 'Courtois Foundation':
                by_funder.setdefault(f['name'], []).append(p.parent.name)
    return '\n'.join(f"- **{f}**: {', '.join(d)}." for f, d in by_funder.items()) + '\n'


def main():
    ordered, by_id = load_authors()
    # Authors go on the PDF export only: project-level authors would be shown in the
    # header of every page of the book; the landing page has its own table.
    block = 'authors:\n' + ''.join('  ' + l + '\n' for l in myst_authors(ordered).splitlines())
    replace_block(ROOT / 'myst.yml', '      # BEGIN authors (generated)', '      # END authors (generated)',
                  ''.join('      ' + l + '\n' for l in block.splitlines()))
    replace_block(ROOT / 'paper' / 'index.md', '<!-- BEGIN authors (generated) -->', '<!-- END authors (generated) -->', index_table(ordered))
    header = ('<!-- Generated by scripts/build_authors.py from cneuromod.all contributors.json '
              '(CRediT roles); do not edit. -->\n\n')
    (ROOT / 'paper' / '_contributions.md').write_text(header + author_contributions(ordered), encoding='utf-8')
    (ROOT / 'paper' / '_dataset_funding.md').write_text(header + dataset_funding(), encoding='utf-8')


if __name__ == '__main__':
    main()
