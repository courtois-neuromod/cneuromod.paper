"""Live CNeuroMod statistics for the paper prose.

This module computes nothing. Every number is read from the tables produced by the
`dataset_comparison` submodule's pipeline, which is the single place where CNeuroMod's
`dataset_info.yaml` files are aggregated:

    source_data/dataset_comparison/output_data/cneuromod_tidy_per_subject.csv
    source_data/dataset_comparison/output_data/cneuromod_tidy_total.csv
    source_data/dataset_comparison/output_data/cneuromod_subjects.csv
    source_data/dataset_comparison/output_data/datasets_tidy_total.csv

Datasets are still being collected and released, so no figure may be typed into the prose,
where it would silently go stale. Quote it through this module instead, and refresh the
tables with `uv run invoke run-cneuromod-tables` inside the submodule.

Usage in a paper `.md` file (the project executes code cells with a python3 kernel):

    ```{code-cell} python3
    :tags: [remove-cell]
    import sys
    from pathlib import Path
    sys.path.insert(0, str(next(p for p in (Path("paper"), Path(".")) if (p / "_stats.py").exists())))
    from _stats import STATS
    ```

    ... a collection of {eval}`STATS.n_datasets` datasets ...
"""

from pathlib import Path

import pandas as pd

OUTPUT_DATA = Path("source_data/dataset_comparison/output_data")

PHYSIO_LABEL = {
    "ECG": "ECG",
    "Resp.": "respiration",
    "PPG": "plethysmograph",
    "EDA": "electrodermal activity",
    "Eye": "eye tracking",
}


def find_output_data(start=None):
    """Locate the pipeline's output_data directory, whatever the build's working directory."""
    here = Path(start or Path.cwd()).resolve()
    for base in [here, *here.parents]:
        candidate = base / OUTPUT_DATA
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(
        f"{OUTPUT_DATA} not found. Initialize the submodule with "
        "`git submodule update --init source_data/dataset_comparison`."
    )


class Stats:
    """Read-only accessor over the dataset_comparison output tables."""

    def __init__(self, output_data=None):
        self.output_data = Path(output_data) if output_data else find_output_data()
        self.per_subject = pd.read_csv(self.output_data / "cneuromod_tidy_per_subject.csv")
        self.total = pd.read_csv(self.output_data / "cneuromod_tidy_total.csv")
        self.subjects_table = pd.read_csv(self.output_data / "cneuromod_subjects.csv").fillna("")
        self.comparison = pd.read_csv(self.output_data / "datasets_tidy_total.csv")

    # --- datasets and participants -------------------------------------------------

    @property
    def names(self):
        """Released dataset names, alphabetical."""
        return sorted(self.per_subject["dataset"].unique())

    @property
    def n_datasets(self):
        return len(self.names)

    @property
    def subjects(self):
        return sorted(self.subjects_table["subject"].unique())

    @property
    def n_subjects(self):
        return len(self.subjects)

    # --- volumes --------------------------------------------------------------------

    def _sum(self, table, modality):
        return table.loc[table["modality"] == modality, "value"].sum()

    def total_h(self, modality="fMRI"):
        """Hours of `modality` summed over all CNeuroMod datasets."""
        return self._sum(self.total, modality)

    def per_subject_h(self, modality="fMRI"):
        """Per-subject hours of `modality` summed over all CNeuroMod datasets."""
        return self._sum(self.per_subject, modality)

    @property
    def fmri_total_h(self):
        return round(self.total_h("fMRI"))

    @property
    def fmri_per_subject_h(self):
        return round(self.per_subject_h("fMRI"))

    def physiology_h(self, per_subject=False):
        """{label: hours} for each physiological channel, in table order."""
        table = self.per_subject if per_subject else self.total
        rows = table[table["group"] == "Physiology"]
        return {
            PHYSIO_LABEL.get(mod, mod): round(rows.loc[rows["modality"] == mod, "value"].sum())
            for mod in rows["modality"].unique()
        }

    # --- coverage gaps ----------------------------------------------------------------

    @property
    def incomplete(self):
        """Rows for subjects that are not fully available in a given dataset."""
        return self.subjects_table[self.subjects_table["status"] != "available"]

    def subjects_with_gaps(self):
        """[(subject, n_datasets_affected), ...], most affected first."""
        counts = self.incomplete["subject"].value_counts()
        return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))

    def datasets_for(self, subject):
        """Datasets in which `subject` is missing or partial."""
        rows = self.incomplete
        return sorted(rows.loc[rows["subject"] == subject, "dataset"])


STATS = Stats()


if __name__ == "__main__":
    s = STATS
    print(f"source:            {s.output_data}")
    print(f"datasets:          {s.n_datasets} ({', '.join(s.names)})")
    print(f"subjects:          {s.n_subjects} ({', '.join(s.subjects)})")
    print(f"fMRI total:        {s.fmri_total_h} h")
    print(f"fMRI per subject:  {s.fmri_per_subject_h} h (summed over datasets)")
    for label, hours in s.physiology_h().items():
        print(f"{label:>24}: {hours} h total")
    for subject, n in s.subjects_with_gaps():
        print(f"  {subject}: missing or partial in {n} dataset(s)")
