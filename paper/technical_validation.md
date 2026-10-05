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

## Stability of brain structure

```{code-cell} python3
:tags: [remove-cell]
# Live grey-matter stability statistics; see paper/_anat_stats.py. Never hardcode these numbers.
sys.path.insert(0, str(next(p for p in (Path("paper"), Path(".")) if (p / "_anat_stats.py").exists())))
from _anat_stats import ANAT

exception_subject = ANAT.non_declining["subject"].iloc[0]
```

Grey-matter volume was tracked across the repeated anatomical sessions of each participant
to establish how stable brain structure is over the course of the project. Volumes were
taken from the longitudinal FreeSurfer stream {cite:p}`reuter2012`, which processes every
session against an unbiased within-subject template, for the {eval}`ANAT.n_subjects`
participants ({eval}`ANAT.sessions_range` sessions each, {eval}`ANAT.n_sessions` in total):
the 68 Desikan cortical regions {cite:p}`desikan2006` (surface-based grey-matter volume), 14
subcortical structures and the 2 cerebellar cortices {cite:p}`fischl2002`
(partial-volume-corrected volumes), {eval}`ANAT.n_regions` regions in all. Each cortical
region was labelled by the Yeo 7-network {cite:p}`yeo2011` covering most of its voxels in
the participant's native space, using the Schaefer 1000-parcel atlas
{cite:p}`schaefer2018`; this label only groups regions for display and summary, and the
volume is always that of the whole region. Each volume was expressed as a percent
deviation from that participant's own mean for the region. Acquisition dates are not part
of this analysis, so sessions are ordered by acquisition but no time interval between them
is assumed. A complementary assessment of the longitudinal reproducibility of quantitative
MRI biomarkers in the same participants is reported in {cite:t}`Boudreau2025-ji`.

Within-subject variation in grey-matter volume is an order of magnitude smaller than
variation between participants ({numref}`fig-anat-stability`, panel D). The coefficient of
variation (CV) of a region across a participant's sessions, averaged over participants, is
smaller than the CV of participants' mean volumes in all {eval}`ANAT.n_regions_intra_below_inter`
of {eval}`ANAT.n_regions` regions, with medians over regions of {eval}`ANAT.cv("intra")`%
within subjects and {eval}`ANAT.cv("inter")`% between subjects. Network medians range from
{eval}`ANAT.network_cv_extreme("intra", "min")` to
{eval}`ANAT.network_cv_extreme("intra", "max")` within subjects, against
{eval}`ANAT.network_cv_extreme("inter", "min")` to
{eval}`ANAT.network_cv_extreme("inter", "max")` between subjects. The Dorsal
Attention network ({eval}`ANAT.n_regions_in("DorsAttn")` regions), the Control network
({eval}`ANAT.n_regions_in("Cont")`) and the cerebellum ({eval}`ANAT.n_regions_in("cerebellum")`)
hold too few regions for their rank in this ordering to be robust.

Superimposed on this stability is a small and consistent decline in volume across
sessions. Averaged over participants, volume falls in every network between the first
session and session {eval}`ANAT.last_session` (the last one reached by at least five
participants), by {eval}`ANAT.network_drop_extreme("min")` to
{eval}`ANAT.network_drop_extreme("max")` percentage points — e.g., from
{eval}`ANAT.deviation("Default", 1)`% to {eval}`ANAT.deviation("Default", ANAT.kept_sessions[-1])`%
in the Default network ({numref}`fig-anat-stability`, panel B). The decline is present in
each participant: least-squares slopes of volume over all regions are negative in
{eval}`ANAT.n_subjects_declining` of {eval}`ANAT.n_subjects` participants, from
{eval}`ANAT.slope_extreme("min")` to {eval}`ANAT.slope_extreme("max")`
(panel C), and {eval}`ANAT.n_trajectories_declining` of {eval}`ANAT.n_trajectories`
participant × network trajectories decline. The exceptions,
{eval}`ANAT.non_declining_phrase()`, come from {eval}`ANAT.non_declining_subjects`, who has
only {eval}`ANAT.subject_sessions(exception_subject)` sessions. This design cannot separate the possible
causes of the decline — ageing, scanner changes, or processing — so we report only its
size and consistency. Over years of repeated scanning, it remains small relative to
differences between individuals, so each participant's anatomy provides a stable
reference for the longitudinal functional data.

:::{figure} ../source_data/anat_stability/output_data/fig_anat_stability.png
:name: fig-anat-stability
:width: 100%

