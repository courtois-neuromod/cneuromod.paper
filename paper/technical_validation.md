---
kernelspec:
  name: python3
  display_name: Python 3
  language: python
---

# Technical Validation

[Demonstrate the quality and reliability of the data through quantitative quality metrics,
reproducibility analyses, and comparisons against established benchmarks.]

```{code-cell} python3
:tags: [remove-cell]
import sys
from pathlib import Path

# Live data-quality statistics; see paper/_qa_stats.py. Never hardcode these numbers.
sys.path.insert(0, str(next(p for p in (Path("paper"), Path(".")) if (p / "_qa_stats.py").exists())))
from _qa_stats import QA, join_names

fd_subjects = QA.subjects_ranked("fd_median")
fd_datasets = QA.datasets_ranked("fd_median")
tsnr_subjects = QA.subjects_ranked("tsnr_median")
tsnr_datasets = QA.datasets_ranked("tsnr_median")
regions = QA.regions_ranked()
```

## fMRI data quality

Functional image quality was assessed with MRIQC {cite:p}`esteban2017mriqc`, computed per
run on the raw BOLD data. We report head-motion and temporal signal-to-noise ratio (tSNR)
image-quality metrics (IQMs) across the {eval}`QA.count("n_runs")` functional runs with
released MRIQC derivatives, spanning {eval}`QA.count("n_datasets")` datasets,
{eval}`QA.count("n_subjects")` participants, and {eval}`QA.count("n_sessions")` unique
dataset × subject × session combinations. The {eval}`len(QA.without_mriqc)` remaining
datasets ({eval}`join_names(QA.without_mriqc)`) have no BOLD MRIQC derivatives available
yet and are excluded from this analysis; the numbers below therefore describe the
datasets with released MRIQC derivatives, not the full collection. No pass/fail threshold
is applied anywhere in this analysis and no run is excluded — the distributions below
describe the released data as-is.

Head motion, summarized as mean framewise displacement (FD) per run
{cite:p}`power2012`, was low overall: median {eval}`QA.value("fd_median", 3)` mm (mean
{eval}`QA.value("fd_mean", 3)`, SD {eval}`QA.value("fd_sd", 3)`, range
{eval}`QA.value("fd_min", 3)`–{eval}`QA.value("fd_max", 3)` mm across runs).
{eval}`QA.count("n_runs_fd_gt05")` runs exceeded a mean FD of 0.5 mm, and
{eval}`QA.count("n_runs_fd_gt02")` runs ({eval}`QA.percent("prop_runs_fd_gt02")`%)
exceeded 0.2 mm. At the volume level ({eval}`QA.count("n_runs_with_fd_timeseries")` runs
with MRIQC framewise-displacement timeseries available), a median of
{eval}`QA.percent("vol_prop_gt02_median")`% of volumes per run exceeded 0.2 mm and a
median of {eval}`QA.percent("vol_prop_gt05_median")`% exceeded 0.5 mm (means
{eval}`QA.percent("vol_prop_gt02_mean")`% and {eval}`QA.percent("vol_prop_gt05_mean")`%).
Motion varied about {eval}`QA.fold("fd_median")`-fold across participants —
sub-{eval}`fd_subjects[0]` and sub-{eval}`fd_subjects[1]` showed the lowest motion
(median FD {eval}`QA.subject(fd_subjects[0])` and {eval}`QA.subject(fd_subjects[1])` mm),
sub-{eval}`fd_subjects[-2]` and sub-{eval}`fd_subjects[-1]` the highest
({eval}`QA.subject(fd_subjects[-2])` and {eval}`QA.subject(fd_subjects[-1])` mm) — while
sub-{eval}`fd_subjects[2]` and sub-{eval}`fd_subjects[3]` fell in between
({eval}`QA.subject(fd_subjects[2])` and {eval}`QA.subject(fd_subjects[3])` mm). Motion
also varied systematically with task demands: passive paradigms such as
{eval}`join_names(fd_datasets[:3])` had the lowest median FD
({eval}`QA.dataset(fd_datasets[0])`–{eval}`QA.dataset(fd_datasets[2])` mm), while the
video-game datasets {eval}`join_names(fd_datasets[-3:])` had the highest
({eval}`QA.dataset(fd_datasets[-3])`–{eval}`QA.dataset(fd_datasets[-1])` mm), consistent
with the additional head movement associated with active gameplay.

