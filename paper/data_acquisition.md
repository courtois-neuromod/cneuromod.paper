# Data Acquisition

## Participants

Six healthy adults (3 women, ages 31–47 at recruitment in 2018) consented to participate in the Courtois NeuroMod project for a minimum of five years. All participants reported normal hearing and vision for their age and were MRI compatible. Specific demographics for each participant are provided in [DATA RECORD TABLE]. Participants were scanned one to two times per week, except during personal holidays, illness, or periods of scanner unavailability. All procedures were approved by the ethics board of the CIUSSS du Centre-Sud-de-l'île-de-Montréal, and all participants provided written informed consent.

## MRI Acquisition

### Scanner and setup

All MRI data were collected at the Unité de Neuroimagerie Fonctionnelle (UNF), located at the Centre de Recherche de l'Institut Universitaire de Gériatrie de Montréal (CRIUGM), affiliated with the Université de Montréal. The scanner is a Siemens Prisma Fit (3T), equipped with a 2-channel transmit body coil and a 64-channel receive head/neck coil.

To minimize head motion, each participant wore a custom-fitted polystyrene foam headcase manufactured by Caseforge, milled from a 3D surface scan of the participant's head and shaped to fit the 64-channel coil.

### Functional MRI

Functional MRI data were acquired using an accelerated simultaneous multi-slice gradient echo-planar imaging (EPI) sequence developed at the Center for Magnetic Resonance Research (CMRR), University of Minnesota, as part of the Human Connectome Project {cite:p}`glasser2016`. The sequence was obtained through a concept-to-production (C2P) agreement and run with the following parameters: slice acceleration factor = 4, TR = 1.49 s, TE = 37 ms, flip angle = 52°, voxel size = 2 × 2 × 2 mm, 60 slices, acquisition matrix 96 × 96. At the start of each session, a short acquisition (3 volumes) with reversed phase-encoding direction was collected to enable retrospective correction of B0 field inhomogeneity-induced distortions.

### Brain anatomical MRI

Dedicated anatomical sessions were conducted approximately four times per year. Each session began with a 21 s localizer scan, followed by:

- T1-weighted MPRAGE 3D sagittal (6:38 min; TR = 2.4 s, TE = 2.2 ms, flip angle = 8°, 0.8 mm isotropic, R = 2)
- T2-weighted FSE (SPACE) 3D sagittal (5:57 min; TR = 3.2 s, TE = 563 ms, 0.8 mm isotropic, R = 2)
- Diffusion-weighted 2D axial (4:04 min; TR = 2.3 s, TE = 82 ms, 57 slices, 2 mm isotropic, SMS = 3, b-max = 3000 s/mm²; repeated with reversed phase-encoding for distortion correction)
- Gradient-echo magnetization transfer (MT), proton density (PD), and T1-weighted (3D) sequences (TR = 28 ms, TE = 3.3 ms, 1.5 mm isotropic)
- MP2RAGE 3D (7:26 min; TR = 4 s, TE = 1.51 ms, TI1 = 700 ms, TI2 = 1500 ms, 1.2 mm isotropic, R = 2)
- Susceptibility-weighted 3D (4:54 min; TR = 27 ms, TE = 20 ms, flip angle = 15°)

### Spinal cord anatomical MRI

Spinal cord sessions followed the community spine-generic standard protocol {cite:p}`cohen-adad2021` and were acquired during the same dedicated anatomical sessions as brain data. The protocol included T1-weighted (3D sagittal, 1.0 mm isotropic), T2-weighted (3D sagittal, 0.8 mm isotropic), diffusion-weighted (2D axial, cardiac-gated, 0.9 × 0.9 × 0.5 mm), magnetization transfer, proton density, T1-weighted, and multi-echo gradient-echo (3D axial, 0.9 × 0.9 × 0.5 mm) sequences. Full acquisition parameters are documented in the BIDS dataset metadata.

## Stimulus Delivery

Visual stimuli were projected onto a screen in the MRI room using an Epson Powerlite L615U projector via a waveguide. For most datasets, audio was delivered via S15 MRI-compatible earphone inserts (Sensimetrics), with a custom impulse response applied online using a finite impulse response filter to correct for headphone frequency response. Sound was amplified using an AudioSource AMP100V amplifier located in the control room.

Two successive hearing protection configurations were used across the project. The initial setup combined S15 earphone inserts, disposable Comply canal tips (NRR 29 dB), and modified commercial earmuffs (NRR 27 dB; Stanley) trimmed to fit inside the head coil. This setup was used for the `hcptrt`, `movie10`, `friends` seasons 1–4, and `shinobi` datasets. It was subsequently replaced due to pressure discomfort during extended sessions. The current setup uses S15 earphone inserts with custom-sized Comply canal tips selected per participant, combined with memory foam headphone rings (Brainwavz Audio), and was used from `friends` season 5 onward.

Task stimuli were presented using a custom overlay built on top of PsychoPy {cite:p}`peirce2019` for all datasets except `hcptrt`, for which E-Prime scripts adapted from the Human Connectome Project were used. Stimulus scripts are publicly available at https://github.com/courtois-neuromod/task_stimuli.

## Physiological Recordings

During all scanning sessions, physiological signals were recorded using a Biopac M160 MRI-compatible system at 1000 Hz, synchronized to the MRI scanner via trigger pulses and monitored with AcqKnowledge software. The following signals were recorded:

- **Cardiac (plethysmograph):** A Biopac TSD200-MRI photoplethysmogram transducer placed on the foot or toe provided beat-by-beat heart rate estimates.
- **Electrocardiogram:** Three MRI-compatible electrodes placed on the lower left rib cage recorded cardiac electrical activity.
- **Skin conductance:** Two electrodes applied to the sole and ankle of the foot recorded electrodermal activity.
- **Respiration:** A custom MRI-compatible respiration belt consisting of a blood pressure cuff, a pressure sensor (MPXV5004GC7U, NXP), and flexible tubing measured thoracic pressure via an analog input to the Biopac system.

In later datasets (see [DATA RECORD TABLE]), eye movements and pupil dilation were recorded using a high-speed infrared camera (MRC Systems) with illuminating IR LEDs; gaze data were processed with Pupil open-source software.
