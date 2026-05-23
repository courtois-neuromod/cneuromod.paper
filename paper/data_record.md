# Data Record

All CNeuroMod data are distributed as [DataLad](https://www.datalad.org/) repositories hosted on GitHub under the [courtois-neuromod](https://github.com/courtois-neuromod) organisation. The master meta-repository, `cneuromod.all`, tracks all datasets and their derivatives as git submodules following [YODA principles](https://handbook.datalad.org/en/latest/basics/101-127-yoda.html). Full technical documentation is available at [docs.cneuromod.ca](https://docs.cneuromod.ca). Data are released under a [CC0 license](https://creativecommons.org/publicdomain/zero/1.0/legalcode).

## Repository structure

`cneuromod.all` is a DataLad YODA meta-repository comprising 43 git submodules. Each experimental paradigm occupies a top-level folder (e.g., `friends/`, `hcptrt/`, `anat/`), which in turn contains independent submodules for each data component:

| Submodule suffix | Contents |
|---|---|
| `<dataset>/bids` | Raw BIDS data |
| `<dataset>/fmriprep` | fMRIPrep preprocessing derivatives |
| `<dataset>/mriqc` | MRIQC quality-control reports |
| `<dataset>/physprep` | Physiological preprocessing derivatives |
| `<dataset>/<other>` | Dataset-specific additional content |

Most data files are git-annex symlinks and must be explicitly retrieved with `datalad get`. Cloning the meta-repository fetches only metadata (git history, file pointers); data files are downloaded on demand. Recursive installation of submodules should be avoided, as submodules re-expose their own sub-submodules at differing versions for provenance tracking.

## BIDS compliance

All functional and anatomical neuroimaging data are formatted according to the [Brain Imaging Data Structure (BIDS)](https://bids.neuroimaging.io/) specification. Deviations from the core specification are:

- Multi-contrast anatomical sequences follow [BEP001](https://bids.neuroimaging.io/bep001).
- Spinal cord images use the Body Part tag proposed in [BEP025](https://bids.neuroimaging.io/bep025) (`bp-cspine`) to distinguish them from brain anatomical images acquired with the same contrasts.

Session indices (`ses-001`, `ses-002`, …) reflect the order of data acquisition; the number of runs, tasks, and their order within a session vary across participants. A small number of session indices are skipped where an entire session was discarded for scanning issues.

## Anatomical data (`anat/`)

The anatomical dataset contains longitudinal brain and spinal cord MRI collected at approximately four sessions per year across the full duration of the project. All images covering the face were anonymised by zeroing the face, teeth, and ear regions with a custom mask warped from MNI space.

**Submodules:** `anat/bids` (raw), `anat/smriprep`, `anat/smriprep.longitudinal`, `anat/freesurfer`, `anat/freesurfer.longitudinal`, `anat/atlases`, `anat/pycortex`.

## Functional datasets

### friends (~65 h/subject, N = 6)

Participants watched all seven seasons of the American sitcom *Friends* in English. Each episode is split into two scanning segments (a/b). The BIDS `task` entity encodes season, episode, and segment (e.g., `task-s01e01a`). Season 7 fMRI responses are withheld as a held-out test set for the [Algonauts Project 2025 Challenge](https://algonautsproject.com/). Physiological recordings (ECG, respiration, plethysmograph, EDA) accompany all runs. **Submodules:** `friends/bids`, `friends/fmriprep`, `friends/mriqc`, `friends/physprep`.

### hcptrt (~9 h/subject, N = 6)

Participants completed 13–18 repetitions of the seven Human Connectome Project (HCP) task-fMRI localizers, yielding 36 standard GLM contrasts, plus 4–6 resting-state runs per subject. Stimuli and E-Prime scripts are adapted from the HCP and available at the [HCP database](https://db.humanconnectome.org). **Submodules:** `hcptrt/bids`, `hcptrt/fmriprep`.

### movie10 (~10 h/subject, N = 6)

Participants watched four feature films (*The Bourne Supremacy*, *The Wolf of Wall Street*, *Life*, and *Hidden Figures*), each cut into approximately 10-minute segments. Physiological recordings accompany all runs. **Submodules:** `movie10/bids`, `movie10/fmriprep`, `movie10/mriqc`, `movie10/physprep`.

### mario (~17 h/subject, N = 5)

Participants played *Super Mario Bros.* (Nintendo, 1985) across 22 levels in a structured discovery phase followed by a randomised practice phase. Physiological recordings accompany all runs. **Submodules:** `mario/bids`, `mario/fmriprep`, `mario/physprep`.

### shinobi (~8 h/subject, N = 4)

Participants played *Shinobi III: Return of the Ninja Master* (Sega, 1993) in two phases. Physiological recordings accompany all runs. Training-session behavioural data are available in `shinobi/training`. **Submodules:** `shinobi/bids`, `shinobi/fmriprep`, `shinobi/mriqc`, `shinobi/physprep`, `shinobi/training`.

### things (~16 h/subject, N = 4)

Participants completed a continuous visual recognition task with images drawn from the [THINGS](https://things-initiative.org/) object database (~4320 unique images per participant from 720 categories; each image presented 3× across sessions). GLM and GLMsingle first-level estimates are provided as derivatives. **Submodules:** `things/bids`, `things/fmriprep`, `things/mriqc`, `things/behaviour`, `things/glm`, `things/glmsingle`.

### harrypotter (~1.2 h/subject, N = 5)

Participants read chapter 9 of *Harry Potter and the Sorcerer's Stone* word-by-word at 2 Hz across 7 runs. Stimuli are adapted from {cite:p}`wehbe2014`. Physiological recordings accompany all runs. **Submodules:** `harrypotter/bids`, `harrypotter/fmriprep`, `harrypotter/physprep`.

### floc (~0.8 h/subject, N = 4)

A functional localizer task (adapted from the [Stanford VPN lab fLoc](https://doi.org/10.1523/JNEUROSCI.4822-14.2015)) identifying brain regions selective for five visual categories (faces, bodies, places, objects, characters) across 6 sessions × 2 runs. Nine GLM contrasts and subject-specific ROIs (FFA, OFA, pSTS, PPA, OPA, MPA, EBA) are provided. **Submodules:** `floc/bids`, `floc/fmriprep`, `floc/mriqc`, `floc/rois`.

### retinotopy (~1.4 h/subject, N = 4)

A retinotopy task (adapted from {cite:p}`kay2013`) using ring, bar, and wedge apertures across 5–6 sessions × 3 runs to derive population receptive field (pRF) maps and delineate 12 visual ROIs (V1–V3, hV4, VO1/2, LO1/2, TO1/2, V3a/b). **Submodules:** `retinotopy/bids`, `retinotopy/fmriprep`, `retinotopy/prf`.

### gamepad (~0.7 h/subject, N = 4)

A cued-response button-press task validating the CNeuroMod MRI-compatible fiber-optic gamepad {cite:p}`harel2023`. **Submodule:** `gamepad/bids`, `gamepad/fmriprep`.

## Preprocessing derivatives

### fMRIPrep

Functional data were preprocessed using fMRIPrep 20.2.5 {cite:p}`esteban2019` via an anatomical fast-track using sMRIPrep output (`--anat-derivatives`), ensuring a consistent anatomical basis across all functional datasets. The `--ignore slicetiming` flag was used. Outputs are provided in three spaces: native T1w, volumetric MNI152NLin2009cAsym, and surface-based fsLR-den-91k (grayordinates). Each functional run yields:

- `*_desc-preproc_bold.nii.gz` — preprocessed BOLD timeseries
- `*_boldref.nii.gz` — single-volume BOLD reference
- `*_desc-brain_mask.nii.gz` — brain mask
- `*_desc-confounds_timeseries.tsv` — confound regressors (motion parameters, CompCor components, global signals, framewise displacement, DVARS)

### sMRIPrep / FreeSurfer

Anatomical processing used sMRIPrep and FreeSurfer in both cross-sectional and longitudinal modes, providing cortical surface reconstructions, segmentations, and subject-specific atlases. Cortical flat maps are available via PyCortex surfaces (`anat/pycortex`).

### PhysPrep

Physiological signals were preprocessed using the CNeuroMod PhysPrep pipeline {cite:p}`physprep`, integrating Phys2Bids, NeuroKit2, and Systole. Outputs per run include:

- `*_physio.tsv.gz` / `*_physio.json` — raw segmented biosignals (in `<dataset>/bids`)
- `*_desc-preproc_physio.tsv.gz` — filtered and cleaned timeseries
- `*_desc-physio_events.tsv` — sparse extracted features (peaks, troughs, SCRs)
- `*_desc-quality.json` — run-level quality assessment (pass/fail per modality)

## Data access

Five of the six participants (`sub-01`, `sub-02`, `sub-03`, `sub-05`, `sub-06`) have consented to fully open sharing via the [Canadian Open Neuroscience Platform (CONP)](https://portal.conp.ca/dataset?id=projects/cneuromod). Access to all six participants requires a registered-access data transfer agreement (DTA), obtainable via [cneuromod.ca/access](https://www.cneuromod.ca/access/access/). Approved researchers receive S3 credentials for download. Full download instructions are available at [docs.cneuromod.ca](https://docs.cneuromod.ca).

## Versioning

`cneuromod.all` uses yearly release tags (e.g., `git checkout 2020`) to pin a specific state of all submodule pointers, enabling exact reproduction of prior analyses. Updates to an existing clone can be obtained with `datalad update -r --merge --reobtain-data`.
