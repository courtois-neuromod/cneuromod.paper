"""Live connectome stability statistics for the paper prose.

Every number is read from the aggregate tables produced by the `connectome_stats`
submodule's pipeline (`uv run invoke run` inside it), which is where per-session
connectomes are compared and summarized into medians:

    source_data/connectome_stats/output_data/group_stats/session_gate.tsv
    source_data/connectome_stats/output_data/group_stats/cross_context.tsv
    source_data/connectome_stats/output_data/group_stats/duration_balance.tsv
    source_data/connectome_stats/output_data/group_stats/longitudinal_lag.tsv
    source_data/connectome_stats/output_data/group_stats/longitudinal_lag_subject.tsv
    source_data/connectome_stats/output_data/group_stats/network_quality.tsv
    source_data/connectome_stats/output_data/group_stats/domain_cross_context.tsv
    source_data/connectome_stats/output_data/group_stats/domain_duration_balance.tsv

The helpers below select values and do only light arithmetic on the published medians
(differences between two lags or bins, means across the nine networks, counts of networks
where an ordering holds), and format them to read naturally inline.

Usage in a paper `.md` file:

    ```{code-cell} python3
    :tags: [remove-cell]
    import sys
    from pathlib import Path
    sys.path.insert(0, str(next(p for p in (Path("paper"), Path(".")) if (p / "_connectome_stats.py").exists())))
    from _connectome_stats import CONN
    ```

    ... computed for {eval}`CONN.n_sessions()` sessions ...
"""

from pathlib import Path

import pandas as pd

GROUP_STATS = Path("source_data/connectome_stats/output_data/group_stats")

MEASURE = "pearson"

# The four session-pair bins, in the order the paper's ordering claim states them.
BINS = (
    "within-subject / within-dataset",
    "within-subject / between-dataset",
    "between-subject / within-dataset",
    "between-subject / between-dataset",
)

# Domain membership as defined upstream (`DOMAIN_DATASETS` in connectome_stats'
# analysis/group_stats.py). A definition, not a statistic: which of these datasets
# actually contribute is read from the tables (`domain_datasets`).
DOMAIN_DATASETS = {
    "movies": ("friends", "movie10"),
    "videogames": ("mario", "mario3", "mariostars", "shinobi"),
    "stories": ("harrypotter", "petit-prince"),
    "taskscapes": ("emotion-videos", "triplets", "multfs", "things"),
    "localizers": ("hcptrt", "floc", "langlocalizer", "retinotopy"),
}

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


def find_group_stats(start=None):
    """Locate the group_stats tables, whatever the build's working directory."""
    here = Path(start or Path.cwd()).resolve()
    for base in [here, *here.parents]:
        candidate = base / GROUP_STATS
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(
        f"{GROUP_STATS} not found. Initialize the submodule with "
        "`git submodule update --init source_data/connectome_stats`."
    )


def num(value, digits=3):
    return Text(f"{value:.{digits}f}")


def count(value):
    return Text(f"{int(value):,}")


def join_names(names):
    """'a', 'a and b', 'a, b, and c'."""
    names = list(names)
    if len(names) <= 2:
        return Text(" and ".join(names))
    return Text(", ".join(names[:-1]) + ", and " + names[-1])


