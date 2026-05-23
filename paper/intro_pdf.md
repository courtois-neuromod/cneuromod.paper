# Introduction

```{admonition} Abstract
:class: note

Add abstract here.
```

Brain encoding models — trained to predict neural activity from the representations of artificial neural networks (ANNs) — have emerged as a powerful framework to study how the brain processes information [MISSING REF: e.g. Yamins & DiCarlo 2016, Schrimpf et al.]. Aligning artificial and biological representations through brain-augmented learning also shows early promise as a path toward more robust and generalizable AI, with models fine-tuned on brain activity demonstrating improved downstream task performance and faster learning from limited data {cite:p}`Bilgin2025-xz`.

The brain, however, is not a collection of independent modules. It is a multimodal, active system that continuously integrates perception, memory, language, and action. Building encoding models that capture this integrative capacity requires training data that spans a broad range of cognitive states — not just a single domain.

Current deep neuroimaging resources have made major strides in individual coverage, but each tends to optimize for depth within one cognitive domain — vision, language, or audition. Multi-participant datasets, on the other hand, prioritize population breadth at the cost of the individual depth needed to model within-subject brain organization. A resource combining deep individual sampling with genuinely multidomain cognitive coverage has yet to be assembled ({numref}`fig-depth-breadth-pdf`).

:::{figure} ../source_data/dataset_comparison/output_data/dataset_neuroimaging_depthvsbreadth.png
:name: fig-depth-breadth-pdf
:width: 80%

**Brain recordings depth vs. breadth.** Each dot represents a neuroimaging dataset, positioned by the number of brain recording hours per subject (x-axis; fMRI, EEG, MEG, iEEG, and calcium imaging combined) and the number of subjects (y-axis). Diagonal lines mark iso-total-hour contours. CNeuroMod (red) occupies the extreme position on the depth axis, with more recording hours per subject than any other publicly available dataset. [MISSING REF: citations for comparison datasets shown]
:::

The Courtois NeuroMod (CNeuroMod) project was designed to fill this gap. Over five years, six individuals were scanned for approximately 200 hours each {cite:p}`BoyleUnknown-cr`, across a rich collection of 29 datasets spanning vision, language, memory, emotion, audition, and videogame play — the latter enabled by a custom fiber-optic controller developed specifically for the project. The dataset was assembled by a highly interdisciplinary team including specialists across all of these cognitive domains, and represents the largest and most cognitively diverse individual neuroimaging resource to date {cite:p}`BoyleUnknown-cr`.

This paper describes the full CNeuroMod dataset. We present the design and rationale of the 29 datasets, provide evidence of high data quality across participants and modalities, and point to dedicated companion publications examining quality within each specific facet of the collection. We close with an overview of the many uses this dataset enables, from brain encoding and decoding to brain-augmented learning, multidomain cognitive modeling, and beyond.