**Grey-matter volume is highly stable within each individual across years of repeated
scanning, with a small, consistent decline.** Volumes come from the longitudinal
FreeSurfer stream for 84 regions (68 Desikan cortical regions, 14 subcortical structures
and 2 cerebellar cortices), each cortical region coloured by the Yeo-7 network covering
most of its voxels in native space. **(A)** Network key: sagittal glass brains showing the
extent of each network in the MNI group atlas, stacked from most to least stable (median
within-subject CV over regions, panel D); colours are used consistently throughout the
figure. The maps are for orientation only, as the analysed regions are defined in each
participant's native space. **(B)** Grey-matter volume per session as percent deviation
from each participant's own mean for that region, averaged over the regions of a network,
then over participants; only sessions reached by at least five participants are shown.
The x axis is session order, and no time interval is implied. **(C)** The same deviation
per participant, averaged over all regions, with each participant's least-squares line
(thick). **(D)** Coefficient of variation of regional volume across sessions within a
participant, averaged over participants (green), and across participants' mean volumes
(orange); bars show the median over the network's regions, and dots individual regions.
:::

## Stability and state dependence of fMRI measures

```{code-cell} python3
:tags: [remove-cell]
# Live connectome statistics; see paper/_connectome_stats.py. Never hardcode these numbers.
sys.path.insert(0, str(next(p for p in (Path("paper"), Path(".")) if (p / "_connectome_stats.py").exists())))
from _connectome_stats import CONN, BINS, join_names as join_datasets

last_lag = CONN.max_lag
n_cells_declining, n_cells = CONN.declining_cells()
weakest = CONN.lowest("median_tsnr")
domain_gate = {"movies": "gated", "videogames": "gated", "stories": "gated",
               "taskscapes": "all", "localizers": "all"}
n_domains_holding = sum(
    CONN.domain_n_positive(d, g) == int(CONN.n_networks) for d, g in domain_gate.items()
)
```

Session-level within-network functional connectomes were computed from the parcellated
BOLD timeseries of `cneuromod.all`, using the cneuromod2026 parcellation — 1,134 parcels
combining a Schaefer cortical parcellation {cite:p}`schaefer2018`, grouped into the 7 Yeo
cortical networks {cite:p}`yeo2011`, a Tian subcortical parcellation {cite:p}`tian2020`,
and a Nettekoven cerebellar parcellation {cite:p}`nettekoven2024`. Runs were z-scored
individually and concatenated within a session, and connectomes were estimated
independently within each network (Pearson correlation of parcel timeseries, Fisher-z
transformed). Session-pair similarity is the Pearson correlation between two sessions'
Fisher-z edge vectors within a network, and bins of session pairs are summarized by their
median similarity. Connectomes were computed for all {eval}`CONN.n_sessions()` available
sessions across {eval}`len(CONN.datasets())` datasets; unless stated otherwise, the
analyses below use the {eval}`CONN.n_sessions("gated")` sessions from
{eval}`len(CONN.datasets("gated"))` datasets ({eval}`join_datasets(CONN.datasets("gated"))`)
carrying at least 30 minutes of usable data, covering all six participants. This
30-minute gate removes {eval}`join_datasets(CONN.gated_out)` entirely.

Within-subject connectome similarity in `friends` — the most task-homogeneous dataset —
declines gently and monotonically with the number of seasons separating two sessions, the
only time axis available since sessions carry no acquisition dates
({numref}`fig-connectome-stability`, panel A). The decline over a
{eval}`last_lag`-season lag ranges from {eval}`CONN.season_drop_extreme("min")` to
{eval}`CONN.season_drop_extreme("max")` — e.g., {eval}`CONN.season("Vis", 0)` to
{eval}`CONN.season("Vis", last_lag)` in the Visual network — while the between-subject
floor (median across networks) barely moves, from {eval}`CONN.floor(0)` to
{eval}`CONN.floor(last_lag)`. The decline is consistent across individuals: averaged over
networks, within-subject similarity drops by {eval}`CONN.subject_drop_range()`% across the
available season lags in each of the {eval}`CONN.n_subjects` participants (panel B), and
it is present in {eval}`n_cells_declining` of {eval}`n_cells` network × participant
combinations. Drift over years of scanning is therefore small relative to the gap between
individuals; the design cannot attribute it to a specific cause (e.g., scanner drift
versus ageing).

Connectome similarity is also sensitive to cognitive context. Across four session-pair
types, the ordering within-subject/within-dataset > within-subject/between-dataset >
between-subject/within-dataset > between-subject/between-dataset holds in
{eval}`CONN.n_networks_ordered()` of {eval}`CONN.n_networks` networks (e.g., Visual
{eval}`CONN.bins("Vis")`; Default {eval}`CONN.bins("Default")`;
{numref}`fig-connectome-stability`, panel D). Similarity increases with session duration,
and the 30-minute gate only partly balances the bins: the median pair minimum duration is
{eval}`CONN.duration(BINS[0])` and {eval}`CONN.duration(BINS[2])` s for the two
within-dataset bins against {eval}`CONN.duration(BINS[1])` and
{eval}`CONN.duration(BINS[3])` s for the two between-dataset bins (a
{eval}`CONN.duration_imbalance_percent()`% imbalance), so part of the between-dataset drop
may reflect duration rather than cognitive state. The within-domain analyses below address
this directly.

