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

For example, the `friends` dataset (participants watching the sitcom *Friends*) exposes `friends/bids` (raw data), `friends/fmriprep` and `friends/mriqc` (preprocessing and quality-control derivatives), and `friends/physprep` (processed physiological recordings). Dataset-specific submodules follow the same convention — e.g. `shinobi/training` for behavioural logs, or `things/glm` and `things/glmsingle` for first-level model estimates. A full description of what each dataset contains is given in [Data Overview](data_overview.md).

## BIDS compliance

All functional and anatomical neuroimaging data are formatted according to the [Brain Imaging Data Structure (BIDS)](https://bids.neuroimaging.io/) specification. Deviations from the core specification are:

- Multi-contrast anatomical sequences follow [BEP001](https://bids.neuroimaging.io/bep001).
- Spinal cord images use the Body Part tag proposed in [BEP025](https://bids.neuroimaging.io/bep025) (`bp-cspine`) to distinguish them from brain anatomical images acquired with the same contrasts.

Session indices (`ses-001`, `ses-002`, …) reflect the order of data acquisition; the number of runs, tasks, and their order within a session vary across participants. A small number of session indices are skipped where an entire session was discarded for scanning issues.

All images covering the face — collected as part of the longitudinal anatomical protocol (`anat/bids`) — were anonymised by zeroing the face, teeth, and ear regions with a custom mask warped from MNI space.

## Preprocessing derivatives

### fMRIPrep

Functional data were preprocessed using fMRIPrep 20.2.5 [MISSING REF: Esteban, O. et al. (2019). "fMRIPrep: a robust preprocessing pipeline for functional MRI." Nature Methods, 16, 111–116. doi: 10.1038/s41592-018-0235-4 — add to references.bib] via an anatomical fast-track using sMRIPrep output (`--anat-derivatives`), ensuring a consistent anatomical basis across all functional datasets. The `--ignore slicetiming` flag was used. Outputs are provided in three spaces: native T1w, volumetric MNI152NLin2009cAsym, and surface-based fsLR-den-91k (grayordinates). Each functional run yields:

- `*_desc-preproc_bold.nii.gz` — preprocessed BOLD timeseries
- `*_boldref.nii.gz` — single-volume BOLD reference
- `*_desc-brain_mask.nii.gz` — brain mask
- `*_desc-confounds_timeseries.tsv` — confound regressors (motion parameters, CompCor components, global signals, framewise displacement, DVARS)

### sMRIPrep / FreeSurfer

Anatomical processing used sMRIPrep and FreeSurfer in both cross-sectional and longitudinal modes, providing cortical surface reconstructions, segmentations, and subject-specific atlases. Cortical flat maps are available via PyCortex surfaces (`anat/pycortex`).

### PhysPrep

Physiological signals were preprocessed using the CNeuroMod PhysPrep pipeline [MISSING REF: PhysPrep — github.com/courtois-neuromod/physprep — add citation to references.bib], integrating Phys2Bids, NeuroKit2, and Systole. Outputs per run include:

- `*_physio.tsv.gz` / `*_physio.json` — raw segmented biosignals (in `<dataset>/bids`)
- `*_desc-preproc_physio.tsv.gz` — filtered and cleaned timeseries
- `*_desc-physio_events.tsv` — sparse extracted features (peaks, troughs, SCRs)
- `*_desc-quality.json` — run-level quality assessment (pass/fail per modality)

## Data access and versioning

Five of the six participants have consented to fully open sharing; access to the
complete databank requires a registered-access data transfer agreement. `cneuromod.all`
uses yearly release tags to pin a specific state of all submodule pointers, enabling
exact reproduction of prior analyses. See [Data Availability](data_availability.md) for
deposit locations, license terms, access procedure, and download instructions.
