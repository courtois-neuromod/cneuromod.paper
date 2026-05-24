# The Dense NeuroAI Dataset Landscape

Several large neuroimaging initiatives have been designed for breadth — collecting data from thousands of subjects to enable population neuroscience and to train brain foundation models. The Human Connectome Project (HCP), UK Biobank, and OmniMouse exemplify this approach, offering wide coverage at the cost of shallow per-subject sampling.

A parallel tradition has pursued depth: recording from a small number of individuals for many hours under rich, naturalistic conditions. {numref}`fig-dataset-landscape` summarizes per-subject data volume across the most prominent resources in this space, spanning five cognitive categories — natural static image viewing, naturalistic video/audio/speech/reading, videogame play, controlled paradigms, and resting state — as well as multiple recording modalities (fMRI, EEG, MEG, iEEG) and physiological signals (respiration, ECG, plethysmograph, electrodermal activity, eye tracking).

CNeuroMod stands out as the largest per-subject resource in naturalistic video and videogame categories by a wide margin. In the static image domain — dominated by the Natural Scenes Dataset (NSD), which exposes subjects to ~10,000 unique images — CNeuroMod offers ~4,300 unique image presentations per subject, placing it in the same tier while adding cross-domain coverage that NSD does not provide. Across physiology and brain recording modalities, CNeuroMod is consistently among the most richly instrumented resources.

:::{figure} ../source_data/dataset_comparison/output_data/dataset_comparison_per_subject.png
:name: fig-dataset-landscape
:width: 100%

**Dense NeuroAI datasets — per-subject data volume.** Each bubble represents the per-subject data volume for a given dataset and modality, scaled logarithmically by amount (see legend). Datasets are grouped into three panels: brain recordings (fMRI, EEG, MEG, iEEG; blue), cognitive tasks (natural static images, naturalistic video/audio/speech/reading, videogames, controlled paradigms, resting state; green), and physiological signals (respiration, ECG, plethysmograph, electrodermal activity, eye tracking; purple). A black outline marks the largest resource within each column. CNeuroMod (top row) leads in naturalistic video and videogame coverage and ranks among the top resources across all panels. [MISSING REF: citations for all comparison datasets]
:::

:::{figure} ../source_data/dataset_comparison/output_data/dataset_comparison_legend.png
:name: fig-dataset-landscape-legend
:width: 40%
:align: center

**Bubble size legend.** Bubble area scales logarithmically with per-subject data volume (hours for brain recordings and physiology; unique stimuli or minutes for tasks).
:::
