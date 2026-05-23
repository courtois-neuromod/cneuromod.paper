---
name: update-intro
description: This skill should be used when a co-author wants to initialize or update paper/intro.md by cross-referencing the canonical participant documentation in the cneuromod.all submodule and the dataset comparison figure. It reads the current introduction section and the relevant source docs, identifies new content or corrections, and proposes a revised paper section in the appropriate academic writing style with proper citations. Use it when someone mentions "update intro", "figure 1", "depth vs breadth", or "dataset comparison figure".
---

# Update Introduction

## Purpose

To keep `paper/intro.md` accurate and up-to-date by comparing it against the canonical participant documentation in the `cneuromod.all` submodule, then proposing targeted revisions that match the paper's style and citation conventions. This skill also ensures Figure 1 (the depth-vs-breadth dataset comparison) is properly embedded and captioned.

## Workflow

### 1. Read the current paper section

Read `paper/intro.md` in full.

### 2. Read the source documentation

Read the participant demographics doc:

```
source_data/cneuromod.all/docs/source/contents/participants.md
```

This documents participant count, age range, sex/gender breakdown, language background, handedness, and inclusion/exclusion criteria.

Also read the dataset overview for high-level coverage of the 29 datasets and cognitive domains:

```
source_data/cneuromod.all/docs/source/contents/datasets.rst
```

### 3. Check the dataset comparison figure

The figure for Figure 1 is a pre-generated PNG:

```
source_data/dataset_comparison/output_data/dataset_neuroimaging_depthvsbreadth.png
```

Read `source_data/dataset_comparison/CLAUDE.md` for background on how the figure was produced (depth = brain recording hours per subject; breadth = number of subjects; CNeuroMod is highlighted in red as the extreme-depth dataset). The figure should be embedded in `paper/intro.md` as Figure 1 using MyST syntax:

```markdown
:::{figure} ../source_data/dataset_comparison/output_data/dataset_neuroimaging_depthvsbreadth.png
:name: fig-depth-breadth
:width: 80%

**Brain recordings depth vs. breadth.** [Caption text here.]
:::
```

If Figure 1 is already present but the path or caption needs updating, propose a correction. If it is absent, propose its insertion at the appropriate place in the intro (typically after the paragraph motivating individual depth).

### 4. Read the available references

Scan both bibliography files:

```
source_data/cneuromod.all/docs/source/cneuromod_references.bib
references.bib
```

Look for citable entries relevant to brain encoding models, ANN-brain alignment, neuroimaging datasets, or CNeuroMod-specific papers. Also check for references to the datasets shown in the figure (HCP, NSD, IBC, studyforrest, etc.) that may be needed for the caption.

### 5. Identify discrepancies and gaps

Compare the paper introduction against the source docs across these themes:
- Participant demographics (count, age range, sex/gender breakdown, language background, handedness)
- Dataset count and cognitive domain coverage
- Scanning duration per participant
- Claims about dataset uniqueness or scale relative to other resources
- Presence and accuracy of Figure 1 embedding and caption
- Any facts that need a citation added

For each note:
- Information in the source doc absent or incorrect in the paper
- Details that need a citation added
- Content too technical for the paper introduction (omit or simplify)

### 6. Propose a revised paper section

Write the full revised `paper/intro.md`. Style rules:
- Match the existing paper prose: concise, factual, present or past tense as appropriate
- The abstract admonition (`{admonition} Abstract`) should remain as a placeholder if not yet filled
- Use MyST citation syntax: `` {cite:p}`key` ``
- Only cite keys that exist in one of the two `.bib` files; never invent citation keys
- Flag missing references as `[MISSING REF: description]`
- Keep section headers and structure identical unless a new subsection is clearly warranted

### 7. Present changes to the user

Before writing to disk, summarize:
- Corrections (values or facts that were wrong)
- Additions (content in source docs or figure missing from paper)
- Omissions (technical detail intentionally excluded and why)
- Missing citations to add to `references.bib`

Ask the user to confirm before applying changes.
