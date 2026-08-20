---
name: update-data-availability
description: This skill should be used when a co-author wants to initialize or update paper/data_availability.md by cross-referencing the canonical access and downloading documentation in the cneuromod.all submodule. It reads the current paper section and the relevant source docs, identifies new content or corrections, and proposes a revised paper section in the appropriate academic writing style with proper citations.
---

# Update Data Availability

## Purpose

To keep `paper/data_availability.md` accurate and up-to-date by comparing it against the canonical documentation in the `cneuromod.all` submodule, then proposing targeted revisions that match the paper's style and citation conventions.

## Workflow

### 1. Read the current paper section

Read `paper/data_availability.md` in full.

### 2. Read the source documentation

Read the following source doc(s):

```
source_data/cneuromod.all/docs/source/contents/access.md
source_data/cneuromod.all/docs/source/contents/downloading.md
```

These files may be more technical or verbose than the paper section. Extract corrections, additions, or updated information — do not copy verbatim. Focus on: where the data are deposited (data portal, DOIs), what license or data use agreement governs access, and how access is granted/requested (e.g. account creation, approval process, datalad/git-annex download instructions).

### 3. Read the available references

Scan both bibliography files:

```
source_data/cneuromod.all/docs/source/cneuromod_references.bib
references.bib
```

Look for citable entries relevant to the data portal, license, or access mechanisms described in this section.

### 4. Identify discrepancies and gaps

Compare the two documents across each subsection. For each note:
- Information in the source doc absent or incorrect in the paper (deposit location, DOIs, license terms, access conditions)
- Details that need a citation added
- Content too technical for the paper (e.g. step-by-step datalad commands — omit or simplify to a pointer)

### 5. Propose a revised paper section

Write the full revised `paper/data_availability.md`. Style rules:
- Match the existing paper prose: concise, factual, past tense for completed work
- Use MyST citation syntax: `{cite:p}\`key\``
- Only cite keys that exist in one of the two `.bib` files; never invent citation keys
- Flag missing references as `[MISSING REF: description]`
- Keep section headers and structure identical unless a new subsection is clearly warranted

### 6. Present changes to the user

Before writing to disk, summarize:
- Corrections (values or facts that were wrong)
- Additions (content in source docs missing from paper)
- Omissions (technical detail intentionally excluded and why)
- Missing citations to add to `references.bib`

Ask the user to confirm before applying changes.
