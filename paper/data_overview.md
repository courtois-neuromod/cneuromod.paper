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
localizers and continuous-recognition paradigms. After summary statistics, the datasets are
described one by one, grouped into the six cognitive categories of
{numref}`tab-cognitive-categories`.

## Summary Statistics

:::{figure} ../source_data/statistics/output_data/figure_cneuromod_comparison_per_subject.png
:name: fig-cneuromod-volume
:width: 100%

**Per-subject data volume across CNeuroMod datasets.** Rows are individual datasets, grouped
and colored by the six cognitive categories of {numref}`tab-cognitive-categories`. Columns
group brain recordings (fMRI), task content (images, video, audio, speech, text, resting
state, controlled tasks, videogames and contrasts) and physiology (ECG, respiration,
plethysmography, electrodermal activity, eye tracking). Bubble labels give hours of unique
per-subject content, excluding stimulus repetitions, or counts for images and contrasts;
bubble area grows with the logarithm of that value. A black outline marks the largest value
in each column.
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

## 🍿 Movies

### movie10

Six participants watched four feature films — *The Bourne Supremacy*, *The Wolf of Wall
Street*, *Hidden Figures* (shown twice) and the BBC series *Life* (shown twice) — cut into
roughly ten-minute segments, for about 10 hours of functional data per participant {cite:p}`gifford2025algonauts`.

### friends

This dataset contains fMRI data acquired while six CNeuroMod participants watched
episodes of the American sitcom *Friends* (seasons 1–7) in English, with brain responses
synchronized to visual frames, audio samples and time-stamped transcripts. It has served
as a benchmark corpus for multimodal movie-encoding challenges
{cite:p}`gifford2025algonauts`.

### ood

The `ood` dataset presents out-of-distribution audiovisual stimuli, held out to test the
generalization of brain encoding models trained on the other movie datasets.