Temporal SNR followed the inverse pattern: median {eval}`QA.value("tsnr_median")` across
runs (mean {eval}`QA.value("tsnr_mean")`, SD {eval}`QA.value("tsnr_sd")`, range
{eval}`QA.value("tsnr_min")`–{eval}`QA.value("tsnr_max")`), with a strong negative
correlation between per-run mean FD and tSNR (Pearson r =
{eval}`QA.value("fd_tsnr_pearson", 2)`, Spearman ρ =
{eval}`QA.value("fd_tsnr_spearman", 2)`) — runs and participants with more motion have
correspondingly lower tSNR. Per-subject median tSNR ranged from
{eval}`QA.subject(tsnr_subjects[0], "tsnr_median", 1)` (sub-{eval}`tsnr_subjects[0]`) to
{eval}`QA.subject(tsnr_subjects[-1], "tsnr_median", 1)` (sub-{eval}`tsnr_subjects[-1]`),
and per-dataset median tSNR from {eval}`QA.dataset(tsnr_datasets[0], "tsnr_median", 1)`
({eval}`tsnr_datasets[0]`) to {eval}`QA.dataset(tsnr_datasets[-1], "tsnr_median", 1)`
({eval}`tsnr_datasets[-1]`), with the lowest values again in the video-game datasets
({eval}`join_names(tsnr_datasets[:3])`).

Regional tSNR was further characterized by averaging per-run tSNR maps within each
participant's own combined Schaefer-1000/7-network cortical {cite:p}`schaefer2018,yeo2011`,
Tian-S3 subcortical {cite:p}`tian2020`, and Nettekoven cerebellar {cite:p}`nettekoven2024`
atlas, defined in MNI space at the functional resolution, and collapsed to
{eval}`len(regions)` region groups. This analysis covers {eval}`QA.n_runs_region_tsnr`
runs from {eval}`len(QA.with_region_tsnr)` datasets ({eval}`join_names(QA.with_region_tsnr)`)
and {eval}`len(QA.region_tsnr_subjects)` participants; per-run tSNR maps for the remaining
datasets and participants were not available for this pass. Median tSNR was lowest in the
Limbic network ({eval}`QA.region("cortex_Limbic")` — orbitofrontal and ventral-temporal
cortex) and in subcortical structures and cerebellum
({eval}`QA.region_list(["subcortex_THA", "subcortex_CAU", "subcortex_PUT", "cerebellum"])`),
and highest in dorsal cortical networks
({eval}`QA.region_list([g for g in QA.regions_ranked(descending=True) if g.startswith("cortex_") and g != "cortex_Limbic"])`).
This ordering reflects the expected susceptibility-dropout pattern of gradient-echo EPI
near air-tissue interfaces, a property of the acquisition geometry rather than of
CNeuroMod specifically; users of ventral-temporal, orbitofrontal, or deep subcortical
signal should budget for reduced tSNR in these regions.

:::{figure} ../source_data/qa_figures/output_data/qa_figure.png
:name: fig-fmri-quality
:width: 100%

**fMRI data quality across the CNeuroMod datasets.** **(a)** Average run FD per dataset.
**(b)** Average run FD per subject. **(c)** Percentage of runs with severe motion (mean
FD > 0.5 mm) per subject. **(d)** Percentage of runs with mild or severe motion (mean
FD > 0.2 mm) per subject. **(e)** Average tSNR maps across subjects and datasets (top),
with voxelwise coverage maps thresholded at tSNR > 30 (middle) and tSNR > 10 (bottom);
orbitofrontal cortex (OFC), ventral temporal cortex (vTC), and subcortex are annotated as
regions of reduced coverage. **(f)** tSNR per run, by subject. **(g)** tSNR distribution
per region group across runs (datasets with per-run tSNR maps), from best (Dorsal
Attention) to worst (Limbic), with matching glass-brain maps of each region group below.
:::

Taken together, these metrics indicate low and stable head motion and adequate temporal
signal quality across the released functional runs, with expected, interpretable variation
across participants, tasks, and brain regions. The main limitation of this analysis is its
restriction to datasets and participants with released MRIQC and tSNR derivatives, and
it will be extended as further derivatives become publicly available.

## sMRI data quality

Structural image quality was assessed separately across the anatomical acquisitions of the
same six participants and is reported in a companion publication [MISSING REF: companion
CNeuroMod structural data quality paper — citation to be supplied].

## Longitudinal stability and state-dependence of fMRI measures

