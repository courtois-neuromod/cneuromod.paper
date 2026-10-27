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

### Dataset maturity

Datasets are released at different stages, so each carries a maturity rating, maintained
by hand in its `dataset_info.yaml`. A *validation paper* is a dedicated paper testing that
the dataset carries its intended signal; the common quality metrics alone do not count.
*Substantial reuse* means at least three papers using the dataset. The ladder has four
levels: 🏆 Reference datasets have a validation paper and substantial reuse; 🟢 Stable
datasets have one or the other; 🟡 Beta datasets are complete (all planned participants
released, fMRIPrep derivatives, README) but neither validated nor substantially reused yet;
🟠 Alpha datasets fall short of that, being not fully acquired or released, or missing a
README. At the time of writing, {eval}`STATS.n_at('reference', 'stable')` of the
{eval}`STATS.n_datasets` datasets are rated Stable or Reference, {eval}`STATS.n_at('beta')`
Beta and {eval}`STATS.n_at('alpha')` Alpha. Each dataset's rating is shown beneath its name
below.

| Level | Datasets |
|---|---|
| 🏆 Reference | {eval}`', '.join(STATS.datasets_at('reference'))` |
| 🟢 Stable | {eval}`', '.join(STATS.datasets_at('stable'))` |
| 🟡 Beta | {eval}`', '.join(STATS.datasets_at('beta'))` |
| 🟠 Alpha | {eval}`', '.join(STATS.datasets_at('alpha'))` |

## 🍿 Movies

### movie10

*Maturity:* {eval}`STATS.maturity_badge('movie10')`

Six participants watched four feature films — *The Bourne Supremacy*, *The Wolf of Wall
Street*, *Hidden Figures* (shown twice) and the BBC series *Life* (shown twice) — cut into
roughly ten-minute segments, for about 10 hours of functional data per participant {cite:p}`gifford2025algonauts`.

### friends

*Maturity:* {eval}`STATS.maturity_badge('friends')`

This dataset contains fMRI data acquired while six CNeuroMod participants watched
episodes of the American sitcom *Friends* (seasons 1–7) in English, with brain responses
synchronized to visual frames, audio samples and time-stamped transcripts. It has served
as a benchmark corpus for multimodal movie-encoding challenges
{cite:p}`gifford2025algonauts`.

### ood

*Maturity:* {eval}`STATS.maturity_badge('ood')`

The `ood` dataset presents out-of-distribution audiovisual stimuli, held out to test the
generalization of brain encoding models trained on the other movie datasets.