class ConnectomeStats:
    """Read-only accessor over the connectome_stats group tables."""

    def __init__(self, group_stats=None):
        self.group_stats = Path(group_stats) if group_stats else find_group_stats()
        read = lambda name: pd.read_csv(  # noqa: E731
            self.group_stats / f"{name}.tsv", sep="\t", dtype={"subject": str}
        )
        self.session_gate = read("session_gate").set_index("dataset")
        self.cross_context = read("cross_context").query("measure == @MEASURE")
        self.duration_table = read("duration_balance")
        self.lag = read("longitudinal_lag").query("measure == @MEASURE and lag_type == 'season'")
        self.lag_subject = read("longitudinal_lag_subject").query("measure == @MEASURE")
        self.quality = read("network_quality").set_index("network")
        self.domain = read("domain_cross_context").query("measure == @MEASURE")
        self.domain_duration_table = read("domain_duration_balance")

    # --- sessions and datasets ------------------------------------------------------

    def n_sessions(self, gate="all"):
        column = "n_sessions" if gate == "all" else "n_passing"
        return count(self.session_gate[column].sum())

    def datasets(self, gate="all"):
        """Datasets with at least one session (gate='all') or one gated session."""
        column = "n_sessions" if gate == "all" else "n_passing"
        return sorted(self.session_gate.index[self.session_gate[column] > 0])

    @property
    def gated_out(self):
        """Datasets with no session above the usable-data gate."""
        return sorted(self.session_gate.index[self.session_gate["n_passing"] == 0])

    # --- longitudinal (friends seasons) ---------------------------------------------

    def _season_curve(self, pair_type="within-subject", gate="gated"):
        rows = self.lag.query("pair_type == @pair_type and gate == @gate")
        return rows.pivot(index="network", columns="lag_value", values="median")

    def season(self, network, lag, digits=3):
        """Within-subject similarity of one network at a given season lag."""
        return num(self._season_curve().loc[network, lag], digits)

    @property
    def max_lag(self):
        return int(self._season_curve().columns.max())

    def season_drop(self):
        """Per-network drop in within-subject similarity, lag 0 to the maximum lag."""
        curve = self._season_curve()
        return (curve[0] - curve[self.max_lag]).sort_values()

    def season_drop_extreme(self, which="min", digits=3):
        """'0.019 (cerebellum)'-style phrase for the smallest or largest drop."""
        drop = self.season_drop()
        network = drop.index[0] if which == "min" else drop.index[-1]
        return Text(f"{drop[network]:.{digits}f} ({NETWORK_LABEL[network]})")

    def floor(self, lag, digits=3):
        """Between-subject similarity at a season lag, median across networks (panel A's grey curve)."""
        return num(self._season_curve("between-subject")[lag].median(), digits)

    def _subject_curve(self, gate="gated"):
        rows = self.lag_subject.query("gate == @gate")
        return rows.pivot_table(index=["subject", "network"], columns="lag_value", values="median")

    def subject_drop_percent(self):
        """Per-subject % drop of the network-averaged curve, lag 0 to its last lag."""
        curve = self._subject_curve().groupby("subject").mean()
        last = curve.apply(lambda row: row.dropna().iloc[-1], axis=1)
        return 100 * (curve[0] - last) / curve[0]

    def subject_drop_range(self, digits=0):
        drop = self.subject_drop_percent()
        return Text(f"{drop.min():.{digits}f}–{drop.max():.{digits}f}")

    @property
    def n_subjects(self):
        return Text(str(len(self.subject_drop_percent())))

    def declining_cells(self):
        """(n network x subject cells that decline from lag 0 to their last lag, n cells)."""
        curve = self._subject_curve()
        last = curve.apply(lambda row: row.dropna().iloc[-1], axis=1)
        return int((curve[0] > last).sum()), len(curve)

    # --- cross-context (panel D) ----------------------------------------------------

    def _bins(self, table, gate):
        rows = table.query("gate == @gate")
        pivot = rows.pivot(index="network", columns="bin", values="median")
        within_within, within_between, between_within, between_between = [
            next(c for c in pivot.columns if c.startswith(prefix))
            for prefix in (
                "within-subject / within",
                "within-subject / between",
                "between-subject / within",
                "between-subject / between",
            )
        ]
        return pivot[[within_within, within_between, between_within, between_between]]

    def bins(self, network, gate="gated", digits=2):
        """'0.95/0.77/0.69/0.61' — the four bins of one network, in BINS order."""
        values = self._bins(self.cross_context, gate).loc[network]
        return Text("/".join(f"{v:.{digits}f}" for v in values))

    def n_networks_ordered(self, gate="gated"):
        """Networks where the full four-bin ordering holds."""
        b = self._bins(self.cross_context, gate)
        ok = (b.iloc[:, 0] > b.iloc[:, 1]) & (b.iloc[:, 1] > b.iloc[:, 2]) & (b.iloc[:, 2] > b.iloc[:, 3])
        return Text(str(int(ok.sum())))

    @property
    def n_networks(self):
        return Text(str(self.cross_context["network"].nunique()))

    def duration(self, bin, gate="gated"):
        """Median pair minimum duration (s) of one cross-context bin."""
        row = self.duration_table.query("gate == @gate and bin == @bin")
        return count(round(row["median_min_duration_sec"].iloc[0]))

    def duration_imbalance_percent(self, gate="gated"):
        """How much longer within-dataset pairs are than between-dataset ones, in %."""
        rows = self.duration_table.query("gate == @gate").set_index("bin")["median_min_duration_sec"]
        within = rows[[BINS[0], BINS[2]]].mean()
        between = rows[[BINS[1], BINS[3]]].mean()
        return Text(f"{100 * (within / between - 1):.0f}")

    # --- network quality (panel C) --------------------------------------------------

    def label(self, network):
        """Prose name of a network ('Vis' -> 'Visual')."""
        return Text(NETWORK_LABEL[network])

    def tsnr(self, network, digits=1):
        return num(self.quality.loc[network, "median_tsnr"], digits)

    def similarity(self, network, digits=3):
        return num(self.quality.loc[network, "within_subject_median_cross_context"], digits)

    def lowest(self, column="median_tsnr"):
        return Text(self.quality[column].idxmin())

    @property
    def n_tsnr_sessions(self):
        return count(self.quality["n_tsnr"].iloc[0])

    @property
    def tsnr_datasets(self):
        return self.quality["datasets"].iloc[0].split(",")

    # --- stimulus domains (panels E–I) ----------------------------------------------

    def domain_datasets(self, domain, gate="gated"):
        """Datasets of a domain that contribute at least one session under `gate`."""
        present = set(self.datasets(gate))
        return sorted(d for d in DOMAIN_DATASETS[domain] if d in present)

    def domain_sessions(self, domain, gate="gated"):
        rows = self.domain_duration_table.query("domain == @domain and gate == @gate")
        return count(rows["n_sessions"].iloc[0])

    def _domain_gap(self, domain, gate):
        b = self._bins(self.domain.query("domain == @domain"), gate)
        return b.iloc[:, 0] - b.iloc[:, 1]

    def domain_gap(self, domain, gate="gated", digits=3):
        """Within-task minus between-task within-subject similarity, mean over networks."""
        return num(self._domain_gap(domain, gate).mean(), digits)

    def domain_n_positive(self, domain, gate="gated"):
        return int((self._domain_gap(domain, gate) > 0).sum())

    def domain_duration(self, domain, which="within", gate="gated"):
        """Median pair minimum duration (s) of the within- or between-task, within-subject bin."""
        rows = self.domain_duration_table.query("domain == @domain and gate == @gate")
        prefix = f"within-subject / {which}"
        row = rows[rows["bin"].str.startswith(prefix)]
        return count(round(row["median_min_duration_sec"].iloc[0]))