Session-level within-network functional connectomes were computed from the parcellated
BOLD timeseries of `cneuromod.all`, using the cneuromod2026 parcellation — 1,134 parcels
combining a Schaefer cortical parcellation {cite:p}`schaefer2018`, grouped into the 7 Yeo
cortical networks {cite:p}`yeo2011`, a Tian subcortical parcellation {cite:p}`tian2020`,
and a Nettekoven cerebellar parcellation {cite:p}`nettekoven2024`. Runs were z-scored
individually and concatenated within a session, and connectomes were estimated
independently within each network (Pearson correlation of parcel timeseries, Fisher-z
transformed). Session-pair similarity is the Pearson correlation between two sessions'
Fisher-z edge vectors within a network, and bins of session pairs are summarized by their
median similarity. Connectomes were computed for all 829 available sessions across 10
datasets; the analyses below use the 559 sessions from 7 datasets (`friends`,
`harrypotter`, `hcptrt`, `mario`, `movie10`, `petit-prince`, `shinobi`) carrying at least
30 minutes of usable data, covering all six participants. This 30-minute gate removes
`floc`, `retinotopy`, and `things` entirely.

Within-subject connectome similarity in `friends` — the most task-homogeneous dataset —
declines gently and monotonically with the number of seasons separating two sessions, the
only time axis available since sessions carry no acquisition dates
({numref}`fig-connectome-stability`, panel A). The decline over a five-season lag ranges
from 0.019 (cerebellum) to 0.043 (Limbic network) — e.g., 0.956 to 0.935 in the Visual
network — and every network remains far above the between-subject floor (0.564–0.572).
Drift over years of scanning is therefore small relative to the gap between individuals.

Connectome similarity is also sensitive to cognitive context. Across four session-pair
types, the ordering within-subject/within-dataset > within-subject/between-dataset >
between-subject/within-dataset > between-subject/between-dataset holds in all 9 networks
(e.g., Visual 0.95/0.80/0.69/0.63; Default 0.94/0.72/0.56/0.45;
{numref}`fig-connectome-stability`, panel B). This contrast is not confounded by
acquisition duration: similarity increases with session duration, so the four bins were
matched by construction, with median pair minimum duration ranging only 2,669–2,784 s
(within 4%) across bins. The between-dataset drop in similarity therefore reflects a
genuine effect of cognitive state rather than a duration artifact or measurement noise.

Similarity also varies by network quality. The Limbic network has both the lowest median
tSNR (18.6) and the lowest within-subject similarity (0.859), and the cerebellum and
subcortex sit below the cortical networks on both measures
({numref}`fig-connectome-stability`, panel C). This comparison is descriptive only: the
per-network tSNR values are available only for the `floc`, `retinotopy`, and `things`
datasets (182 sessions) — precisely the three datasets removed by the 30-minute gate —
while similarity is computed over the disjoint set of 559 gated sessions. With nine
network-level points and no shared sessions between the two axes, this panel establishes
an ordering, not a quantitative tSNR–similarity relationship.

As a robustness check on the state-dependence result, restricting the "different task"
comparison to a swap within a single naturalistic stimulus domain — movies (`friends` and
`movie10`, 333 sessions), video games (`mario`, `mario3`, `mariostars`, `shinobi`, 138
sessions), and stories (`harrypotter`, `petit-prince`, 19 sessions) — still yields
within-subject/within-task similarity exceeding within-subject/between-task similarity in
all 9 networks for all three domains ({numref}`fig-connectome-stability`, panels D–F),
with median gaps of 0.022 (movies), 0.047 (video games), and 0.077 (stories). The effect
is smallest for movies, where "different task" means a different film rather than a
different kind of activity; the stories domain, resting on only 19 sessions, is
suggestive rather than conclusive. Stratifying session pairs by head motion or by tSNR
does not change any of these orderings (not shown).

:::{figure} ../source_data/connectome_stats/output_data/connectome_figure.png
:name: fig-connectome-stability
:width: 100%

**Functional connectomes from six deeply sampled individuals are stable across five years,
sensitive to cognitive context, and informative in every network.** **(G)** Network key:
sagittal glass brains showing the anatomical extent of each of the 9 networks; colors are
used consistently throughout the figure. **(A)** Within-subject connectome similarity in
`friends` as a function of season lag, remaining well above the between-subject floor
(grey band). **(B)** Median similarity for within-subject/within-dataset,
within-subject/between-dataset, between-subject/within-dataset, and
between-subject/between-dataset session pairs, per network. **(C)** Within-subject
similarity against median per-network tSNR (disjoint session sets; see main text).
**(D–F)** The within- vs. between-task contrast of panel B repeated within a single
stimulus domain — **(D)** movies, **(E)** video games, **(F)** stories. Axes in (A) and in
(B, D–F) are truncated, with the break marked on the frame.
:::

## Preprocessing Pipeline Validation

[Describe any validation steps applied to preprocessed derivatives.]