*[TODO: dataset documentation pending — [cneuromod.all#60](https://github.com/courtois-neuromod/cneuromod.all/issues/60)]*

## 💬 Stories

### harrypotter

Five participants read Chapter 9 of *Harry Potter and the Sorcerer's Stone*, presented
word by word at 2 Hz across seven runs in a single session {cite:p}`Toneva2022-bf`,
using the same stimuli as the separate fMRI dataset reported by {cite:t}`wehbe2014`.

### petit-prince

Participants listened to the audiobook of Antoine de Saint-Exupéry's *Le Petit Prince*,
a story also used in the multilingual Le Petit Prince fMRI corpus {cite:p}`li2022petitprince`.

*[TODO: dataset documentation pending — [cneuromod.all#61](https://github.com/courtois-neuromod/cneuromod.all/issues/61)]*

### narratives

Participants listened to spoken narratives in the scanner, drawn from the Narratives
collection {cite:p}`nastase2021`.

*[TODO: dataset documentation pending — [cneuromod.all#62](https://github.com/courtois-neuromod/cneuromod.all/issues/62)]*

## 👾 Videogames

### shinobi

Four CNeuroMod participants played *Shinobi III: Return of the Ninja Master* (Sega, 1993)
in-scanner across three levels selected for the relative homogeneity of their core
mechanics {cite:p}`Harel2026-hr`. Participants also completed behavioural-only at-home training
sessions before scanning, documented separately as the `shinobi/training` asset.

### mario

Five CNeuroMod participants played *Super Mario Bros.* (Nintendo, 1985) in-scanner across
22 of the game's original levels, in a structured discovery phase followed by a longer
practice phase of randomly selected levels {cite:p}`Paugam2025-oq`. Prior gameplay
experience varied across participants, from no videogame experience to regular
players who had already completed the game.

### mariostars

Participants played, in-scanner, the *Super Mario All-Stars* remake of the original
*Super Mario Bros.* levels.

*[TODO: dataset documentation pending — [cneuromod.all#63](https://github.com/courtois-neuromod/cneuromod.all/issues/63)]*

### mario3

Participants played *Super Mario Bros. 3* in-scanner, with frame-accurate replay files
recorded for every play.

*[TODO: dataset documentation pending — [cneuromod.all#64](https://github.com/courtois-neuromod/cneuromod.all/issues/64)]*

### mario_eeg

Electroencephalography was recorded outside the scanner while participants played
*Super Mario Bros.*

*[TODO: dataset documentation pending — [cneuromod.all#65](https://github.com/courtois-neuromod/cneuromod.all/issues/65)]*

## 🔬 Taskscapes

### triplets

Participants viewed word triplets and picked the semantic odd one out.

*[TODO: dataset documentation pending — [cneuromod.all#66](https://github.com/courtois-neuromod/cneuromod.all/issues/66)]*

### things

Four participants completed 33–36 fMRI sessions of a continuous-recognition task with
images drawn from 720 categories of the THINGS dataset {cite:p}`St-Laurent2026-zc`. Each
run presented 60 trials with a 2.98 s image followed by a 1.49 s inter-stimulus interval,
while participants maintained central fixation; each image was seen three times across
sessions.

### emotion-videos

Five participants (`sub-01`, `sub-02`, `sub-03`, `sub-05`, `sub-06`) watched 1,888 short
silent video clips from the database of {cite:t}`cowen2017`, which evoke a broad range of
affective states and were normed by an independent sample on 34 emotion categories and 14
affective dimensions (no ratings were collected from CNeuroMod participants). Of the 2,185
clips in the database, those longer than 20 s and those with extreme content (e.g.
pornography, murder, animal abuse) were discarded. Each clip was shown once, over 36 runs of
8 min 20 s spread across six to seven sessions, with 45 to 65 clips per run separated by a
jittered inter-trial interval of 3 to 6 s. Participants were only asked to keep their eyes
open and fixate a marker shown before each clip, which also served for eye-tracking drift
correction. Clip order within a run was shared across participants, while run order was
randomized per participant. Cardiac, respiratory and electrodermal signals and eye-tracking
were recorded throughout.

### multfs

A visual working-memory task quizzed participants on combinations of stimulus features
across a range of difficulty levels.

*[TODO: dataset documentation pending — [cneuromod.all#68](https://github.com/courtois-neuromod/cneuromod.all/issues/68)]*

### mutemusic

Five participants (`sub-01`, `sub-02`, `sub-03`, `sub-05`, `sub-06`) listened to familiar
and unfamiliar music tracks in which parts of the audio had been replaced by silence, and
imagined the continuation of the music during the silent gaps, a paradigm adapted from
{cite:t}`kraemer2005` {cite:p}`Freteault2025-bp`. From a pool of 75 tracks spanning three
categories (songs with lyrics, orchestral music, and video game music, partly drawn from
the games played in `mario` and `shinobi`), each participant heard 60 tracks, half rated
familiar and half unfamiliar during a pre-scan assessment. Each track excerpt (45 s to
1 min 15 s) included two to four silences of 4–6 s, and each of the six ten-track playlists
was presented three times. After each track, participants rated the vividness of their
imagery on a five-point scale, and they completed questionnaires on auditory imagery and
musical sophistication.

## 🧭 Functional localizers

### langlocalizer

A language localizer contrasted sentences with degraded controls to map
language-selective cortex.

*[TODO: dataset documentation pending — [cneuromod.all#70](https://github.com/courtois-neuromod/cneuromod.all/issues/70)]*

### floc

Four participants (`sub-01`, `sub-02`, `sub-03`, `sub-05`) completed six sessions of a
functional localizer task designed to identify brain regions that respond preferentially
to specific stimulus categories, adapting the Stanford VPN lab's fLoc task
{cite:p}`stigliani2015,St-Laurent2026-zc`.

### retinotopy

Four participants completed multiple sessions of a retinotopy task adapted from
{cite:t}`kay2013`, designed to derive population receptive field properties at the voxel level
and to delineate regions of interest in early visual cortex {cite:p}`St-Laurent2026-zc`.
Each session comprised three runs using ring, bar and wedge apertures drawn from Human
Connectome Project retinotopy stimuli, with participants fixating centrally and
responding to a colour-change detection task.

### hcptrt

Participants repeated the functional localizers developed by the Human Connectome
Project 15 times each, accumulating approximately 10 hours of functional data per
subject across seven tasks adapted from the HCP task-fMRI protocol
{cite:p}`barch2013,Rastegarnia2023-qz`. Sessions typically combined either two repetitions of the
HCP localizers, or one resting-state run and one HCP localizer run.

## 🧰 Others

### hearing

The `hearing` dataset tracks the auditory health of all six participants under repeated
exposure to scanner noise {cite:p}`Fortier2025-bo`. After baseline tests in early 2021,
clinical audiology tests were administered immediately before and after scanning
sessions, to detect temporary changes, and two to seven days after a session, to detect
lasting ones. Tests covered otoscopy, tympanometry, stapedial reflexes, pure-tone
audiometry over the standard (0.25–8 kHz) and extended high-frequency (9–20 kHz) ranges,
and distortion product otoacoustic emissions, a subclinical marker that can precede
measurable threshold shifts.

### anat

The `anat` dataset comprises longitudinal anatomical and upper-spinal-cord MRI collected
at roughly four sessions per year to monitor structural stability over the course of the
study {cite:p}`Boudreau2025-ji`. Cortical flat maps and quantitative measures such as gray-matter morphometry,
tractography and myelination can be derived from the FreeSurfer derivatives it provides.

### gamepad

This dataset validates the CNeuroMod videogame controller, an open-source,
fiber-optic, MRI-compatible game controller designed by the project's engineering team
{cite:p}`Harel2023-gp`, comparing it against a commercial SNES-like controller
across alternating mock-scanner and MRI sessions.
