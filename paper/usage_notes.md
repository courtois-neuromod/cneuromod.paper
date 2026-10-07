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
The benchmark has remained open after the challenge closed. MIRAGE, submitted to the
official evaluation platform after the competition, replaced the separate unimodal feature
extractors with a single natively multimodal foundation model, and an ensemble of its
models reached 0.323 on the held-out season and 0.227 on the out-of-distribution films,
above the top challenge entries {cite:p}`Gokce2026-ja`.

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

Videogames extend brain encoding to active, goal-directed behaviour. In `shinobi` and `mario`,
participants play with an MRI-compatible controller {cite:p}`harel2023gamepad`, and every
frame and button press is recorded alongside fMRI. Behaviour this rich can be learned by an
artificial agent, which can then be asked to imitate both a participant's play and that
participant's brain activity.

In `shinobi`, agents trained by imitation learning to reproduce one participant's play style
predicted that participant's brain activity better than agents trained on other participants'
gameplay or than control models, most strongly in somatosensory, attention and visual networks
{cite:p}`Kemtur2023-px`. Videogames thus support personalized models of behaviour and brain
at once.

Gameplay can also be described without an agent. Annotations of player actions and game
feedback, extracted automatically from the emulator's memory states, predicted activity in
visual, motor, executive and limbic systems {cite:p}`harel2026gamer`. This makes event-related
analyses of complex play possible without manual coding.

Fitting the brain is not enough: models must also generalize. In `mario`, agents trained from
scratch with reinforcement learning, imitation learning or a vision objective were compared on
brain encoding {cite:p}`Paugam2025-oq`. Reinforcement learning had a small advantage, but an
untrained network of the same architecture came close, and all models generalized poorly to
new levels. `mario` is therefore a benchmark for the robustness and out-of-distribution
generalization of brain encoding models in active tasks. Its high-resolution gameplay also
supports a continual-learning benchmark comparing human and agent learning trajectories
{cite:p}`Harel2025-gl`.

---

## 3. Towards Better AI with Neural Data

Brain encoding uses AI models to explain the brain. The reverse question is whether brain
data can improve AI models. Neuroscience has been proposed as a source of inductive biases
for more robust and safer AI, and fine-tuning AI systems directly on brain recordings is one
of the routes considered {cite:p}`Mineault2024-ai`. The bottleneck is data: brain recordings
are collected at a much smaller scale than the data used to train AI models. With tens of
hours of fMRI per participant for the same stimuli, CNeuroMod makes this "brain-tuning"
feasible.

Brain-tuning first improves brain encoding itself. Fine-tuning SoundNet, a small audio
network of about 2.5M parameters, on three seasons of `friends` improved brain encoding on a
fourth, unseen season, beyond auditory and visual cortices, and individual models often
matched or outperformed group models {cite:p}`Freteault2025-tx`. Language models fine-tuned
with a brain alignment module on more than 50 hours of `friends` showed encoding gains that
grew with model size (GPT-2 to LLaMA-2 7B) and with training duration (1–40 hours), and
that generalized to held-out movies and participants {cite:p}`Bilgin2025-xz`. RABBiT, a
compact audio-to-fMRI encoder with a brain-tuned speech backbone trained on `friends`
(about 39 hours per participant), predicted responses to speech in 324 new participants from
other datasets without any participant-specific data, better than group averages. Ten
minutes of data from a new participant were enough to outperform per-participant linear
models {cite:p}`Moussa2026-ft`.

Brain-tuning also transfers to AI tasks. Brain-aligned SoundNet improved on the HEAR battery
of auditory tasks, most for tasks with little training data, where it performed comparably
to much larger models {cite:p}`Freteault2025-tx`. Brain-tuned language models better
captured perceptual properties such as colour and shape {cite:p}`Bilgin2025-xz`, and
brain-tuning a multimodal audio-video model on the superior temporal sulcus during
`friends` improved sarcasm detection in sitcoms {cite:p}`Policzer2025-ja`. Brain
organization can even serve as an architectural prior. The Platonic brain bridge hypothesis
proposes that omni models, which process video, audio and text jointly, converge on
brain-like representations {cite:p}`Zhang2026-zn`. Encoders built on such models ranked
first on the post-challenge Algonauts 2025 leaderboard. In the other direction, Brain-MoE
assigns the experts of a frozen omni model to the seven canonical cortical networks, trains
each on questions labelled by the network most engaged in `friends` fMRI, and raised
held-out accuracy in all 15 model–benchmark pairs, by 6.4 percentage points on average.

Brain-tuning is not yet a routine recipe. During the Algonauts 2025 challenge, one team
fine-tuned language and vision backbones on the brain data. The gains were modest, and for a
stimulus-tuned language model they did not carry over to the out-of-distribution films. The
authors noted that a more comprehensive selection of hyperparameters could have helped, but
was out of reach within the time and compute of the competition {cite:p}`Scholz2025-io`.
Downstream evaluation is the proper test of these approaches. Brain data will remain small
compared to the parameter counts of modern models, so the relevant benchmark is not scale
but data efficiency: how much a fixed, modest amount of brain data improves a model on tasks
where training data are scarce, compared with controls of matched capacity, such as the
random experts used for Brain-MoE. Direct fine-tuning is also only one way to use brain
data to improve AI models. Brain-MoE uses it instead to structure a model and to label its
training data, and such indirect uses remain largely unexplored. The depth of CNeuroMod per participant and the diversity of
its tasks make it a testbed for these comparisons.

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
