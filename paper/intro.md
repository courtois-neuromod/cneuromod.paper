---
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
from _stats import COMPARISON, STATS
```

+++ {"part": "abstract"}

Artificial neural networks can be trained to imitate both the brain activity and the behaviour of an individual, a framework to study how the brain processes information and a possible route toward more robust AI. Imitating one person requires many hours of their brain and behavioural data, across many cognitive domains, yet existing deep neuroimaging resources each focus on a single domain. The Courtois NeuroMod (CNeuroMod) project was designed to fill this gap. Over more than five years, {eval}`STATS.n_subjects` healthy adults were each scanned for an average of {eval}`STATS.fmri_per_subject_h` hours of fMRI, across {eval}`STATS.n_datasets` datasets in six cognitive categories: movies, stories, videogame play recorded with a custom MRI-compatible controller, controlled paradigms with many trials, functional localizers, and anatomical and validation data. The {eval}`STATS.fmri_total_h` hours of 3T fMRI come with physiological recordings, eye tracking, and repeated anatomical scans of the brain and spinal cord, released in BIDS with preprocessing derivatives as versioned DataLad datasets, openly for five of the six participants. Head motion was low, and both grey-matter volume and functional connectomes were stable within individuals across years, with connectomes remaining sensitive to cognitive context. Community uptake is already substantial and growing, spanning individual encoding models that predict brain responses to multimodal movies and generalize to new stimuli; models of the active brain, comparing artificial agents playing the same videogames with each participant's gameplay and brain activity; brain decoding of perception and action; brain-informed training of AI models; cognitive neuroscience with annotated naturalistic stimuli; and foundation models of individual brains.

+++

Brain encoding models are trained to predict neural activity directly from rich stimuli, using the representations of artificial neural networks (ANNs) as predictive features. Brain encoding has emerged as a powerful approach to study how the brain processes information {cite:p}`yamins2016,schrimpf2020`. Aligning artificial and biological representations through brain-augmented learning also shows early promise as a path toward more robust and generalizable AI, with models fine-tuned on brain activity demonstrating improved downstream task performance and faster learning from limited data {cite:p}`Bilgin2025-xz`.

The brain, however, is not a collection of independent modules. It is a multimodal, active system that continuously integrates perception, memory, language, and action. Building encoding models that capture this integrative capacity requires training data that spans a broad range of cognitive states and not just a single domain.

Classical large-scale neuroimaging initiatives have been designed for breadth, i.e. collecting data from thousands of subjects to enable population neuroscience and to train brain foundation models that generalize across participants. The Human Connectome Project (HCP) {cite:p}`glasser2016,barch2013` and UK Biobank {cite:p}`miller2016` are flagship datasets in this category. Such datasets, however, typically offer shallow per-subject sampling, with about {eval}`round(COMPARISON.value("HCP", "fMRI"))` hours of functional magnetic resonance imaging (fMRI) per participant in HCP and only {eval}`round(60 * COMPARISON.value("UK Biobank", "fMRI"))` minutes in UK Biobank. Importantly, these datasets rely on a short, fixed battery of tasks administered identically to all participants, and therefore have limited coverage of cognitive states.

A parallel tradition has pursued depth: recording from a small number of individuals for many hours under rich, naturalistic conditions. {numref}`fig-dataset-landscape` summarizes per-subject data volume across the most prominent resources in this space, along several stimulus and task dimensions — static images, naturalistic video, audio, speech and text, videogame play, controlled tasks and resting state — as well as recording modalities (fMRI, EEG, MEG, iEEG) and physiological signals. Although existing deep neuroimaging resources have made major strides in individual coverage, each tends to optimize for depth within one specific cognitive domain, such as vision, language, or audition. A resource combining deep individual sampling with extensive multidomain cognitive coverage has yet to be assembled.

```{code-cell} python3
:tags: [remove-cell]
# Regenerates figures/fig1_dataset_landscape.png (shown by the figure directive below)
# when the book is built with --execute; the committed PNG is used otherwise.
import matplotlib
matplotlib.use("Agg")
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