*[TODO: dataset documentation pending — [cneuromod.all#60](https://github.com/courtois-neuromod/cneuromod.all/issues/60)]*

## 💬 Stories

### harrypotter

*Maturity:* {eval}`STATS.maturity_badge('harrypotter')`

Five participants read Chapter 9 of *Harry Potter and the Sorcerer's Stone*, presented
word by word at 2 Hz across seven runs in a single session {cite:p}`Toneva2022-bf`,
using the same stimuli as the separate fMRI dataset reported by {cite:t}`wehbe2014`.

### petit-prince

*Maturity:* {eval}`STATS.maturity_badge('petit-prince')`

Participants listened to the audiobook of Antoine de Saint-Exupéry's *Le Petit Prince*,
a story also used in the multilingual Le Petit Prince fMRI corpus {cite:p}`li2022petitprince`.

*[TODO: dataset documentation pending — [cneuromod.all#61](https://github.com/courtois-neuromod/cneuromod.all/issues/61)]*

### narratives

*Maturity:* {eval}`STATS.maturity_badge('narratives')`

Participants listened to spoken narratives in the scanner, drawn from the Narratives
collection {cite:p}`nastase2021`.

*[TODO: dataset documentation pending — [cneuromod.all#62](https://github.com/courtois-neuromod/cneuromod.all/issues/62)]*

## 👾 Videogames

### shinobi

*Maturity:* {eval}`STATS.maturity_badge('shinobi')`

Four CNeuroMod participants played *Shinobi III: Return of the Ninja Master* (Sega, 1993)
in-scanner across three levels selected for the relative homogeneity of their core
mechanics {cite:p}`Harel2026-hr`. Participants also completed behavioural-only at-home training
sessions before scanning, documented separately as the `shinobi/training` asset.

### mario

*Maturity:* {eval}`STATS.maturity_badge('mario')`

Five CNeuroMod participants played *Super Mario Bros.* (Nintendo, 1985) in-scanner across
22 of the game's original levels, in a structured discovery phase followed by a longer
practice phase of randomly selected levels {cite:p}`Paugam2025-oq`. Prior gameplay
experience varied across participants, from no videogame experience to regular
players who had already completed the game.

### mariostars

*Maturity:* {eval}`STATS.maturity_badge('mariostars')`

After completing `mario`, the same five participants played in-scanner the *Super Mario Bros.*
remake included in *Super Mario All-Stars* (Nintendo, 1993), on the same 22 levels. Level
layouts, enemies and items are essentially unchanged, while graphics and sound are entirely
redone for the Super Nintendo, so the dataset tests how brain and behavioural models generalize
across visual and auditory renderings of the same game. There is no discovery phase: all
sessions follow the `mario` practice design, with levels in pseudo-random order. Part of the
fMRI data is withheld as the test set of the Algonauts Project 2027 Challenge, and will be
released once the challenge ends.

### mario3

*Maturity:* {eval}`STATS.maturity_badge('mario3')`

After `mario` and `mariostars`, the same five participants played *Super Mario Bros. 3*
(Nintendo, 1988) in-scanner across 80 levels of the game's eight worlds, including fortresses
and airships with their boss fights. As in `mario`, a discovery phase (each level once, in game
order) was followed by a practice phase of levels in pseudo-random order. The game keeps the
character and core controls of `mario` but adds new mechanics, such as suits with new abilities,
P-Switches and auto-scrolling levels, as well as longer and more varied levels, so the dataset
tests how models generalize to new game mechanics. Unlike `mario` and `mariostars`, each life
is stored as its own replay file. Part of the fMRI data is withheld as the test set of the
Algonauts Project 2027 Challenge, and will be released once the challenge ends.

### mario_eeg

*Maturity:* {eval}`STATS.maturity_badge('mario_eeg')`

Electroencephalography was recorded outside the scanner while participants played
*Super Mario Bros.*

*[TODO: dataset documentation pending — [cneuromod.all#65](https://github.com/courtois-neuromod/cneuromod.all/issues/65)]*

## 🔬 Taskscapes

### triplets

*Maturity:* {eval}`STATS.maturity_badge('triplets')`

Participants viewed word triplets and picked the semantic odd one out.

*[TODO: dataset documentation pending — [cneuromod.all#66](https://github.com/courtois-neuromod/cneuromod.all/issues/66)]*

### things

*Maturity:* {eval}`STATS.maturity_badge('things')`

Four participants completed 33–36 fMRI sessions of a continuous-recognition task with
images drawn from 720 categories of the THINGS dataset {cite:p}`St-Laurent2026-zc`. Each
run presented 60 trials with a 2.98 s image followed by a 1.49 s inter-stimulus interval,
while participants maintained central fixation; each image was seen three times across
sessions.

### emotion-videos

*Maturity:* {eval}`STATS.maturity_badge('emotion-videos')`

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

*Maturity:* {eval}`STATS.maturity_badge('multfs')`

Five participants (`sub-01`, `sub-02`, `sub-03`, `sub-05`, `sub-06`) performed 12 structured
visual working-memory tasks over 16 scanning sessions, after one behavioural training session.
The stimuli are eight photorealistic renderings of 3D models, crossing two object categories
(faces and buses), two identities per category and two viewpoints, each shown at one of two
screen locations. The tasks apply a small set of working-memory operations to location,
category or identity: a delayed match-to-sample task on location, run in every session as a
reference for session-to-session variability; three 1-back tasks; two contextual
decision-making tasks, in which the outcome of a first comparison selects the feature used for
a second one; and six interleaved delayed match-to-sample tasks, crossing two interleaving
patterns (ABAB, ABBA) with the three features. Each stimulus lasts one TR (1.49 s), and each
session comprises seven runs. Every ordered pair of consecutive stimuli occurs at least five
times per participant (1,808 trials in total), yielding more than 400 distinct task conditions
(task rule crossed with a single stimulus or a pair of consecutive stimuli), each with at least
five correct-trial repetitions. This factorial design dissociates task rule, stimulus content and
their interaction, for representational similarity analysis, brain encoding and generalization
across tasks and individuals. Accuracy was high for the 1-back (94.6%) and interleaved
(93.3%) tasks and lower for contextual decision-making (77.8%). Cardiac, respiratory and
electrodermal signals and eye-tracking were recorded throughout.

### mutemusic

*Maturity:* {eval}`STATS.maturity_badge('mutemusic')`

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

*Maturity:* {eval}`STATS.maturity_badge('langlocalizer')`

Four participants (`sub-01`, `sub-02`, `sub-03`, `sub-05`), all right-handed and fluent in
English and French (two native speakers of each), completed three sessions of standard
language localizers from the Fedorenko lab, one week apart. Each session comprised two runs of
each of four block-design tasks, interleaved with other CNeuroMod tasks: reading English
sentences versus non-word sequences {cite:p}`fedorenko2010`; listening to English passages
versus acoustically degraded versions of the same passages {cite:p}`scott2016`; and two
versions of the *Alice in Wonderland* localizer, in English and in French, contrasting intact
passages with degraded passages and passages in an unfamiliar language (Tamil)
{cite:p}`malikmoraleda2022`. Crossing modality (reading versus listening) and language
(English versus French) within the same individuals, with three repetitions of the full
protocol, separates differences in the topography of the language network between
participants from variability within a participant across sessions, modalities and
languages. Subject-specific language regions of interest derived from these data will be
distributed with the atlases in `anat`.

### floc

*Maturity:* {eval}`STATS.maturity_badge('floc')`

Four participants (`sub-01`, `sub-02`, `sub-03`, `sub-05`) completed six sessions of a
functional localizer task designed to identify brain regions that respond preferentially
to specific stimulus categories, adapting the Stanford VPN lab's fLoc task
{cite:p}`stigliani2015,St-Laurent2026-zc`.

### retinotopy

*Maturity:* {eval}`STATS.maturity_badge('retinotopy')`

Four participants completed multiple sessions of a retinotopy task adapted from
{cite:t}`kay2013`, designed to derive population receptive field properties at the voxel level
and to delineate regions of interest in early visual cortex {cite:p}`St-Laurent2026-zc`.
Each session comprised three runs using ring, bar and wedge apertures drawn from Human
Connectome Project retinotopy stimuli, with participants fixating centrally and
responding to a colour-change detection task.

### hcptrt

*Maturity:* {eval}`STATS.maturity_badge('hcptrt')`

Participants repeated the functional localizers developed by the Human Connectome
Project 15 times each, accumulating approximately 10 hours of functional data per
subject across seven tasks adapted from the HCP task-fMRI protocol
{cite:p}`barch2013,Rastegarnia2023-qz`. Sessions typically combined either two repetitions of the
HCP localizers, or one resting-state run and one HCP localizer run.

## 🧰 Others

### hearing

*Maturity:* {eval}`STATS.maturity_badge('hearing')`

All six participants underwent clinical audiology tests over about 1.5 years, run by a trained
audiologist, to check that repeated scanning with hearing protection did not damage their
hearing {cite:p}`Fortier2025-bo`. After baseline tests in January–February 2021, hearing was
measured immediately before and after a scan session, to capture temporary threshold shifts,
and again two to seven days later, to capture lasting changes against baseline. Each session
started with a check of the outer and middle ear, followed by tympanometry, ipsilateral
stapedial reflexes, pure-tone audiometry over the standard (0.25–8 kHz) and extended
high-frequency (9–20 kHz) ranges, distortion product otoacoustic emissions and their growth
function, transient-evoked otoacoustic emissions, and a matrix speech-in-noise test in French
and English. Otoacoustic emissions probe outer hair cell function and can reveal subclinical
changes before thresholds shift. The number of hearing sessions ranges from 4 (`sub-04`, who
suspended scanning during the protocol) to 18 (`sub-05`, who has a pre-existing hearing
impairment and was followed with an intensive five-week audiometry protocol). The data are
behavioural only, stored as one BIDS-like task per test.

### anat

*Maturity:* {eval}`STATS.maturity_badge('anat')`

The `anat` dataset comprises longitudinal anatomical and upper-spinal-cord MRI collected
at roughly four sessions per year to monitor structural stability over the course of the
study {cite:p}`Boudreau2025-ji`. Cortical flat maps and quantitative measures such as gray-matter morphometry,
tractography and myelination can be derived from the FreeSurfer derivatives it provides.

### gamepad

*Maturity:* {eval}`STATS.maturity_badge('gamepad')`

This dataset validates the CNeuroMod videogame controller, an open-source,
fiber-optic, MRI-compatible game controller designed by the project's engineering team
{cite:p}`Harel2023-gp`, comparing it against a commercial SNES-like controller
across alternating mock-scanner and MRI sessions.
