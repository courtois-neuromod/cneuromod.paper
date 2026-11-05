# Co-author review round

Before the preprint, every co-author confirms their name, ORCID, affiliations and CRediT
contributions, and may flag big mistakes in the description of their dataset(s). Round 1 started
on 2026-11-05; the deadline is **Friday 2026-11-13**, after which authors who have not replied are
removed from the preprint's author list. Line edits on the manuscript come in later rounds
(3–6 months of iteration before journal submission).

## Process

1. **Sync the sources.** Bump `source_data/cneuromod.all`, run
   `uv run python scripts/build_authors.py`, check that the `statistics` tables are pinned to the
   same upstream commit, and merge to `main` so https://paper.cneuromod.ca is current.

2. **Build the Word version** and upload it to Google Drive (File → Open → Upload; it converts to
   a Google Doc), shared as "anyone with the link can comment":

   ```bash
   uv run jupyter book build --tex --execute --execute-parallel 1
   uv run python scripts/build_docx.py   # exports/cneuromod_paper.docx
   ```

3. **Send** [`email_template.md`](email_template.md) as one email, all co-authors in BCC. It links
   to the live pages (authors on the landing page, contributions in Acknowledgements, datasets in
   Data Overview) and the Google Doc. Track replies in a private Google Sheet (one row per author:
   id, name, date sent, replied, changes requested, PR link, verified); emails are not stored in
   this repository.

4. **Apply corrections**, from email replies, Google Doc comments or pull requests:
   - name, ORCID, affiliations → upstream `cneuromod.all/AUTHORS.yaml`, setting `verified: true`
     once the author has confirmed;
   - dataset roles → upstream `cneuromod.all/<dataset>/contributors.json`;
   - dataset descriptions → upstream `cneuromod.all/<dataset>/README.md`, then the
     `update-data-overview` skill;
   - paper roles, order, fallback affiliations → `paper/authors_extra.yaml`.

   Then bump the submodule and run `uv run python scripts/build_authors.py`.

`scripts/build_author_review.py` builds a standalone author-table document (the earlier,
metadata-only version of this round); it is not needed when the live site is used.
