---
abstract: |
  [Add abstract here]
---

# Introduction

Brain encoding models — trained to predict neural activity from the representations of artificial neural networks (ANNs) — have emerged as a powerful framework to study how the brain processes information [MISSING REF: e.g. Yamins & DiCarlo 2016, Schrimpf et al.]. Aligning artificial and biological representations through brain-augmented learning also shows early promise as a path toward more robust and generalizable AI, with models fine-tuned on brain activity demonstrating improved downstream task performance and faster learning from limited data {cite:p}`Bilgin2025-xz`.

The brain, however, is not a collection of independent modules. It is a multimodal, active system that continuously integrates perception, memory, language, and action. Building encoding models that capture this integrative capacity requires training data that spans a broad range of cognitive states — not just a single domain.

Current deep neuroimaging resources have made major strides in individual coverage, but each tends to optimize for depth within one cognitive domain — vision, language, or audition. Multi-participant datasets, on the other hand, prioritize population breadth at the cost of the individual depth needed to model within-subject brain organization. A resource combining deep individual sampling with genuinely multidomain cognitive coverage has yet to be assembled ({numref}`fig-depth-breadth`).

Several large neuroimaging initiatives have been designed for breadth — collecting data from thousands of subjects to enable population neuroscience and to train brain foundation models. The Human Connectome Project (HCP), UK Biobank, and OmniMouse exemplify this approach, offering wide coverage at the cost of shallow per-subject sampling.

A parallel tradition has pursued depth: recording from a small number of individuals for many hours under rich, naturalistic conditions. {numref}`fig-per-subject-short` summarizes per-subject data volume across the most prominent resources in this space, spanning five cognitive categories — natural static image viewing, naturalistic video/audio/speech/reading, videogame play, controlled paradigms, and resting state — as well as multiple recording modalities (fMRI, EEG, MEG, iEEG) and physiological signals.

CNeuroMod stands out as the largest per-subject resource in naturalistic video and videogame categories by a wide margin. In the static image domain — dominated by the Natural Scenes Dataset (NSD), which exposes subjects to ~10,000 unique images — CNeuroMod offers ~4,300 unique image presentations per subject, placing it in the same tier while adding cross-domain coverage that NSD does not provide. Across physiology and brain recording modalities, CNeuroMod is consistently among the most richly instrumented resources.

::::{grid} 2
:name: fig-dataset-landscape

:::{grid-item}
:columns: 5

```{figure} ../source_data/dataset_comparison/output_data/dataset_neuroimaging_depthvsbreadth.png
:name: fig-depth-breadth
**(a)**
```

```{figure} ../source_data/dataset_comparison/output_data/dataset_task_composition_radar_cneuromod.png
:name: fig-radar-cneuromod
**(b)** CNeuroMod
```

```{figure} ../source_data/dataset_comparison/output_data/dataset_task_composition_radar_nsd.png
:name: fig-radar-nsd
NSD
```

```{figure} ../source_data/dataset_comparison/output_data/dataset_task_composition_radar_ibc.png
:name: fig-radar-ibc
IBC
```
:::

:::{grid-item}
:columns: 7

```{figure} ../source_data/dataset_comparison/output_data/dataset_comparison_per_subject_short.png
:name: fig-per-subject-short
**(c)**
```
:::
::::

**Figure 1. The dense NeuroAI dataset landscape.** **(a)** Depth vs. breadth scatter plot: each dot is a neuroimaging dataset, positioned by brain recording hours per subject (x-axis; fMRI, EEG, MEG, iEEG, and calcium imaging combined) and number of subjects (y-axis). Diagonal lines mark iso-total-hour contours. CNeuroMod (red) has the highest per-subject recording time of any public dataset. **(b)** Task composition radar charts for CNeuroMod, NSD, and IBC, showing per-subject coverage across eight cognitive domains (images, video, audio, speech, text, resting state, controlled tasks, games). **(c)** Per-subject data volume for the ten largest dense NeuroAI datasets across brain recording modalities, task types, and physiological signals; bubble area scales logarithmically with data volume; black outline marks the largest resource in each column. [MISSING REF: citations for all comparison datasets]

The Courtois NeuroMod (CNeuroMod) project was designed to fill this gap. Over five years, six individuals were scanned for approximately 200 hours each {cite:p}`BoyleUnknown-cr`, across a rich collection of 29 datasets spanning vision, language, memory, emotion, audition, and videogame play — the latter enabled by a custom fiber-optic controller developed specifically for the project. The dataset was assembled by a highly interdisciplinary team including specialists across all of these cognitive domains, and represents the largest and most cognitively diverse individual neuroimaging resource to date {cite:p}`BoyleUnknown-cr`.

This paper describes the full CNeuroMod dataset. We present the design and rationale of the 29 datasets, provide evidence of high data quality across participants and modalities, and point to dedicated companion publications examining quality within each specific facet of the collection. We close with an overview of the many uses this dataset enables, from brain encoding and decoding to brain-augmented learning, multidomain cognitive modeling, and beyond.
