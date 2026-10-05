"""Live grey-matter stability statistics for the paper prose.

Every number is read from the tracked tables produced by the `anat_stability`
submodule's pipeline (`uv run invoke run` inside it), which is where volumes are
extracted, coefficients of variation computed and trajectories fitted:

    source_data/anat_stability/output_data/stability_per_region.tsv
    source_data/anat_stability/output_data/volume_trajectories.tsv
    source_data/anat_stability/output_data/trajectory_slopes.tsv

The helpers below select values and do only light arithmetic on the published tables
(medians over a network's regions, differences between two sessions, counts of negative
slopes), and format them to read naturally inline.

Usage in a paper `.md` file:

    ```{code-cell} python3
    :tags: [remove-cell]
    import sys
    from pathlib import Path
    sys.path.insert(0, str(next(p for p in (Path("paper"), Path(".")) if (p / "_anat_stats.py").exists())))
    from _anat_stats import ANAT
    ```

    ... across {eval}`ANAT.n_sessions` anatomical sessions ...
"""

from pathlib import Path

import pandas as pd

OUTPUT_DATA = Path("source_data/anat_stability/output_data")

# Panel B of the figure keeps the session ranks reached by at least this many participants
# (`MIN_SUBJECTS_PER_SESSION` in the submodule's notebook).
MIN_SUBJECTS_PER_SESSION = 5

# The slope table's row for each participant's trajectory over all regions.
ALL_REGIONS = "all"

NETWORK_LABEL = {
    "Vis": "Visual",
    "SomMot": "Somatomotor",
    "DorsAttn": "Dorsal Attention",
    "SalVentAttn": "Salience/Ventral Attention",
    "Limbic": "Limbic",
    "Cont": "Control",
    "Default": "Default",
    "cerebellum": "cerebellum",
    "subcortex": "subcortex",
}


class Text(str):
    """A string that renders inline without quotes (its repr is itself)."""

    def __repr__(self):
        return str(self)


def find_output_data(start=None):
    """Locate the submodule's output tables, whatever the build's working directory."""
    here = Path(start or Path.cwd()).resolve()
    for base in [here, *here.parents]:
        candidate = base / OUTPUT_DATA
        if (candidate / "stability_per_region.tsv").is_file():
            return candidate
    raise FileNotFoundError(
        f"{OUTPUT_DATA} not found. Initialize the submodule with "
        "`git submodule update --init source_data/anat_stability`."
    )


def percent(value, digits=1):
    """A fraction as a percentage, e.g. 0.0138 -> '1.4'."""
    return Text(f"{100 * value:.{digits}f}")


def signed(value, digits=2):
    """Typographic sign, e.g. -1.16 -> '−1.16', 1.45 -> '+1.45'."""
    return Text(f"{value:+.{digits}f}".replace("-", "−"))


def join_names(names):
    """'a', 'a and b', 'a, b, and c'."""
    names = list(names)
    if len(names) <= 2:
        return Text(" and ".join(names))
    return Text(", ".join(names[:-1]) + ", and " + names[-1])


