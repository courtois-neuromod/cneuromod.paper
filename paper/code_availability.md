# Code Availability

The code used to generate most dataset assets (preprocessing derivatives, quality-control reports and other
derived data) is distributed with the assets themselves, in a `code` component of each DataLad dataset, and the exact
commands were recorded with `datalad run` (see [Data Record](data_record.md)). This does not yet apply to every asset.
The repositories below cover the analyses and figures of this article.

The depth-vs-breadth dataset comparison figure ({numref}`fig-dataset-landscape`) was
generated with
[`courtois-neuromod/cneuromod.all.comparison`](https://github.com/courtois-neuromod/cneuromod.all.comparison).

The per-subject data volume figure across CNeuroMod datasets ({numref}`fig-cneuromod-volume`)
was generated with
[`courtois-neuromod/cneuromod.all.statistics`](https://github.com/courtois-neuromod/cneuromod.all.statistics).

The fMRI data quality analysis and figure ({numref}`fig-fmri-quality`) were generated with
[`courtois-neuromod/cneuromod.all.qa_figures`](https://github.com/courtois-neuromod/cneuromod.all.qa_figures).

The grey matter stability analysis and figure ({numref}`fig-anat-stability`) were
generated with
[`courtois-neuromod/anat.stability_grey_matter`](https://github.com/courtois-neuromod/anat.stability_grey_matter).

The connectome stability analysis and figure ({numref}`fig-connectome-stability`) were
generated with
[`courtois-neuromod/cneuromod.all.connectome_stats`](https://github.com/courtois-neuromod/cneuromod.all.connectome_stats).

The data reuse analysis and figure ({numref}`fig-reuse`) were generated with
[`courtois-neuromod/cneuromod.all.reuse_stats`](https://github.com/courtois-neuromod/cneuromod.all.reuse_stats).
