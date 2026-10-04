"""Live fMRI data-quality statistics for the paper prose.

This module computes nothing. Every number is read from the summary tables produced by
the `qa_figures` submodule's pipeline (`uv run invoke run-qa-summary`), which is the
single place where the per-run MRIQC and regional tSNR tables are aggregated:

    source_data/qa_figures/output_data/tables/summary/overall.tsv
    source_data/qa_figures/output_data/tables/summary/by_subject.tsv
    source_data/qa_figures/output_data/tables/summary/by_dataset.tsv
    source_data/qa_figures/output_data/tables/summary/by_region_group.tsv
    source_data/qa_figures/output_data/tables/summary/coverage.tsv

The helpers below only select and format values (rounding, thousands separators,
percentages, name lists) so they read naturally inline.

Usage in a paper `.md` file:

    ```{code-cell} python3
    :tags: [remove-cell]
    import sys
    from pathlib import Path
    sys.path.insert(0, str(next(p for p in (Path("paper"), Path(".")) if (p / "_qa_stats.py").exists())))
    from _qa_stats import QA
    ```

    ... across {eval}`QA.count("n_runs")` functional runs ...
"""

from pathlib import Path

import pandas as pd

SUMMARY_DATA = Path("source_data/qa_figures/output_data/tables/summary")

REGION_LABEL = {
    "cortex_Limbic": "Limbic",
    "cortex_Vis": "Visual",
    "cortex_Default": "Default",
    "cortex_SomMot": "Somatomotor",
    "cortex_SalVentAttn": "Salience/Ventral Attention",
    "cortex_Cont": "Control",
    "cortex_DorsAttn": "Dorsal Attention",
    "cerebellum": "cerebellum",
    "subcortex_THA": "thalamus",
    "subcortex_CAU": "caudate",
    "subcortex_PUT": "putamen",
}


class Text(str):
    """A string that renders inline without quotes (its repr is itself)."""

    def __repr__(self):
        return str(self)


def find_summary_data(start=None):
    """Locate the summary tables, whatever the build's working directory."""
    here = Path(start or Path.cwd()).resolve()
    for base in [here, *here.parents]:
        candidate = base / SUMMARY_DATA
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(
        f"{SUMMARY_DATA} not found. Initialize the submodule with "
        "`git submodule update --init source_data/qa_figures`."
    )


def join_names(names):
    """'a', 'a and b', 'a, b, and c'."""
    names = list(names)
    if len(names) <= 2:
        return Text(" and ".join(names))
    return Text(", ".join(names[:-1]) + ", and " + names[-1])


class QAStats:
    """Read-only accessor over the qa_figures summary tables."""

    def __init__(self, summary_data=None):
        self.summary_data = Path(summary_data) if summary_data else find_summary_data()
        read = lambda name: pd.read_csv(  # noqa: E731
            self.summary_data / f"{name}.tsv", sep="\t", dtype={"subject": str}
        )
        self.overall = read("overall").set_index("statistic")["value"]
        self.by_subject = read("by_subject").set_index("subject")
        self.by_dataset = read("by_dataset").set_index("dataset")
        self.by_region = read("by_region_group").set_index("group")
        self.coverage = read("coverage").fillna("")

    # --- scalars --------------------------------------------------------------------

    def count(self, statistic):
        """An integer statistic with a thousands separator, e.g. '5,905'."""
        return Text(f"{int(self.overall[statistic]):,}")

    def value(self, statistic, digits=1):
        """A real-valued statistic, rounded."""
        return Text(f"{self.overall[statistic]:.{digits}f}".replace("-", "−"))

    def percent(self, statistic, digits=1):
        """A proportion statistic as a percentage, without the % sign."""
        return Text(f"{100 * self.overall[statistic]:.{digits}f}")

    # --- subjects and datasets ------------------------------------------------------

    def subject(self, label, column="fd_median", digits=3):
        """Median FD (default) or tSNR of one subject ('01'), rounded."""
        return Text(f"{self.by_subject.loc[label, column]:.{digits}f}")

    def subjects_ranked(self, column="fd_median"):
        """Subject labels ordered from lowest to highest `column`."""
        return [Text(s) for s in self.by_subject[column].sort_values().index]

    def dataset(self, name, column="fd_median", digits=3):
        """Median FD (default) or tSNR of one dataset, rounded."""
        return Text(f"{self.by_dataset.loc[name, column]:.{digits}f}")

    def datasets_ranked(self, column="fd_median"):
        """Dataset names ordered from lowest to highest `column`."""
        return [Text(d) for d in self.by_dataset[column].sort_values().index]

    def fold(self, column="fd_median", table="subject", digits=1):
        """Ratio between the highest and lowest median across subjects or datasets."""
        values = (self.by_subject if table == "subject" else self.by_dataset)[column]
        return Text(f"{values.max() / values.min():.{digits}f}")

    # --- regional tSNR --------------------------------------------------------------

    def region(self, group, digits=1):
        """Median per-run tSNR of a region group ('cortex_Limbic'), rounded."""
        return Text(f"{self.by_region.loc[group, 'tsnr_median']:.{digits}f}")

    def regions_ranked(self, descending=False):
        """Region groups ordered by median tSNR."""
        order = self.by_region["tsnr_median"].sort_values(ascending=not descending)
        return list(order.index)

    def region_list(self, groups, digits=1):
        """'Label value, Label value, ...' for the given region groups."""
        return Text(", ".join(f"{REGION_LABEL[g]} {self.region(g, digits)}" for g in groups))

    # --- coverage -------------------------------------------------------------------

    @property
    def without_mriqc(self):
        """Datasets with no BOLD MRIQC derivatives."""
        return list(self.coverage.loc[self.coverage["n_runs_mriqc"] == 0, "dataset"])

    @property
    def with_region_tsnr(self):
        """Datasets with at least one run in the regional tSNR analysis."""
        return list(self.coverage.loc[self.coverage["n_runs_region_tsnr"] > 0, "dataset"])

    @property
    def n_runs_region_tsnr(self):
        return Text(f"{self.coverage['n_runs_region_tsnr'].sum():,}")

    @property
    def region_tsnr_subjects(self):
        """Subject labels with regional tSNR in at least one dataset."""
        labels = {s for row in self.coverage["region_tsnr_subjects"] for s in row.split(",") if s}
        return sorted(labels)

    @property
    def subjects_without_region_tsnr(self):
        return [s for s in self.by_subject.index if s not in self.region_tsnr_subjects]


QA = QAStats()


if __name__ == "__main__":
    q = QA
    print(f"source:              {q.summary_data}")
    print(f"MRIQC runs:          {q.count('n_runs')} in {q.count('n_datasets')} datasets")
    print(f"without MRIQC:       {join_names(q.without_mriqc)}")
    print(f"median FD / tSNR:    {q.value('fd_median', 3)} mm / {q.value('tsnr_median')}")
    print(f"FD rank (subjects):  {q.subjects_ranked()}")
    print(f"FD rank (datasets):  {q.datasets_ranked()}")
    print(f"region tSNR:         {q.n_runs_region_tsnr} runs, {join_names(q.with_region_tsnr)}")
    print(f"region order:        {q.region_list(q.regions_ranked())}")
    print(f"no region tSNR:      {q.subjects_without_region_tsnr}")