class AnatStats:
    """Read-only accessor over the anat_stability output tables."""

    def __init__(self, output_data=None):
        self.output_data = Path(output_data) if output_data else find_output_data()
        read = lambda name: pd.read_csv(self.output_data / f"{name}.tsv", sep="\t")  # noqa: E731
        self.regions = read("stability_per_region")
        self.trajectories = read("volume_trajectories")
        slopes = read("trajectory_slopes")
        self.subject_slopes = slopes.query("network == @ALL_REGIONS").set_index("subject")
        self.network_slopes = slopes.query("network != @ALL_REGIONS")

    # --- sample ---------------------------------------------------------------------

    @property
    def n_subjects(self):
        return Text(str(len(self.subject_slopes)))

    @property
    def n_sessions(self):
        return Text(str(self.subject_slopes["n_sessions"].sum()))

    @property
    def sessions_range(self):
        """'5–15': fewest to most anatomical sessions per participant."""
        n = self.subject_slopes["n_sessions"]
        return Text(f"{n.min()}–{n.max()}")

    @property
    def n_regions(self):
        return Text(str(len(self.regions)))

    def n_regions_in(self, network):
        return Text(str(int((self.regions["network"] == network).sum())))

    def label(self, network):
        """Prose name of a network ('Vis' -> 'Visual')."""
        return Text(NETWORK_LABEL[network])

    # --- within- vs between-subject variation (panel D) ------------------------------

    def cv(self, which="intra", digits=1):
        """Median over regions of the within- ('intra') or between-subject ('inter') CV, in %."""
        return percent(self.regions[f"{which}_subject_cv"].median(), digits)

    def network_cv(self):
        """Median CV over each network's regions, most stable (lowest within-subject CV) first."""
        table = self.regions.groupby("network")[["intra_subject_cv", "inter_subject_cv"]].median()
        return table.sort_values("intra_subject_cv")

    def network_cv_extreme(self, which="intra", end="min", digits=2):
        """'0.75% (cerebellum)'-style phrase for the lowest or highest network median CV."""
        column = self.network_cv()[f"{which}_subject_cv"].sort_values()
        network = column.index[0] if end == "min" else column.index[-1]
        return Text(f"{percent(column[network], digits)}% ({NETWORK_LABEL[network]})")

    @property
    def n_regions_intra_below_inter(self):
        below = self.regions["intra_subject_cv"] < self.regions["inter_subject_cv"]
        return Text(str(int(below.sum())))

    @property
    def stability_order(self):
        """Networks from most to least stable, as prose names."""
        return [NETWORK_LABEL[n] for n in self.network_cv().index]

    # --- volume over sessions (panel B) -----------------------------------------------

    @property
    def kept_sessions(self):
        """Session ranks reached by enough participants to be shown in panel B."""
        rows = self.trajectories.query("n_subjects >= @MIN_SUBJECTS_PER_SESSION")
        return sorted(rows["session_rank"].unique())

    @property
    def last_session(self):
        return Text(str(self.kept_sessions[-1]))

    def _curve(self):
        return self.trajectories.pivot(index="network", columns="session_rank",
                                       values="mean_deviation_pct")

    def deviation(self, network, session, digits=2):
        """Mean deviation (%) of a network from participants' own mean, at a session rank."""
        return signed(self._curve().loc[network, session], digits)

    def network_drop(self):
        """Per-network fall in percentage points, first to last shown session, smallest first."""
        curve = self._curve()
        return (curve[1] - curve[self.kept_sessions[-1]]).sort_values()

    def network_drop_extreme(self, end="min", digits=1):
        """'1.0 (subcortex)'-style phrase for the smallest or largest network decline."""
        drop = self.network_drop()
        network = drop.index[0] if end == "min" else drop.index[-1]
        return Text(f"{drop[network]:.{digits}f} ({NETWORK_LABEL[network]})")

    # --- per-participant slopes (panel C) ---------------------------------------------

    def slope_extreme(self, end="min", digits=2):
        """'−0.10% per session (sub-01)'-style phrase for the shallowest or steepest all-region slope."""
        slopes = self.subject_slopes["slope_pct_per_session"].round(digits)
        target = slopes.max() if end == "min" else slopes.min()
        subjects = sorted(slopes.index[slopes == target])
        return Text(f"{signed(target, digits)}% per session ({', '.join(subjects)})")

    @property
    def n_subjects_declining(self):
        return Text(str(int((self.subject_slopes["slope_pct_per_session"] < 0).sum())))

    @property
    def n_trajectories(self):
        return Text(str(len(self.network_slopes)))

    @property
    def n_trajectories_declining(self):
        return Text(str(int((self.network_slopes["slope_pct_per_session"] < 0).sum())))

    @property
    def non_declining(self):
        """Subject x network trajectories with a non-negative slope."""
        return self.network_slopes.query("slope_pct_per_session >= 0")

    def non_declining_phrase(self, digits=2):
        """'DorsAttn and subcortex (+0.04 and +0.03 % per session)'-style phrase."""
        rows = self.non_declining
        networks = join_names(NETWORK_LABEL[n] for n in rows["network"])
        values = join_names(signed(v, digits) for v in rows["slope_pct_per_session"])
        return Text(f"{networks} ({values}% per session)")

    @property
    def non_declining_subjects(self):
        return join_names(sorted(self.non_declining["subject"].unique()))

    def subject_sessions(self, subject):
        return Text(str(self.subject_slopes.loc[subject, "n_sessions"]))


ANAT = AnatStats()


if __name__ == "__main__":
    a = ANAT
    print(f"source:          {a.output_data}")
    print(f"sample:          {a.n_subjects} subjects, {a.n_sessions} sessions ({a.sessions_range}), "
          f"{a.n_regions} regions")
    print(f"median CV:       {a.cv('intra')}% within vs {a.cv('inter')}% between")
    print(f"network intra:   {a.network_cv_extreme('intra', 'min')} to {a.network_cv_extreme('intra', 'max')}")
    print(f"network inter:   {a.network_cv_extreme('inter', 'min')} to {a.network_cv_extreme('inter', 'max')}")
    print(f"intra < inter:   {a.n_regions_intra_below_inter}/{a.n_regions}")
    print(f"stability order: {a.stability_order}")
    print(f"sessions shown:  1–{a.last_session}")
    print(f"network drop:    {a.network_drop_extreme('min')} to {a.network_drop_extreme('max')} pp")
    print(f"Default:         {a.deviation('Default', 1)} to {a.deviation('Default', a.kept_sessions[-1])}")
    print(f"subject slopes:  {a.slope_extreme('min')} to {a.slope_extreme('max')}, "
          f"{a.n_subjects_declining}/{a.n_subjects} declining")
    print(f"trajectories:    {a.n_trajectories_declining}/{a.n_trajectories} declining; "
          f"exceptions {a.non_declining_phrase()} in {a.non_declining_subjects}")
