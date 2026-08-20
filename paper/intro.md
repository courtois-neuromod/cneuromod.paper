---
abstract: |
  [Add abstract here]
kernelspec:
  name: python3
  display_name: Python 3
  language: python
---

# Introduction

```{code-cell} python3
:tags: [remove-cell]
import sys
from pathlib import Path

# Live dataset statistics; see paper/_stats.py. Never hardcode these numbers.
sys.path.insert(0, str(next(p for p in (Path("paper"), Path(".")) if (p / "_stats.py").exists())))
from _stats import STATS
```

Brain encoding models — trained to predict neural activity from the representations of artificial neural networks (ANNs) — have emerged as a powerful framework to study how the brain processes information [MISSING REF: e.g. Yamins & DiCarlo 2016, Schrimpf et al.]. Aligning artificial and biological representations through brain-augmented learning also shows early promise as a path toward more robust and generalizable AI, with models fine-tuned on brain activity demonstrating improved downstream task performance and faster learning from limited data {cite:p}`Bilgin2025-xz`.

The brain, however, is not a collection of independent modules. It is a multimodal, active system that continuously integrates perception, memory, language, and action. Building encoding models that capture this integrative capacity requires training data that spans a broad range of cognitive states — not just a single domain.

Current deep neuroimaging resources have made major strides in individual coverage, but each tends to optimize for depth within one cognitive domain — vision, language, or audition. Multi-participant datasets, on the other hand, prioritize population breadth at the cost of the individual depth needed to model within-subject brain organization. A resource combining deep individual sampling with genuinely multidomain cognitive coverage has yet to be assembled ({numref}`fig-dataset-landscape`).

Several large neuroimaging initiatives have been designed for breadth — collecting data from thousands of subjects to enable population neuroscience and to train brain foundation models. The Human Connectome Project (HCP), UK Biobank, and OmniMouse exemplify this approach, offering wide coverage at the cost of shallow per-subject sampling.

A parallel tradition has pursued depth: recording from a small number of individuals for many hours under rich, naturalistic conditions. {numref}`fig-dataset-landscape` summarizes per-subject data volume across the most prominent resources in this space, spanning five cognitive categories — natural static image viewing, naturalistic video/audio/speech/reading, videogame play, controlled paradigms, and resting state — as well as multiple recording modalities (fMRI, EEG, MEG, iEEG) and physiological signals.

CNeuroMod stands out as the largest per-subject resource in naturalistic video and videogame categories by a wide margin. In the static image domain — dominated by the Natural Scenes Dataset (NSD), which exposes subjects to ~10,000 unique images — CNeuroMod offers ~4,300 unique image presentations per subject, placing it in the same tier while adding cross-domain coverage that NSD does not provide. Across physiology and brain recording modalities, CNeuroMod is consistently among the most richly instrumented resources.

```{code-cell} python3
:tags: [hide-input]
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from pathlib import Path

# Resolve image directory whether CWD is project root or paper/
_candidates = [
    Path("source_data/dataset_comparison/output_data"),
    Path("../source_data/dataset_comparison/output_data"),
]
base = next(p for p in _candidates if p.exists())

img_a = mpimg.imread(base / "dataset_neuroimaging_depthvsbreadth.png")
img_b = mpimg.imread(base / "dataset_comparison_per_subject_short.png")
img_c = mpimg.imread(base / "dataset_task_composition_radar_grid.png")

FIG_W = 12.0

# Top row: panel a (40%) and panel b (60%)
h_a   = FIG_W * 0.4 * img_a.shape[0] / img_a.shape[1]
h_b   = FIG_W * 0.6 * img_b.shape[0] / img_b.shape[1]
h_top = max(h_a, h_b)

# Bottom row: panel c full width
h_c = FIG_W * img_c.shape[0] / img_c.shape[1]

fig = plt.figure(figsize=(FIG_W, h_top + h_c))
gs  = gridspec.GridSpec(2, 1, figure=fig, height_ratios=[h_top, h_c], hspace=0.08)

# Top row: depth vs breadth | physiological depth
gs_top = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=gs[0],
                                          width_ratios=[2, 3], wspace=0.04)

ax_a = fig.add_subplot(gs_top[0])
ax_a.imshow(img_a)
ax_a.axis('off')
ax_a.text(0.0,  1.03, 'a',                transform=ax_a.transAxes,
          fontsize=12, fontweight='bold', va='bottom', ha='left', clip_on=False)
ax_a.text(0.5,  1.03, 'depth vs breadth', transform=ax_a.transAxes,
          fontsize=11, fontweight='bold', va='bottom', ha='center', clip_on=False)

ax_b = fig.add_subplot(gs_top[1])
ax_b.imshow(img_b)
ax_b.axis('off')
ax_b.text(0.0,  1.03, 'b',                    transform=ax_b.transAxes,
          fontsize=12, fontweight='bold', va='bottom', ha='left', clip_on=False)
ax_b.text(0.5,  1.03, 'physiological depth',  transform=ax_b.transAxes,
          fontsize=11, fontweight='bold', va='bottom', ha='center', clip_on=False)

# Bottom row: cognitive depth (11 radar plots)
ax_c = fig.add_subplot(gs[1])
ax_c.imshow(img_c)
ax_c.axis('off')
ax_c.text(0.0,  1.03, 'c',               transform=ax_c.transAxes,
          fontsize=12, fontweight='bold', va='bottom', ha='left', clip_on=False)
ax_c.text(0.5,  1.03, 'cognitive depth', transform=ax_c.transAxes,
          fontsize=11, fontweight='bold', va='bottom', ha='center', clip_on=False)

plt.show()
```

:::{figure} figures/fig1_dataset_landscape.png
:name: fig-dataset-landscape
:width: 100%

**The dense NeuroAI dataset landscape.** **(a)** Depth vs. breadth scatter plot: each dot is a neuroimaging dataset positioned by brain recording hours per subject (x-axis; fMRI, EEG, MEG, iEEG, and calcium imaging combined) and number of subjects (y-axis). Diagonal lines mark iso-total-hour contours. CNeuroMod (red) has the highest per-subject recording time of any public dataset. **(b)** Per-subject data volume for the largest dense NeuroAI datasets across brain recording modalities, task types, and physiological signals; bubble area scales logarithmically with data volume; black outline marks the largest resource in each column. **(c)** Cognitive depth radar charts for 11 dense NeuroAI datasets, showing per-subject coverage across cognitive domains. [MISSING REF: citations for all comparison datasets]
:::

The Courtois NeuroMod (CNeuroMod) project was designed to fill this gap. Over five years, six individuals were scanned for approximately 200 hours each {cite:p}`BoyleUnknown-cr`, across a rich collection of {eval}`STATS.n_datasets` datasets spanning vision, language, memory, emotion, audition, and videogame play — the latter enabled by a custom fiber-optic controller developed specifically for the project. The dataset was assembled by a highly interdisciplinary team including specialists across all of these cognitive domains, and represents the largest and most cognitively diverse individual neuroimaging resource to date {cite:p}`BoyleUnknown-cr`.

This paper describes the full CNeuroMod dataset. We present the design and rationale of the {eval}`STATS.n_datasets` datasets, provide evidence of high data quality across participants and modalities, and point to dedicated companion publications examining quality within each specific facet of the collection. We close with an overview of the many uses this dataset enables, from brain encoding and decoding to brain-augmented learning, multidomain cognitive modeling, and beyond.
