#!/usr/bin/env python3
"""Convert the paper to Word, to share as a Google Doc for co-author comments.

MyST's docx export takes a single article, so the whole paper goes through the plain LaTeX
export of myst.yml instead. Build that first (it runs the notebooks, so the live numbers are filled in):

    uv run jupyter book build --tex --execute --execute-parallel 1
    uv run python scripts/build_docx.py

Writes exports/cneuromod_paper.docx. PDF figures are rasterized with pdftoppm (poppler) because
Word cannot embed them; citations are resolved by pandoc's citeproc from the exported main.bib.
"""
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import pypandoc

ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / '_build' / 'exports' / 'cneuromod_paper_tex'
OUT = ROOT / 'exports' / 'cneuromod_paper.docx'


def main():
    if not (TEX / 'cneuromod_paper.tex').exists():
        raise SystemExit(f'{TEX} not found: run `uv run jupyter book build --tex --execute` first')
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / 'tex'
        shutil.copytree(TEX, work)
        for pdf in (work / 'files').glob('*.pdf'):
            subprocess.run(['pdftoppm', '-png', '-r', '200', '-singlefile', str(pdf), str(pdf.with_suffix(''))],
                           check=True)
        for tex in work.glob('*.tex'):
            text = tex.read_text(encoding='utf-8')
            text = re.sub(r'(\\includegraphics(?:\[[^\]]*\])?\{files/[^}]+)\.pdf\}', r'\1.png}', text)
            text = '\n'.join(line for line in text.splitlines() if 'curvenote' not in line)
            tex.write_text(text, encoding='utf-8')
        pypandoc.convert_file(
            str(work / 'cneuromod_paper.tex'), 'docx', format='latex', outputfile=str(OUT),
            extra_args=['--citeproc', '--bibliography', str(work / 'main.bib'),
                        f'--resource-path={work}', '--metadata', 'link-citations=true'],
            cworkdir=str(work),
        )
    print(f'Wrote {OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
