---
kernelspec:
  name: python3
  display_name: Python 3
  language: python
---

# Data Overview

```{code-cell} python3
:tags: [remove-cell]
import sys
from pathlib import Path

# Live dataset statistics; see paper/_stats.py. Never hardcode these numbers.
sys.path.insert(0, str(next(p for p in (Path("paper"), Path(".")) if (p / "_stats.py").exists())))
from _stats import STATS
```

The CNeuroMod databank comprises {eval}`STATS.n_datasets` datasets acquired across
{eval}`STATS.n_subjects` deeply-sampled participants (`sub-01`–`sub-06`), spanning
naturalistic movie and audiobook listening, videogame play, controlled cognitive
localizers and continuous-recognition paradigms.

## Summary Statistics

:::{figure} ../source_data/dataset_comparison/output_data/cneuromod_comparison_per_subject.png
:name: fig-cneuromod-volume
:width: 100%

**Per-subject data volume across CNeuroMod datasets.** Rows are individual datasets,
columns group recording modalities (fMRI, naturalistic stimuli, controlled-task
regressors, physiology, eye tracking), and bubble area is proportional to the hours of
unique per-subject content, excluding stimulus repetitions.
:::

The databank totals {eval}`STATS.fmri_total_h` hours of fMRI across all participants and
datasets, or {eval}`STATS.fmri_per_subject_h` hours per subject on average. Physiological
recordings accompany most fMRI sessions: {eval}`STATS.physiology_h()['ECG']` hours of ECG,
{eval}`STATS.physiology_h()['respiration']` hours of respiration,
{eval}`STATS.physiology_h()['plethysmograph']` hours of plethysmography and
{eval}`STATS.physiology_h()['electrodermal activity']` hours of electrodermal activity,
alongside {eval}`STATS.physiology_h()['eye tracking']` hours of eye tracking wherever the
in-scanner eye tracker was available.

Coverage is not uniform across the six participants. `sub-04` has the most limited
footprint, missing or partial in {eval}`len(STATS.datasets_for('sub-04'))` of the
{eval}`STATS.n_datasets` datasets, followed by `sub-05`
({eval}`len(STATS.datasets_for('sub-05'))` datasets) and `sub-06`
({eval}`len(STATS.datasets_for('sub-06'))` datasets); `sub-01` and `sub-03` each have a
single gap. Beyond per-subject availability, one dataset withholds content by design:
`friends` releases the stimuli for season 7 but keeps the corresponding fMRI responses
held out as an in-distribution test set for encoding-model benchmarks, including the
Algonauts Project 2025 Challenge.

## Dataset Coverage

### anat

The `anat` dataset comprises longitudinal anatomical and upper-spinal-cord MRI collected
at roughly four sessions per year to monitor structural stability over the course of the
study. Cortical flat maps and quantitative measures such as gray-matter morphometry,
tractography and myelination can be derived from the FreeSurfer derivatives it provides.

| | |
|---|---|
| **Subjects** | 6 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ✅ · `sub-05` ✅ · `sub-06` ✅ |

:::{admonition} How to cite
:class: tip

{cite:p}`Boudreau2025-ji`
:::

### emotion-videos

*(No overview text is yet available for this dataset — its `cneuromod.all` entry has not
been documented with a README.)*

| | |
|---|---|
| **Subjects** | 5 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ✅ · `sub-06` ✅ |
| **Tasks** | 📺 Silent emotion-evoking video clips — ~5.2 hours of naturalistic silent video watching per subject; clips are shared across subjects but not repeated within |
| **Data** | 🧠 fMRI — 5.2 h/subject |
|  | 🎬 Naturalistic video — 5.2 h/subject |
|  | 🫀 ECG — 5.2 h/subject |
|  | 🫁 Respiration — 5.2 h/subject |
|  | 🫀 Pulse — 5.2 h/subject |
|  | 😓 Skin conductance (EDA) — 5.2 h/subject |
|  | 👁️ Eye tracking — 5.2 h/subject |

### floc

Four participants (`sub-01`, `sub-02`, `sub-03`, `sub-05`) completed six sessions of a
functional localizer task designed to identify brain regions that respond preferentially
to specific stimulus categories, adapting the Stanford VPN lab's fLoc task
{cite:p}`St-Laurent2026-zc`.

