# Usage Notes

The CNeuroMod dataset has been used in a growing body of research spanning brain encoding, brain decoding, cognitive neuroscience, and AI alignment with neural data. This section provides an overview of key research directions enabled by the dataset and practical guidance for new users.

:::{figure} ../source_data/reuse_stats/output_data/figure_montage.png
:name: fig-reuse
:width: 100%

**Reuse of the CNeuroMod dataset.** Number of papers using CNeuroMod data, by year and
publication type (journal article, conference paper, preprint, thesis, book chapter),
computed from the curated reference list of the `cneuromod.all` repository. Undated entries
are not shown.
:::

## 1. Individual Brain Encoding Models

CNeuroMod has emerged as a key resource for building multimodal encoding models of
individual brains, accelerated by the Algonauts Project 2025 Challenge. This open
competition invited participants to predict fMRI responses in 1,000 cortical parcels from
multimodal movie features. Training used about 65 hours of movies, watched by each of four
participants: seasons 1–6 of `friends` and the four `movie10` films. Brain responses were
withheld for two test sets: season 7 of `friends` (in distribution) and six
out-of-distribution videos (`ood`), the latter deciding the winners
{cite:p}`gifford2025algonauts`.

The top-ranked entries, all multimodal, were closely matched on the out-of-distribution
films. TRIBE, ranked first, combined pretrained text, audio and video foundation models
with a multimodal AI-to-brain transformer, and reached a mean parcel-wise correlation of
0.320 on the held-out season and 0.215 on the out-of-distribution films. Its ablations
showed that unimodal models reliably predict their own sensory networks but are
systematically outperformed by the multimodal model in high-level associative cortices
{cite:p}`d-Ascoli2026-hf`. The second- and third-ranked models, built on transformers and
on recurrent networks, scored 0.210 and 0.209 on the out-of-distribution films
{cite:p}`Schad2025-pz,Eren2025-xi`, and further entries replicated these levels of
performance across a wide range of architectures
{cite:p}`Villanueva2025-aw,He2025-vt,Corsico2025-si,Scholz2025-io`.

Brain encoding can also be combined with models of the brain's own dynamics. Individual
auto-regressive models of BOLD dynamics trained on movie watching kept improving with more
data, with no complete saturation at 9 hours of training data. They generalized to other
video stimuli and to resting state, and their predicted dynamics reproduced classical
functional connectivity networks {cite:p}`Paugam2024-jo`. NeuroWorld brings the two
together in a "brain world model": a latent brain state evolves auto-regressively, driven
only by past brain activity and by the stimulus seen so far, and is decoded back into
individual fMRI responses {cite:p}`Dong2026-ol`. Under this strictly causal protocol,
starting from a single observed fMRI time point, it predicted the next 20 time points of
the Algonauts 2025 data more accurately than causal versions of TRIBE-style encoders, and
degraded only slowly over rollouts of up to 2.5 minutes.

## 2. Brain Encoding Models of the Active Brain