Similarity also varies by network quality. The {eval}`CONN.label(weakest)` network has
both the lowest median tSNR ({eval}`CONN.tsnr(weakest)`) and the lowest within-subject
similarity ({eval}`CONN.similarity(weakest)`), and the cerebellum
({eval}`CONN.tsnr("cerebellum")`; {eval}`CONN.similarity("cerebellum")`) and subcortex
({eval}`CONN.tsnr("subcortex")`; {eval}`CONN.similarity("subcortex")`) sit below most
cortical networks on both measures ({numref}`fig-connectome-stability`, panel C).
Per-network tSNR is available for {eval}`CONN.n_tsnr_sessions` sessions from
{eval}`len(CONN.tsnr_datasets)` datasets, which only partly overlap the gated sessions
used for similarity; with nine network-level points, this panel establishes an ordering
rather than a quantitative tSNR–similarity relationship.

As a robustness check on the state-dependence result, restricting the "different task"
comparison to a swap within a single stimulus domain still yields within-subject/within-task
similarity exceeding within-subject/between-task similarity in all
{eval}`CONN.n_networks` networks for {eval}`n_domains_holding` of
{eval}`len(domain_gate)` domains ({numref}`fig-connectome-stability`, panels E–I). The
gap, averaged across networks, is {eval}`CONN.domain_gap("movies")` for movies
({eval}`join_datasets(CONN.domain_datasets("movies"))`, with each season or film treated as
a task; {eval}`CONN.domain_sessions("movies")` sessions),
{eval}`CONN.domain_gap("videogames")` for video games
({eval}`join_datasets(CONN.domain_datasets("videogames"))`;
{eval}`CONN.domain_sessions("videogames")` sessions),
{eval}`CONN.domain_gap("taskscapes", "all")` for taskscapes — tasks that systematically
explore a stimulus space ({eval}`join_datasets(CONN.domain_datasets("taskscapes", "all"))`;
{eval}`CONN.domain_sessions("taskscapes", "all")` sessions),
{eval}`CONN.domain_gap("stories")` for stories
({eval}`join_datasets(CONN.domain_datasets("stories"))`;
{eval}`CONN.domain_sessions("stories")` sessions), and
{eval}`CONN.domain_gap("localizers", "all")` for functional localizers
({eval}`join_datasets(CONN.domain_datasets("localizers", "all"))`;
{eval}`CONN.domain_sessions("localizers", "all")` sessions). In the movie domain the
within- and between-title pairs are matched in duration (median pair minimum duration
{eval}`CONN.domain_duration("movies", "within")` vs.
{eval}`CONN.domain_duration("movies", "between")` s), so the persistence of the gap there
cannot be a duration artifact. The gap is smallest for movies, where "different task"
means a different film rather than a different kind of activity, and grows as the tasks
being swapped become more dissimilar — although this gradient also mixes task
dissimilarity with how finely tasks are defined (title for movies, dataset elsewhere).
Three caveats apply: the stories domain rests on only
{eval}`CONN.domain_sessions("stories")` sessions and is suggestive rather than conclusive;
the taskscape and localizer domains each reduce to a single dataset under the 30-minute
gate and are therefore shown without it; and the localizer between-task pairs are much
shorter than the within-task pairs (median pair minimum duration
{eval}`CONN.domain_duration("localizers", "between", "all")` vs.
{eval}`CONN.domain_duration("localizers", "within", "all")` s), so part of that gap
reflects duration. Stratifying session pairs by head motion or by tSNR does not change any
of these orderings (not shown).

:::{figure} ../source_data/connectome_stats/output_data/connectome_figure.png
:name: fig-connectome-stability
:width: 100%

**Functional connectomes from six deeply sampled individuals are stable across five years,
sensitive to cognitive context, and informative in every network.** **(J)** Network key:
sagittal glass brains showing the anatomical extent of each of the 9 networks, stacked in
decreasing order of stability over seasons (panel A); colors are used consistently
throughout the figure, and panels D–I share this order. **(A)** Within-subject connectome
similarity in `friends` as a function of season lag, one line per network, against the
between-subject curve (grey). **(B)** The same within-subject curves averaged over
networks, one line per participant. **(C)** Within-subject similarity against median
per-network tSNR; open markers show individual participants, filled dots the network
medians. **(D)** Median similarity for within-subject/within-dataset,
within-subject/between-dataset, between-subject/within-dataset, and
between-subject/between-dataset session pairs, per network. **(E–I)** The within- vs.
between-task contrast of panel D repeated within a single stimulus domain — **(E)** movies,
**(F)** video games, **(G)** stories, **(H)** taskscapes and **(I)** functional
localizers; (H) and (I) include sessions below the 30-minute gate. Axes in (A), (B) and
(D–I) are truncated, with the break marked on the frame.
:::