| | |
|---|---|
| **Subjects** | 3 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ❌ · `sub-06` ❌ |
| **Tasks** | 👁️ Functional localizer — 5 visual categories (faces, bodies, places, objects, characters) — 6 sessions × 2 runs; rapid 12-trial blocks; one-back repetition detection task; 9 GLM contrasts; subject-specific ROIs for FFA, OFA, pSTS, PPA, OPA, MPA and EBA |
| **Data** | 🧠 fMRI — 0.8 h/subject |
|  | 📊 Controlled — 0.77 h/subject |
|  | 📐 Contrasts — 9 contrasts |

:::{admonition} How to cite
:class: tip

{cite:p}`St-Laurent2026-zc`
:::

### friends

This dataset contains fMRI data acquired while six CNeuroMod participants watched
episodes of the American sitcom *Friends* (seasons 1–7) in English, with brain responses
synchronized to visual frames, audio samples and time-stamped transcripts. It has served
as a benchmark corpus for multimodal movie-encoding challenges. [MISSING REF: Gifford et
al. (2025), "The Algonauts Project 2025 Challenge: How the Human Brain Makes Sense of
Multimodal Movies" — full bibliographic details (venue/DOI) needed]

| | |
|---|---|
| **Subjects** | 6 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` 🟡 _(seasons 1–4 only)_ · `sub-05` ✅ · `sub-06` ✅ |
| **Tasks** | 📺 Friends seasons 1–7 (~170 episodes) — ~65 hours of naturalistic movie watching per subject |
| **Data** | 🧠 fMRI — 61.9 h/subject |
|  | 🎬 Naturalistic video — 65.0 h/subject |
|  | 🔊 Audio — 65.0 h/subject |
|  | 🗣️ Speech listening — 65.0 h/subject |
|  | 🫀 ECG — 65 h/subject |
|  | 🫁 Respiration — 65 h/subject |
|  | 🫀 Pulse — 65 h/subject |
|  | 😓 Skin conductance (EDA) — 65 h/subject |
|  | 👁️ Eye tracking — 22 h/subject |

### gamepad

This dataset validates the CNeuroMod videogame controller, an open-source,
fiber-optic, MRI-compatible game controller designed by the project's engineering team
[MISSING REF: Harel, Y., Cyr, A., Boyle, J., Pinsard, B., Bernard, J., et al. (2023).
"Open design of a reproducible videogame controller for MRI and MEG." PLOS ONE, 18. doi:
10.1371/journal.pone.0290158], comparing it against a commercial SNES-like controller
across alternating mock-scanner and MRI sessions.

| | |
|---|---|
| **Subjects** | 4 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ❌ · `sub-06` ✅ |
| **Tasks** | 🎮 Cued-response button press — MRI controller validation — 4 MRI sessions × 2 runs per subject; participants pressed various controller buttons for short and long durations (5 blocs of 10 trials per condition); MRI-compatible controller compared against a commercial SNES-like controller across alternating mock-scanner sessions |
| **Data** | 🧠 fMRI — 0.7 h/subject |
|  | 📊 Controlled — 0.67 h/subject |
|  | 🕹️ Behavioural sessions (mock scanner) (button press events (.tsv) ✅) |
|  | 🫀 Physiology (ECG 🔒, respiration 🔒, plethysmograph 🔒, EDA 🔒) |
|  | 👁️ Eyetracking (gaze 🔒, pupillometry 🔒) |

### harrypotter

Five participants read Chapter 9 of *Harry Potter and the Sorcerer's Stone*, presented
word by word at 2 Hz across seven runs in a single session, using the same stimuli as the
separate fMRI dataset reported by Wehbe et al. (2014).

| | |
|---|---|
| **Subjects** | 5 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ✅ · `sub-06` ✅ |
| **Tasks** | 📖 Harry Potter and the Sorcerer's Stone — Chapter 9 — word-by-word text at 2 Hz; 7 runs × ~10 min; 1 session per participant |
| **Data** | 🧠 fMRI — 1.4 h/subject |
|  | 📖 Text reading — 1.4 h/subject |
|  | 🫀 ECG — 1.4 h/subject |
|  | 🫁 Respiration — 1.4 h/subject |
|  | 🫀 Pulse — 1.4 h/subject |
|  | 😓 Skin conductance (EDA) — 1.4 h/subject |
|  | 👁️ Eyetracking (gaze ❌, pupillometry ❌) |

:::{admonition} How to cite
:class: tip

{cite:p}`Toneva2022-bf`
:::

### hcptrt

Participants repeated the functional localizers developed by the Human Connectome
Project 15 times each, accumulating approximately 10 hours of functional data per
subject across seven tasks adapted from the HCP task-fMRI protocol
{cite:p}`Rastegarnia2023-qz`. Sessions typically combined either two repetitions of the
HCP localizers, or one resting-state run and one HCP localizer run.

| | |
|---|---|
| **Subjects** | 6 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ✅ · `sub-05` ✅ · `sub-06` ✅ |
| **Tasks** | 🎭 7 HCP task localizers (36 contrasts) — 13–18 repetitions per participant |
|  | 💤 resting state — 4–6 repetitions per participant |
| **Data** | 🧠 fMRI — 7.3 h/subject |
|  | 💤 Resting state — 1.25 h/subject |
|  | 📊 Controlled — 7.85 h/subject |
|  | 📐 Contrasts — 36 contrasts |
|  | 📈 Physiology (ECG ❌, pulse ❌, respiration ❌, skin conductance ❌) |
|  | 👁️ Eyetracking (Gaze ❌, pupillometry ❌) |

:::{admonition} How to cite
:class: tip

{cite:p}`Rastegarnia2023-qz`
:::

### hearing

*(No overview text is yet available for this dataset — its `cneuromod.all` entry has not
been documented with a README.)*

| | |
|---|---|
| **Subjects** | 6 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ✅ · `sub-05` ✅ · `sub-06` ✅ |

### langlocalizer

*(No overview text is yet available for this dataset — its `cneuromod.all` entry has not
been documented with a README.)*

| | |
|---|---|
| **Subjects** | 4 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ✅ · `sub-06` ❌ |
| **Data** | 🧠 fMRI — 1.1 h/subject |
|  | 📊 Controlled — 1.1 h/subject |
|  | 📐 Contrasts — 4 contrasts |

### mario

Five CNeuroMod participants played *Super Mario Bros.* (Nintendo, 1985) in-scanner across
22 of the game's original levels, in a structured discovery phase followed by a longer
practice phase of randomly selected levels {cite:p}`Paugam2025-oq`. Prior gameplay
experience varied across participants, from no videogame experience to regular
players who had already completed the game.

| | |
|---|---|
| **Subjects** | 5 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ✅ · `sub-06` ✅ |
| **Tasks** | 🎮 Super Mario Bros — in-scanner gameplay — 22 levels (excluding water and boss levels); discovery phase (all levels in order, unlimited attempts) then practice phase (random level per run); 3374 total level attempts across 5 participants; ~16.8 h fMRI per participant |
| **Data** | 🧠 fMRI — 18.4 h/subject |
|  | 🎬 Naturalistic video — 18.4 h/subject |
|  | 🔊 Audio — 18.4 h/subject |
|  | 🎮 Gameplay — 18.4 h/subject |
|  | 🫀 ECG — 18.4 h/subject |
|  | 🫁 Respiration — 18.4 h/subject |
|  | 🫀 Pulse — 18.4 h/subject |
|  | 😓 Skin conductance (EDA) — 18.4 h/subject |
|  | 🕹️ Game logs (annotated events (.tsv) ✅, game replay (.bk2) ✅, video replay (.mp4) ✅, replay summary (.json) ✅, mapped RAM variables (.json) ✅, low-level features (.npy) ✅, scene annotations ✅) |
|  | 👁️ Eyetracking (gaze 🔒, pupillometry 🔒) |

:::{admonition} How to cite
:class: tip

{cite:p}`Paugam2025-oq`
:::

### mario3

*(No overview text is yet available for this dataset — its `cneuromod.all` entry has not
been documented with a README.)*

| | |
|---|---|
| **Subjects** | 5 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ✅ · `sub-06` ✅ |
| **Data** | 🧠 fMRI — 9.9 h/subject |
|  | 🎬 Naturalistic video — 9.9 h/subject |
|  | 🔊 Audio — 9.9 h/subject |
|  | 🎮 Gameplay — 9.9 h/subject |

### mario_eeg

*(No overview text is yet available for this dataset — its `cneuromod.all` entry has not
been documented with a README.)*

| | |
|---|---|
| **Subjects** | 3 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ❌ · `sub-06` ❌ |

### mariostars

*(No overview text is yet available for this dataset — its `cneuromod.all` entry has not
been documented with a README.)*

| | |
|---|---|
| **Subjects** | 5 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ✅ · `sub-06` ✅ |
| **Data** | 🧠 fMRI — 6.9 h/subject |
|  | 🎬 Naturalistic video — 6.9 h/subject |
|  | 🔊 Audio — 6.9 h/subject |
|  | 🎮 Gameplay — 6.9 h/subject |

### movie10

Six participants watched four feature films — *The Bourne Supremacy*, *The Wolf of Wall
Street*, *Hidden Figures* (shown twice) and the BBC series *Life* (shown twice) — cut into
roughly ten-minute segments, for about 10 hours of functional data per participant.
[MISSING REF: Gifford et al. (2025), "The Algonauts Project 2025 Challenge" — full
bibliographic details needed]

| | |
|---|---|
| **Subjects** | 6 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ✅ · `sub-05` ✅ · `sub-06` ✅ |
| **Tasks** | 🎬 4 feature films (~7.3 h unique content) — The Bourne Supremacy, The Wolf of Wall Street, Hidden Figures, Life (BBC) |
| **Data** | 🧠 fMRI — 10.3 h/subject |
|  | 🎬 Naturalistic video — 7.3 h/subject |
|  | 🔊 Audio — 7.3 h/subject |
|  | 🗣️ Speech listening — 7.3 h/subject |
|  | 🫀 ECG — 10.0 h/subject |
|  | 🫁 Respiration — 10.0 h/subject |
|  | 🫀 Pulse — 10.0 h/subject |
|  | 😓 Skin conductance (EDA) — 10.0 h/subject |
|  | 👁️ Eyetracking (gaze ❌, pupillometry ❌) |

### multfs

*(No overview text is yet available for this dataset — its `cneuromod.all` entry has not
been documented with a README.)*

| | |
|---|---|
| **Subjects** | 5 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ✅ · `sub-06` ✅ |
| **Tasks** | 🧩 Visual working memory — combinatorial feature task — Continuously quizzed on visual feature combinations across varying difficulty levels (~10 repetitions per stimulus per subject); stimuli shared across subjects. Designed for RSA and brain encoding across a rich combinatorial task space. |
| **Data** | 🧠 fMRI — 8.8 h/subject |
|  | 📊 Controlled — 8.8 h/subject |

### mutemusic

*(No overview text is yet available for this dataset — its `cneuromod.all` entry has not
been documented with a README.)*

| | |
|---|---|
| **Subjects** | 5 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ✅ · `sub-06` ✅ |
| **Data** | 🧠 fMRI — 3.3 h/subject |
|  | 🔊 Audio — 1.1 h/subject |

### narratives

*(No overview text is yet available for this dataset — its `cneuromod.all` entry has not
been documented with a README.)*

| | |
|---|---|
| **Subjects** | 5 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ✅ · `sub-06` ✅ |
| **Data** | 🧠 fMRI — 9.7 h/subject |
|  | 🔊 Audio — 3.2 h/subject |
|  | 🗣️ Speech listening — 3.2 h/subject |

### ood

*(No overview text is yet available for this dataset — its `cneuromod.all` entry has not
been documented with a README.)*

| | |
|---|---|
| **Subjects** | 3 — `sub-01` ❌ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ✅ · `sub-06` ❌ |
| **Data** | 🧠 fMRI — 2.0 h/subject |
|  | 🎬 Naturalistic video — 2.0 h/subject |
|  | 🔊 Audio — 2.0 h/subject |
|  | 🗣️ Speech listening — 2.0 h/subject |

### petit-prince

*(No overview text is yet available for this dataset — its `cneuromod.all` entry has not
been documented with a README.)*

| | |
|---|---|
| **Subjects** | 5 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ✅ · `sub-06` ✅ |
| **Data** | 🧠 fMRI — 3.2 h/subject |
|  | 🔊 Audio — 1.1 h/subject |
|  | 🗣️ Speech listening — 1.1 h/subject |

### retinotopy

Four participants completed multiple sessions of a retinotopy task adapted from Kay et
al. (2013), designed to derive population receptive field properties at the voxel level
and to delineate regions of interest in early visual cortex {cite:p}`St-Laurent2026-zc`.
Each session comprised three runs using ring, bar and wedge apertures drawn from Human
Connectome Project retinotopy stimuli, with participants fixating centrally and
responding to a colour-change detection task.

| | |
|---|---|
| **Subjects** | 4 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ✅ · `sub-06` ❌ |
| **Tasks** | 👁️ Retinotopy — ring, bar and wedge apertures — 5–6 sessions × 3 runs; HCP retinotopy stimuli; fixation task with colour-change detection; pRF maps and 12 visual ROIs (V1–V3, hV4, VO1/2, LO1/2, TO1/2, V3a/b) |
| **Data** | 🧠 fMRI — 1.4 h/subject |
|  | 📊 Controlled — 1.4 h/subject |
|  | 📐 Contrasts — 12 contrasts |
|  | 👁️ Eyetracking (gaze ❌, pupillometry ❌) |

:::{admonition} How to cite
:class: tip

{cite:p}`St-Laurent2026-zc`
:::

### shinobi

Four CNeuroMod participants played *Shinobi III: Return of the Ninja Master* (Sega, 1993)
in-scanner across three levels selected for the relative homogeneity of their core
mechanics [MISSING REF: Harel, Y., Pinsard, B., Boyle, J., Borghesani, V., Le Clei, M., et
al. (2026). "Gamer in the scanner: Event-related analysis of fMRI activity during retro
videogame play guided by automated annotations of game content." doi:
10.1162/IMAG.a.1256]. Participants also completed behavioural-only at-home training
sessions before scanning, documented separately as the `shinobi/training` asset.

| | |
|---|---|
| **Subjects** | 4 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ❌ · `sub-04` ✅ _(11 sessions (vs 12 for other participants))_ · `sub-05` ❌ · `sub-06` ✅ _(~7 h fMRI (vs ~8 h for other participants))_ |
| **Tasks** | 🎮 Shinobi III: Return of the Ninja Master — in-scanner gameplay — 3 levels cycled (1, 4, 5); 4–5 runs × ~10 min per session; 11–12 sessions per participant; ~8 h fMRI per participant |
|  | 🏠 Shinobi III — at-home behavioral training (shinobi/training submodule) — Behavioral only; free-choice training regimen before scanner sessions; total gameplay per participant (training + in-scanner) exceeds fMRI acquisition time |
| **Data** | 🧠 fMRI — 10.4 h/subject |
|  | 🎬 Naturalistic video — 10.4 h/subject |
|  | 🔊 Audio — 10.4 h/subject |
|  | 🎮 Gameplay — 10.4 h/subject |
|  | 🫀 ECG — 8.0 h/subject |
|  | 🫁 Respiration — 8.0 h/subject |
|  | 🫀 Pulse — 8.0 h/subject |
|  | 😓 Skin conductance (EDA) — 8.0 h/subject |
|  | 🕹️ Game logs (annotated events (.tsv) ✅, game replay (.bk2) 🟡, video replay (.mp4) ✅, replay summary (.json) ✅, mapped RAM variables (.json) ✅, low-level features (.npy) ✅) |
|  | 👁️ Eyetracking (gaze ❌, pupillometry ❌) |

### things

Four participants completed 33–36 fMRI sessions of a continuous-recognition task with
images drawn from 720 categories of the THINGS dataset {cite:p}`St-Laurent2026-zc`. Each
run presented 60 trials with a 2.98 s image followed by a 1.49 s inter-stimulus interval,
while participants maintained central fixation; each image was seen three times across
sessions.

| | |
|---|---|
| **Subjects** | 4 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ _(ses-024–026 administered out of planned order)_ · `sub-04` ❌ · `sub-05` ❌ · `sub-06` ✅ _(3840 unique images (vs 4320); ses-019–026 administered out of planned order)_ |
| **Tasks** | 🖼️ Continuous visual recognition — 720 THINGS object categories — 33–36 sessions × up to 6 runs; ~4320 unique images; each image shown 3× across sessions; confidence rating on each trial |
| **Data** | 🧠 fMRI — 16.4 h/subject |
|  | 🖼️ Images — 4320 unique images/subject |
|  | 📊 Controlled — 16.4 h/subject |
|  | 📐 Contrasts — 1 contrasts |
|  | 📈 Physiology (ECG 🔒, respiration 🔒, pulse 🔒, skin conductance 🔒) |
|  | 👁️ Eyetracking (gaze ✅, pupillometry ✅) |

:::{admonition} How to cite
:class: tip

{cite:p}`St-Laurent2026-zc`
:::

### triplets

*(No overview text is yet available for this dataset — its `cneuromod.all` entry has not
been documented with a README.)*

| | |
|---|---|
| **Subjects** | 4 — `sub-01` ✅ · `sub-02` ✅ · `sub-03` ✅ · `sub-04` ❌ · `sub-05` ❌ · `sub-06` ✅ |
| **Tasks** | 🔺 Word triplets — semantic odd-one-out judgment — Single words shown in triplets; participants select the semantic odd one out. Each unique word shown ~3× per subject; stimuli shared across subjects. Designed for representational similarity analysis and brain encoding models. |
| **Data** | 🧠 fMRI — 7.8 h/subject |
|  | 📖 Text reading — 2.6 h/subject |

## Asset Coverage

| Asset | Datasets |
|---|---|
| 📁 BIDS | anat, emotion-videos, floc, friends, gamepad, harrypotter, hcptrt, hearing, langlocalizer, mario, mario3, mario_eeg, mariostars, movie10, multfs, mutemusic, narratives, ood, petit-prince, retinotopy, shinobi, things, triplets |
| 🧠 fMRIPrep | emotion-videos, floc, friends, gamepad, harrypotter, hcptrt, langlocalizer, mario, mario3, mariostars, movie10, multfs, mutemusic, narratives, ood, petit-prince, retinotopy, shinobi, things, triplets |
| 🫀 PhysPrep | emotion-videos, friends, harrypotter, mario, movie10, shinobi |
| timeseries | floc, friends, harrypotter, hcptrt, mario, mario3, mariostars, movie10, petit-prince, retinotopy, shinobi, things |
| 👁️ Population Receptive Field | retinotopy |
| 📍 floc ROIs | floc |
| 🗺️ Mario scenes | mario |
| 🏗️ sMRIPrep | anat |
| 🕹️ Shinobi training | shinobi |

### BIDS

All functional and anatomical data are organized following the
[Brain Imaging Data Structure (BIDS)](https://bids.neuroimaging.io/) specification.

### fMRIPrep

Functional data were preprocessed with [fMRIPrep](https://fmriprep.readthedocs.io/en/stable/installation.html),
a minimal-user-input pipeline that performs coregistration, normalization, unwarping,
noise-component extraction and skull-stripping, combining tools from FSL, ANTs,
FreeSurfer and AFNI. Slice-timing correction was disabled (fMRIPrep was invoked with
`--ignore slicetiming`).

### PhysPrep

Physiological recordings (PPG, ECG, EDA and respiration) were segmented, cleaned and
processed with [Physprep](https://github.com/courtois-neuromod/physprep), a pipeline
developed within the CNeuroMod project that integrates Phys2Bids, NeuroKit2 and Systole.

### timeseries

fMRI timeseries capturing local BOLD fluctuations were extracted from the fMRIPrep
derivatives with the
[`cneuromod_extract_tseries`](https://github.com/courtois-neuromod/cneuromod_extract_tseries)
library. Signal is standardized, detrended, smoothed, masked, vectorized and saved as 2D
arrays suitable for machine-learning pipelines.

### Population Receptive Field (retinotopy)

Voxel-wise population receptive fields were estimated with the
[analyzePRF](http://kendrickkay.net/analyzePRF/) MATLAB toolbox
(commit `a3ac908`, based on release 1.6) in MATLAB R2021a.

### floc ROIs (floc)

Subject-specific functional regions of interest were derived from the `floc` dataset
using a first-level GLM with Kanwisher-group parcels as spatial priors.

### Mario scenes (mario)

The 22 *Super Mario Bros.* levels used in `mario` are partitioned into 313 short scenes
(≈15 per level), each annotated with game-design pattern labels, forming the atomic unit
of analysis for behavioral and neural studies of gameplay.

### sMRIPrep (anat)

Anatomical data were preprocessed with [sMRIPrep](https://github.com/nipreps/smriprep),
which takes the T1w and T2w images from each participant's first two sessions and
averages them after coregistration.

### Shinobi training (shinobi)

`shinobi/training` contains behavioral-only at-home gameplay of *Shinobi III: Return of
the Ninja Master* for the same four participants as the `shinobi` neuroimaging dataset,
stored as a companion submodule.
