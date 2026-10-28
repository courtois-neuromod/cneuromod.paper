# Co-author review of author metadata

Before the preprint, every co-author confirms their name, ORCID, affiliations and CRediT
contributions. This round covers metadata only; the manuscript text is reviewed in a later round.

Do not start the round until all dataset `contributors.json` files are final upstream: the
review document is generated from them.

## Process

1. **Build the review document.** After bumping `source_data/cneuromod.all`:

   ```bash
   uv run python scripts/build_author_review.py
   ```

   This writes `exports/author_review.md` and `exports/author_review.docx`: the author table of
   <https://docs.cneuromod.ca/AUTHORS.html> (same renderer), followed by the paper-only settings
   from `paper/authors_extra.yaml` (author order, paper roles, missing ORCIDs/affiliations).

2. **Publish.** Upload the .docx to Google Drive as a Google Doc, shared as "anyone with the link
   can comment".

3. **Send** [`email_template.md`](email_template.md) to each co-author. Track replies in a private
   Google Sheet (one row per author: id, name, email, gitid, date sent, reminder date, replied,
   changes requested, PR link, verified); emails are not stored in this repository. Send a
   reminder after 10 days.

4. **Apply corrections.** Export the Doc as .docx and map each comment to an author through the
   table row it is anchored in. Fixes go to:
   - name, ORCID, affiliations → upstream `cneuromod.all/AUTHORS.yaml`, setting `verified: true`
     once the author has confirmed;
   - dataset roles → upstream `cneuromod.all/<dataset>/contributors.json`;
   - paper roles, order, fallback affiliations → `paper/authors_extra.yaml`.

   Then bump the submodule and run `uv run python scripts/build_authors.py`.