out_dir = next(p for p in (Path("paper/figures"), Path("figures")) if p.exists())
fig.savefig(out_dir / "fig1_dataset_landscape.png", dpi=150, bbox_inches="tight")
plt.close(fig)
```

:::{figure} figures/fig1_dataset_landscape.png
:name: fig-dataset-landscape
:width: 100%

**The dense NeuroAI dataset landscape.** The ten datasets with the most fMRI hours per subject are colored by rank, from purple to orange (deepest); this color code is shared across panels. **(a)** Depth vs. breadth scatter plot: each dot is a neuroimaging dataset positioned by fMRI hours per subject (x-axis) and number of subjects (y-axis), both on log scales. Diagonal lines mark iso-total-hour contours (100, 1,000 and 10,000 h). CNeuroMod has the highest per-subject recording time of any dataset in the comparison. **(b)** Per-subject data volume of the ten deepest datasets for fMRI and physiological signals (eye tracking, EDA, PPG, respiration, ECG); bubble area scales logarithmically with data volume, and a black outline marks the largest dataset in each row. **(c)** Cognitive depth radar charts for the same ten datasets, showing per-subject coverage of unique images (×100), video, audio, speech and text stimuli, resting state, controlled tasks and videogame play (hours), and number of task contrasts, on a logarithmic radial scale (key at left); a black outline marks the largest dataset on each axis. Datasets: AtariFMRI {cite:p}`tomov2023`, BOLD5000 {cite:p}`chang2019`, Doctor Who {cite:p}`seeliger2019`, HCP {cite:p}`barch2013`, IBC {cite:p}`ponce2026`, iEEG-fMRI film {cite:p}`berezutskaya2022`, MSC {cite:p}`gordon2017`, MyConnectome {cite:p}`poldrack2015`, Narratives {cite:p}`nastase2021`, NL-fMRI {cite:p}`lebel2023`, NNDb {cite:p}`aliko2020`, NOD {cite:p}`zhang2025`, NSD {cite:p}`allen2021`, OmniMouse {cite:p}`willeke2026`, Sherlock MEG {cite:p}`armeni2022`, Spacetop {cite:p}`jung2025`, studyforrest {cite:p}`hanke2016` and UK Biobank {cite:p}`miller2016`.
:::

The Courtois NeuroMod (CNeuroMod) project was designed to fill this gap. Over more than five years, {eval}`STATS.n_subjects` individuals were each scanned for an average of {eval}`STATS.fmri_per_subject_h` hours of fMRI {cite:p}`BoyleUnknown-cr`, across a rich collection of {eval}`STATS.n_datasets` datasets organized into six cognitive categories ({numref}`tab-cognitive-categories`): naturalistic movies and stories, videogame play — enabled by a custom fiber-optic controller developed specifically for the project {cite:p}`Harel2023-gp` — densely sampled experimental paradigms (which we term *taskscapes*), standard functional localizers, and complementary anatomical, auditory and hardware validation data.

<!-- Mirrors CATEGORIES in .claude/skills/update-data-overview/scripts/build_overview.py; keep in sync. -->
:::{table} **Cognitive categories of the CNeuroMod datasets.**
:name: tab-cognitive-categories

| Category | Description | Datasets |
|---|---|---|
| 🍿 Movies | Naturalistic viewing of feature films and TV series | `movie10`, `friends`, `ood` |
| 💬 Stories | Naturalistic narratives, listened to as audiobooks or read word by word | `harrypotter`, `petit-prince`, `narratives` |
| 👾 Videogames | Active play of retro videogames with a custom MRI-compatible controller | `shinobi`, `mario`, `mariostars`, `mario3`, `mario_eeg` |
| 🔬 Taskscapes | Controlled experimental paradigms with many trials spread over many sessions | `triplets`, `things`, `emotion-videos`, `multfs`, `mutemusic` |
| 🧭 Functional localizers | Standard tasks that map functional regions in each participant | `langlocalizer`, `floc`, `retinotopy`, `hcptrt` |
| 🧰 Others | Anatomical, auditory and hardware validation data | `hearing`, `anat`, `gamepad` |
:::

CNeuroMod stands out as the largest per-subject resource in the naturalistic video and videogame categories by a wide margin ({numref}`fig-dataset-landscape`c), and as the most richly instrumented one across all physiological modalities ({numref}`fig-dataset-landscape`b). The Stories category includes {eval}`STATS.stories_unique_h` hours of unique stories per participant, heard as audiobooks or read word by word, complemented by sessions in which participants recalled the stories <!-- TODO: quote recall hours once they are added to narratives/dataset_info.yaml -->. This exceeds the entire stimulus set of Narratives ({eval}`COMPARISON.value("Narratives", "Speech", per_subject=False)` hours) {cite:p}`nastase2021`, although the natural language dataset of {cite:t}`lebel2023` offers more hours of spoken stories per participant ({eval}`COMPARISON.value("NL-fMRI", "Speech")` hours).

The taskscapes category has multiple variants, each focused on a separate domain. The static image domain is currently the most developed in the field, and is dominated by the Natural Scenes Dataset (NSD) {cite:p}`allen2021`, which exposed each participant to up to {eval}`COMPARISON.count("NSD", "Images")` unique images (1,000 of which were shared across participants) drawn from the COCO database of complex scenes {cite:p}`lin2014`. CNeuroMod `things` offers {eval}`STATS.things_images` unique images per participant, each shown three times and drawn from 720 object categories of the THINGS initiative {cite:p}`hebart2019,St-Laurent2026-zc`. This is on par with BOLD5000 {cite:p}`chang2019`, and complements THINGS-fMRI, which samples the same object concepts {cite:p}`hebart2023`. Other CNeuroMod taskscapes similarly probe a systematic stimulus–task space: visual working memory (`multfs`, with roughly 420 unique configurations, each repeated at least ten times <!-- TODO: verify against multfs docs -->), semantic word representation (`triplets`), musical imagery (`mutemusic`, with 60 familiar and unfamiliar music tracks per participant, interrupted by silent gaps and each presented three times) and emotions (`emotion-videos`, with 1,888 short silent videos, each shown once). With the exception of `emotion-videos`, which builds on the emotion-evoking video set of {cite:t}`cowen2017` and its fMRI study by {cite:t}`horikawa2020`, these domains have rarely been probed at this scale.

The functional localizers cover the seven task domains of the HCP {cite:p}`barch2013`, with 13 to 18 repetitions of the full battery per participant, complemented by visual (`floc`, `retinotopy`) and language (`langlocalizer`) localizers, for a total of {eval}`STATS.localizer_contrasts` canonical contrasts.

CNeuroMod therefore pushes the frontier in some domains, most notably videogames, and matches existing resources in others. What sets it apart is that all of these domains, from movies and stories to videogames, taskscapes and localizers, were sampled in the same individuals, making it the most cognitively diverse intensive individual neuroimaging resource to date ({numref}`fig-dataset-landscape`a). This paper describes the full CNeuroMod dataset. We present the design and rationale of the {eval}`STATS.n_datasets` datasets, provide evidence of high data quality across participants and modalities, and point to dedicated companion publications examining quality within each specific facet of the collection. We close with an overview of the many uses this dataset enables, from brain encoding and decoding to brain-augmented learning, multidomain cognitive modeling, and beyond.
