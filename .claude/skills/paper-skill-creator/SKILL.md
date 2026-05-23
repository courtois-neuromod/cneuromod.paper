---
name: paper-skill-creator
description: This skill should be used when a co-author wants to create a new Claude Code skill for drafting or updating a section of the CNeuroMod paper (paper/*.md). It produces a ready-to-use skill file at .claude/skills/SKILL_NAME/SKILL.md and updates README.md. Use it whenever someone says "create a skill for [paper section]" or "add a skill to update [section name]".
---

# Paper Skill Creator

## Purpose

To create a new project-level Claude Code skill that helps co-authors draft or update a specific section of `paper/*.md` by cross-referencing the canonical source documentation in `source_data/cneuromod.all/docs/source/`.

Each skill produced by this workflow follows the same pattern as `update-data-acquisition`: read the current paper section, read the relevant source docs, compare them, and propose a revised section with proper citations.

## Source documentation map

The following source docs are available in `source_data/cneuromod.all/docs/source/contents/` and map to paper sections:

| Paper section | Primary source doc(s) |
|---|---|
| `paper/data_acquisition.md` | `mri.md` |
| `paper/data_record.md` | `bids.md`, `datasets.rst` |
| `paper/data_overview.md` | `datasets.rst`, `components.rst` |
| `paper/technical_validation.md` | `fmriprep.md`, `physprep.md` |
| `paper/usage_notes.md` | `access.md`, `downloading.md`, `fmriprep.md` |
| `paper/intro.md` | `participants.md` |
| `paper/statement_of_need.md` | (no direct source doc; use general project context) |

Both bibliography files are always relevant:
- `source_data/cneuromod.all/docs/source/cneuromod_references.bib`
- `references.bib`

## Workflow

### 1. Identify the target paper section

Ask the user (or infer from context) which `paper/*.md` section the new skill is for. Confirm the skill name to use, following the convention `update-<section-name>` (e.g., `update-data-record`, `update-usage-notes`).

### 2. Determine the relevant source docs

Use the map above to identify which file(s) in `source_data/cneuromod.all/docs/source/contents/` the skill should read. If no clear mapping exists, read the directory listing and use judgment.

### 3. Write the skill file

Create `.claude/skills/<skill-name>/SKILL.md` with the following structure, adapted for the specific section:

```markdown
---
name: <skill-name>
description: This skill should be used when a co-author wants to initialize or update <paper section file> by cross-referencing the canonical documentation in the cneuromod.all submodule. It reads the current paper section and the relevant source docs, identifies new content or corrections, and proposes a revised paper section in the appropriate academic writing style with proper citations.
---

# Update <Section Title>

## Purpose

To keep `<paper section file>` accurate and up-to-date by comparing it against the canonical documentation in the `cneuromod.all` submodule, then proposing targeted revisions that match the paper's style and citation conventions.

## Workflow

### 1. Read the current paper section

Read `<paper section file>` in full.

### 2. Read the source documentation

Read the following source doc(s):

```
<list source doc paths>
```

These files may be more technical or verbose than the paper section. Extract corrections, additions, or updated information — do not copy verbatim.

### 3. Read the available references

Scan both bibliography files:

```
source_data/cneuromod.all/docs/source/cneuromod_references.bib
references.bib
```

Look for citable entries relevant to the methods or content described in this section.

### 4. Identify discrepancies and gaps

Compare the two documents across each subsection. For each note:
- Information in the source doc absent or incorrect in the paper
- Details that need a citation added
- Content too technical for the paper (omit or simplify)

### 5. Propose a revised paper section

Write the full revised `<paper section file>`. Style rules:
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
```

### 4. Update README.md

Add a row for the new skill to the Claude Code Skills table in `README.md`:

```markdown
| `<skill-name>` | "update <section name>" or `/<skill-name>` | <one-line description of what it cross-references> |
```

### 5. Confirm with the user

Show the user the created skill path and the README addition. Do not run the skill itself — just report that it is ready to use.

## Rules for all produced skills

- Skills always live at `.claude/skills/<skill-name>/SKILL.md` inside this project — never in `~/.claude/skills/`
- No `scripts/`, `references/`, or `assets/` subdirectories are needed for these paper skills
- The skill description must be specific enough to trigger automatically when a co-author mentions the section name
