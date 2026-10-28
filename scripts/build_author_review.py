#!/usr/bin/env python3
"""Build the document co-authors comment on to confirm their author metadata.

Reuses the author table of https://docs.cneuromod.ca/AUTHORS.html (rendered by
cneuromod.all's _render_authors_list) and appends the paper-only settings from
paper/authors_extra.yaml. Writes exports/author_review.md and, with pandoc,
exports/author_review.docx (to upload as a Google Doc).
Run: uv run python scripts/build_author_review.py
"""
import re
import subprocess
from types import SimpleNamespace

import yaml

from build_authors import ROOT, SRC, load_authors
from _ext.renderers import _render_authors_list
from _ext.validator import load_authors as load_index

INTRO = """\
# CNeuroMod data paper — author list review

Please find **your row** in the table below and check:

1. your name, as it should be printed;
2. your ORCID (the name links to it; a GitHub link or no link means it is missing);
3. your affiliations (numbers refer to the Affiliations table);
4. your contributions, as [CRediT](https://credit.niso.org/) roles for each dataset, and for the
   paper itself (see "Paper-specific settings" at the end).

Use comments or suggestion mode on your row for anything that needs to change. If everything is
correct, add a comment **"OK"** on your name.

## Contributors

"""


def paper_section(ordered):
    extra = yaml.safe_load((ROOT / 'paper' / 'authors_extra.yaml').read_text(encoding='utf-8'))
    roles, default = extra['paper_contributions'], extra['paper_default_roles']
    out = ['## Paper-specific settings', '',
           'Author order on the paper (\\* shared co-first authorship, † corresponding author):', '']
    out += [f"{i}. {a['name']}{'\\*' if a['equal'] else ''}{'†' if a['corr'] else ''}"
            for i, a in enumerate(ordered, 1)]
    out += ['', 'Roles for the paper and core team (everyone else: '
            f"{', '.join(default)}):", '']
    out += [f"- {a['name']}: {', '.join(roles[a['id']])}" for a in ordered if a['id'] in roles]
    fallback = [a for a in ordered if not a.get('affiliations') and a['affs']]
    if fallback:
        out += ['', 'Affiliations used on the paper but not yet confirmed in AUTHORS.yaml:', '']
        out += [f"- {a['name']}: {'; '.join(a['affs'])}" for a in fallback]
    missing = [(a['name'], [k for k, v in (('ORCID', a.get('orcid')), ('affiliation', a['affs'])) if not v])
               for a in ordered]
    missing = [(n, m) for n, m in missing if m]
    if missing:
        out += ['', 'Missing information:', '']
        out += [f"- {n}: {', '.join(m)}" for n, m in missing]
    return '\n'.join(out) + '\n'


def main():
    ordered, _ = load_authors()
    discovery = SimpleNamespace(
        _authors=load_index(SRC / 'AUTHORS.yaml'),
        _dataset_contributors={p.parent.name: p for p in sorted(SRC.glob('*/contributors.json'))},
    )
    # MyST {sup} role -> pandoc superscript
    table = re.sub(r'\{sup\}`([^`]*)`', r'^\1^', _render_authors_list(discovery))
    out = ROOT / 'exports'
    out.mkdir(exist_ok=True)
    md = out / 'author_review.md'
    md.write_text(INTRO + table + '\n' + paper_section(ordered), encoding='utf-8')
    subprocess.run(['pandoc', str(md), '-o', str(out / 'author_review.docx')], check=True)


if __name__ == '__main__':
    main()
