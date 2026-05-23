---
name: update-data-acquisition
description: This skill should be used when a co-author wants to initialize or update paper/data_acquisition.md by cross-referencing the canonical MRI documentation in the cneuromod.all submodule. It reads the current paper section and the technical source docs, identifies new content or corrections, and proposes a revised paper section in the appropriate academic writing style with proper citations.
---

# Update Data Acquisition

## Purpose

To keep `paper/data_acquisition.md` accurate and up-to-date by comparing it against the canonical technical documentation in the `cneuromod.all` submodule, then proposing targeted revisions that match the paper's style and citation conventions.

## Workflow

### 1. Read the current paper section

Read `paper/data_acquisition.md` in full to understand what is already written and at what level of detail.

### 2. Read the source documentation

Read the canonical source documentation:

```
source_data/cneuromod.all/docs/source/contents/participants.md
source_data/cneuromod.all/docs/source/contents/mri.md
```

`participants.md` is the authoritative source for participant demographics, language backgrounds, handedness, and exclusion criteria. `mri.md` is more technical and verbose than the paper section. The goal is not to copy either file verbatim but to extract corrections, additions, or updated details that should be reflected in the paper.

### 3. Read the available references

Scan both bibliography files for citable entries relevant to the acquisition methods:

```
source_data/cneuromod.all/docs/source/cneuromod_references.bib
references.bib
```

Relevant citation keys to look for include entries related to:
- HCP / Human Connectome Project sequences (e.g., Glasser, Xu)
- The spine-generic protocol (Cohen-Adad)
- PsychoPy (Peirce)
- Any other methods cited in `mri.md`

### 4. Identify discrepancies and gaps

Compare the two documents systematically across each subsection:
- **Participants** — gender breakdown (including trans identity), age range, handedness, language background, exclusion criteria, scan frequency, ethics approval (cross-reference `participants.md`)
- **Scanner and setup** — hardware, headcases
- **Functional MRI** — sequence parameters, reference for the HCP EPI sequence
- **Brain anatomical MRI** — full sequence list and parameters (check for missing flip angles, durations, or updated values)
- **Spinal cord anatomical MRI** — sequence list and parameters vs. the spine-generic protocol
- **Stimulus delivery** — projector, audio system, hearing protection details, stimulus software
- **Physiological recordings** — Biopac setup, individual sensors, eye tracking

For each subsection note:
- Parameters present in `mri.md` but absent or different in `data_acquisition.md`
- Details in `data_acquisition.md` that may need a citation added
- Content in `mri.md` too technical for the paper (omit or simplify)

### 5. Propose a revised paper section

Write out the full revised `paper/data_acquisition.md`. Follow these style rules:
- Match the existing paper prose style: concise, factual, past tense for completed acquisitions
- Do not reproduce every parameter from `mri.md`; include what is necessary for reproducibility and scientific context
- Use MyST citation syntax: `{cite:p}\`key\`` for parenthetical citations
- Only cite keys that exist in one of the two `.bib` files above; do not invent citation keys
- If a needed reference is missing from both `.bib` files, flag it explicitly with a `[MISSING REF: description]` placeholder
- Keep section headers and structure identical to the current file unless a new subsection is clearly warranted

### 6. Present changes to the user

Before writing to disk, present a summary of what changed and why. List:
- Corrections (parameter values that were wrong)
- Additions (content present in source docs but missing from paper)
- Omissions (technical detail from `mri.md` intentionally excluded and why)
- Missing citations that need to be added to `references.bib`

Ask the user to confirm before applying the changes.