[Overview: CNeuroMod's active tasks — particularly videogame paradigms — enable a new class of encoding models that capture brain activity during goal-directed, embodied behavior.]

### Atari Games

[Discuss Cross et al. and Tomov et al. using Atari game stimuli for brain encoding. Summarize key findings linking RL agent representations to neural activity. Add citations.]

### Videogame Controller and Motor Signals

[Discuss Harel et al. (PLOS ONE) examining controller inputs and neural correlates. Summarize findings on motor and planning signals in fMRI. Add citation.]

### Clean BOLD Signal in Active Tasks

[Describe Harel et al. (Imaging Neuroscience) demonstrating that high-quality BOLD signal is recoverable during active gameplay despite motion and arousal confounds. Add citation.]

### Imitation Learning in the Brain

In `shinobi`, artificial agents trained by imitation learning to reproduce one
participant's play style predicted that participant's brain activity better than agents
trained on other participants' gameplay {cite:p}`Kemtur2023-px`.

### Artificial Agents in Mario

In `mario`, artificial agents trained on the same game with reinforcement learning,
imitation learning or a vision objective were compared on brain encoding of new
playthroughs {cite:p}`Paugam2025-oq`. Reinforcement learning had a small but significant
advantage, and encoding improved over training. All models generalized poorly to new
levels, which makes `mario` a benchmark for out-of-distribution generalization in active
tasks.

### Learning Trajectories in Mario

High-resolution human gameplay from `mario` forms the basis of a continual-learning
benchmark comparing human and agent learning trajectories {cite:p}`Harel2025-gl`.

[Expand: how neural representations evolve as subjects learn to play Super Mario Bros. Note this as a major area for future competitions.]

---

## 3. Towards Better AI with Neural Data

[Overview: Growing excitement in the ML community about using neural recordings as a source of inductive biases or alignment signals for AI models.]

### The Case for Neuro-Aligned AI

[Reference Mineault et al. white paper and recent review articles arguing for integrating neural data into AI training pipelines. Summarize the main arguments.]

### SoundNet Trained on Neural Data

Fine-tuning an audio network on three seasons of *Friends* improved brain encoding on a
fourth, unseen season, beyond auditory and visual cortices. Individual models often matched
or outperformed group models {cite:p}`Freteault2025-tx`.

### Brain-Informed Fine-Tuning of Language Models

Brain-informed fine-tuning of language models on more than 50 hours of *Friends* produced
encoding gains that grew with model size and with training duration (1–40 hours), and that
generalized to held-out movies and participants {cite:p}`Bilgin2025-xz`.

### Rabbit and the platonic bridge hypothesis

### Challenges and Proper Downstream Evaluation

[Discuss the challenge of limited neural data relative to large model parameter counts. Argue that benchmarking on fine-tuning on small datasets is more meaningful than competing on large-scale benchmarks with unconstrained compute. Provide practical recommendations for future neuro-AI work using CNeuroMod.]

---

## 4. Brain Decoding

[Overview: CNeuroMod supports brain decoding — reconstructing stimuli or mental states from neural activity — across multiple modalities and task types.]

### Decoding with the Shinobi Dataset

[Describe Shima et al. (Imaging Neuroscience) using the Shinobi videogame fMRI dataset for brain decoding. Summarize what was decoded (game state? actions? rewards?) and key findings. Add citation.]

### Expanding the Space of Brain Decoding

[Explain how the breadth of CNeuroMod stimuli and tasks greatly expands the stimulus and cognitive spaces available for decoding, beyond the traditional image/language domains.]

### Upcoming Benchmarks

[Preview the triplets dataset (for word-level semantic decoding) and the MultiFS working memory dataset as upcoming resources that will open new decoding benchmarks for the community.]

---

## 5. Cognitive Neuroscience and Naturalistic Annotations

[Overview: CNeuroMod naturalistic stimuli, combined with rich semantic annotations, support traditional cognitive neuroscience questions about emotion, memory, language, and social cognition.]

### Emotion Annotations in Friends

[Highlight recent works using emotional annotations synchronized with the Friends TV show fMRI data. Summarize the types of annotations available and key cognitive neuroscience findings. Add citations.]

### Language Comprehension

`harrypotter` reproduces, in five CNeuroMod participants, the word-by-word reading paradigm
of an existing fMRI dataset. A study using brain encoding of a computational representation
of composed, "supra-word" meaning found that hubs thought to process lexical meaning also
maintain supra-word meaning {cite:p}`Toneva2022-bf`. A methods paper from the same group
tested its inferences on two fMRI datasets with naturalistic stimuli and found them
strikingly consistent between the two {cite:p}`Toneva2022-vu`.

% TODO: confirm which fMRI datasets Toneva2022-vu used.

### Large-Scale Annotation Efforts

[Describe the team's ongoing effort to release large-scale annotations of naturalistic stimuli, including Friends and Mario scenes (scene segmentation, character identity, emotional valence, actions, etc.). Explain how these annotations will enable purely cognitive neuroscience-driven analyses without requiring ML expertise.]

---

## 6. Foundation Models and the Digital Brain

CNeuroMod was designed around a deliberate bet: model a few individuals in depth before
attempting to model humanity at large. Six participants is a small sample by the standards
of population neuroscience, but a sample of many people cannot answer the question
CNeuroMod targets: can a model reproduce one specific brain across a wide range of
cognitive functions? Answering it requires many hours of data from the same person,
recorded under many different tasks. The work reviewed above shows that this works.
Individual models trained on CNeuroMod predict brain activity for new stimuli, improve with
more data from the same person, and often match or outperform group models. Through the
Algonauts 2025 challenge, the dataset also became a shared benchmark that teams outside the
project could build on.

### The Digital Brain Project

This bet is now being scaled up. Building on CNeuroMod, the
[Digital Brain Project](https://digitalbrainproject.org/) aims to "build a functional model
of the human brain" from neural recordings acquired during complex, interactive tasks. With
US$15M in funding from Meta, coordinated by the Rothschild Hospital Foundation with the
Université de Montréal as advisory partner, it will collect 15,000 hours of brain activity
across nine inaugural teams in Switzerland, the USA, Canada and France. It follows the same
design principle as CNeuroMod: "a few subjects over many sessions, building dense
individual brain maps", with open release of deidentified data in BIDS format.
CNeuroMod is one of its two contributing labs. Its infrastructure — standardized formats,
versioned datasets and reproducible processing pipelines — provides a template for
collecting and sharing data at this scale.

### TRIBE v2: towards a foundation model of brain responses

Modelling work is scaling up in the same way. TRIBE, the model that won Algonauts 2025, was
trained only on CNeuroMod: seasons 1–6 of *Friends* and the four `movie10` films, more
than 80 hours of fMRI per participant {cite:p}`d-Ascoli2026-hf`. Its encoding accuracy
rose steadily with the amount of training data and had not reached a plateau. Its
successor, TRIBE v2, aims to be a foundation model of brain responses to video, audio and
language. It combines CNeuroMod with three other deeply sampled training datasets and is
evaluated on new stimuli, tasks and participants across more than 1,000 hours of fMRI from
720 participants {cite:p}`dascoli2026tribev2`. CNeuroMod supplies most of this training
data: 268.7 of the 451.6 training hours of fMRI and 54k of the 59k training sentences.
It is also the only training dataset that combines video, audio and text. Encoding
accuracy across CNeuroMod again rose log-linearly with training data, without a plateau.
The paper does not report an ablation that measures how much the other training datasets
add, so CNeuroMod's share of the model's performance remains to be quantified.

### Extending CNeuroMod across recording modalities

CNeuroMod itself is expanding across recording modalities. A magnetoencephalography (MEG)
extension is about to be collected: about 10 hours of MEG per participant for five
participants, covering most CNeuroMod tasks with a reduced set of stimuli. The tasks of the
Digital Brain Project will also be recorded in `sub-01` with both EEG and MEG. Together,
these extensions will give the same tasks in the same individuals with complementary
temporal and spatial resolution, a resource for building individual brain models that
generalize across recording modalities as well as across stimuli and tasks.

### Optimal Transport for Data-Efficient Alignment

[Discuss the opportunity to apply optimal transport (OT) methods for aligning neural representations across subjects and datasets in a data-efficient manner. Reference work from Aimy Wenegrat's lab and the INRIA DANDI team. Explain why OT is particularly well-suited to the small-N, high-dimensional regime of deep phenotyping datasets like CNeuroMod.]

---

## Accessing the Data

[Instructions for requesting access and downloading data via the CNeuroMod data portal. Include links to the data agreement, DataLad/datalad-cneuromod repository, and OpenNeuro/OSF deposits where applicable.]

## Known Limitations

[Describe known issues: small N (6 subjects), site-specific scanner characteristics, missing sessions for some subjects/tasks, motion in active paradigms, and task-specific exclusion criteria. Refer readers to the Data Record section for per-dataset details.]

## Recommended Practices

[Suggest best practices: use fMRIPrep outputs, leverage provided confound regressors, cite the relevant task papers when using specific datasets, check the CNeuroMod documentation for versioned data releases.]
