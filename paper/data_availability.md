# Data Availability

## Deposit and distribution

All CNeuroMod data are distributed as DataLad datasets [MISSING REF: Halchenko et al.
2021, JOSS, DataLad] hosted under the
[`courtois-neuromod`](https://github.com/courtois-neuromod) GitHub organisation, with
annexed file content served from an Amazon S3 fileserver. The meta-dataset
[`cneuromod.all`](https://github.com/courtois-neuromod/cneuromod.all) is the single
entry point: it follows YODA principles and tracks every experimental paradigm as a
top-level folder containing independent submodules for each data component (raw BIDS,
fMRIPrep and sMRIPrep derivatives, MRIQC reports, PhysPrep physiological derivatives,
and dataset-specific content). Yearly release tags (e.g. `2020`) pin the state of all
submodule pointers, so any published analysis can be reproduced against the exact
version of the databank it used.

## Open access to five participants

Five of the six participants (`sub-01`, `sub-02`, `sub-03`, `sub-05`, `sub-06`) elected
to share their data without restriction. These data are deposited on the
[Canadian Open Neuroscience Platform (CONP)](https://portal.conp.ca/dataset?id=projects/cneuromod)
[MISSING REF: CONP platform paper] under a permissive Creative Commons license that
authorises redistribution of derivative works [MISSING REF: exact CC license variant to
be confirmed — the source documentation says only "a liberal Creative Commons data
license"]. No registration or agreement is required: the standard download procedure
retrieves all CONP-hosted content and simply warns about the files that remain
restricted. [MISSING REF: DOI for the CONP deposit.]

## Registered access to the complete databank

Access to the complete databank, including the sixth participant, is granted through a
registered-access procedure documented at
[cneuromod.ca/access](https://www.cneuromod.ca/access/access/). Applicants submit a
brief description of their planned analyses and an inter-institutional data transfer
agreement (DTA) signed both by the researcher responsible for the project and by a
representative of their academic institution. Applications are reviewed by a data access
committee; approved teams receive S3 credentials from the CNeuroMod data manager,
which unlock the restricted content through the same DataLad interface.

## Downloading

Data are retrieved by cloning `cneuromod.all`, installing the submodules of interest,
and fetching file content with `datalad get`; existing clones are updated with
`datalad update -r --merge --reobtain-data`. Recursive installation of the full
meta-dataset is discouraged, as submodules re-expose their own sub-submodules at
differing versions for provenance tracking. Complete, up-to-date instructions —
including prerequisites, credential setup, and partial-download recipes — are
maintained at [docs.cneuromod.ca](https://docs.cneuromod.ca).

## Ethics

The Courtois NeuroMod project was approved by the research ethics board of the CIUSSS du
Centre-Sud-de-l'Île-de-Montréal, most recently renewed on 21 October 2022 by the Comité
d'éthique de la recherche — Vieillissement et neuroimagerie (CER-VN) under project
number CER VN 18-19-22. All participants gave written informed consent, and consented
explicitly to the public sharing of their data under the terms described above. The
consent forms (English and French) and the project description are available from the
project documentation; the formal ethics authorisation letter is available upon request.