CONN = ConnectomeStats()


if __name__ == "__main__":
    c = CONN
    print(f"source:            {c.group_stats}")
    print(f"sessions:          {c.n_sessions()} in {len(c.datasets())} datasets")
    print(f"gated:             {c.n_sessions('gated')} in {join_names(c.datasets('gated'))}")
    print(f"gated out:         {join_names(c.gated_out)}")
    print(f"season drop:       {c.season_drop_extreme('min')} to {c.season_drop_extreme('max')}")
    print(f"Vis:               {c.season('Vis', 0)} to {c.season('Vis', c.max_lag)}")
    print(f"floor:             {c.floor(0)} to {c.floor(c.max_lag)}")
    print(f"subject drop:      {c.subject_drop_range()}% over {c.n_subjects} subjects")
    print(f"declining cells:   {c.declining_cells()}")
    print(f"ordering holds:    {c.n_networks_ordered()}/{c.n_networks}")
    print(f"Vis / Default:     {c.bins('Vis')} ; {c.bins('Default')}")
    print(f"duration (s):      {[str(c.duration(b)) for b in BINS]}, +{c.duration_imbalance_percent()}%")
    print(f"lowest tSNR:       {c.lowest()} {c.tsnr(c.lowest())} / {c.similarity(c.lowest())}")
    print(f"tSNR sessions:     {c.n_tsnr_sessions} from {len(c.tsnr_datasets)} datasets")
    for domain, gate in [("movies", "gated"), ("videogames", "gated"), ("stories", "gated"),
                         ("taskscapes", "all"), ("localizers", "all")]:
        print(f"{domain:<18} {gate:<6} {c.domain_sessions(domain, gate):>4} sessions, "
              f"gap {c.domain_gap(domain, gate)}, {c.domain_n_positive(domain, gate)}/9, "
              f"dur {c.domain_duration(domain, 'within', gate)}/{c.domain_duration(domain, 'between', gate)} s, "
              f"{c.domain_datasets(domain, gate)}")
