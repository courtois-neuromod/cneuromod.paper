**To:** yourself — **BCC:** all co-authors
**Subject:** CNeuroMod data paper — preprint next week: please check your author entry by Friday 13 November

Dear colleagues,

It's a big day for CNeuroMod: the data paper is ready for preprint! We plan to post it next week,
to coincide with the launch of the Algonauts 2027 competition. You are receiving this email
because you are listed as a co-author. Before we post it, I need each of you to check a few things.

The paper is shared as a Google Doc where anyone with the link can comment:
https://docs.google.com/document/d/1yCNMDuuzsJqBXlkWpoDEyAhffFXqg2UQ/edit

1. **Your name, affiliations and ORCID.** Check your row in the author list:
   https://docs.google.com/document/d/1yCNMDuuzsJqBXlkWpoDEyAhffFXqg2UQ/edit#heading=h.6juref69dgmj
   Missing ORCIDs and affiliations show as empty or `[MISSING: affiliation]`; please send them if
   that's you.
2. **Your contributions.** Check your CRediT roles (https://credit.niso.org), listed per author
   with the datasets each role applies to (`paper` stands for the manuscript itself and the core
   team):
   https://docs.google.com/document/d/1yCNMDuuzsJqBXlkWpoDEyAhffFXqg2UQ/edit#heading=h.axivcd6ztfjk
3. **Competing interests.** The paper currently states that the authors declare no competing
   interests. Please confirm this applies to you, or tell me what should be declared:
   https://docs.google.com/document/d/1yCNMDuuzsJqBXlkWpoDEyAhffFXqg2UQ/edit#heading=h.aj1urnsbvw5q
4. **If time permits**, skim the description of the dataset(s) you contributed to (one
   subsection per dataset in "Data Overview"; acquisition and validation details are in the
   following sections) and flag any big mistake. This is not the time for line edits: there will
   be plenty of opportunities to improve the text later.

The same content is also available as a website, https://paper.cneuromod.ca, if you prefer
reading it there.

**Deadline: Friday 13 November.** If I have not heard from you by then, I will take you off the
author list of the preprint. A one-line "all good, no competing interests" is enough. If you
need a few more days, just let me know.

**How to send feedback**, whichever is easiest for you:

- reply to this email;
- comment directly in the Google Doc (link above);
- open a pull request on GitHub (see below).

**What happens next.** After the preprint, we will spend about 3 to 6 months iterating on the
manuscript, and you will have more chances to comment on the text. Several key technical
validation papers are on their way (mario, multfs, emotion-videos, mute-music, triplets,
langloc). Once they are available as preprints, we will submit the core paper. In the meantime,
I will approach editors at a few journals to gauge their interest.

**For those who want to open a pull request.** The author list, the contributions and the
dataset descriptions are all generated from https://github.com/courtois-neuromod/cneuromod.all
(the CNeuroMod DataLad superdataset, whose documentation is rendered at
https://docs.cneuromod.ca). The files that matter:

- `AUTHORS.yaml`: one entry per person (name, ORCID, affiliations, GitHub ID). Once you have
  checked your entry, set `verified: true` in it; this is how we record your confirmation.
- `<dataset>/contributors.json`: the CRediT roles of each contributor to that dataset (people
  are referenced by `gitid`, `orcid` or `id`, which must match `AUTHORS.yaml`).
- `<dataset>/README.md`: the description of the dataset, which the paper's Data Overview
  section is built from.
- `<dataset>/dataset_info.yaml`: structured facts (subjects, modalities, maturity). The hours and
  counts in its `stats` block are generated automatically: please don't edit them by hand,
  just tell us if they look wrong.
- `<dataset>/CITATION.cff`: the reference(s) to cite for that dataset.
- `docs/source/`: shared documentation pages (participants, MRI acquisition, access,
  downloading) and the bibliography `cneuromod_references.bib`.

The manuscript itself lives in https://github.com/courtois-neuromod/cneuromod.paper (one
MyST markdown file per section in `paper/`). The author table and the contributions in the paper
are generated from `cneuromod.all`, so please fix those upstream rather than in the paper.

Thank you all for the years of work that went into this dataset. I am very excited to finally
share it!

Lune
