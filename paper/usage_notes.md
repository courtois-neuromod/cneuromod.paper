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

Brain decoding reverses the direction of encoding: it infers a stimulus or a cognitive state
from a pattern of brain activity. Functional brain organization varies substantially across
individuals, so decoders are usually trained on large groups of participants, at the cost of
blurring individual signatures. Deeply sampled participants offer the alternative of training
a decoder entirely within one brain, and CNeuroMod has enough repetitions of the same
conditions to do so.

`hcptrt` puts this to the test on the Human Connectome Project task battery, a popular group
decoding benchmark, repeated many times in each participant. Individual decoders classified
single fMRI volumes (1.49 s) into 21 conditions, the setting closest to decoding a
continuous, naturalistic experience in real time {cite:p}`Rastegarnia2023-qz`. With about
7 hours of data per participant, they approached the accuracy of group models trained on
more than 1,000 hours from the original HCP sample. They also learned individual-specific
features: accuracy dropped sharply when a decoder was applied to another participant, and
models trained on the other participants did not match the participant's own model.

Decoding is not limited to blocked designs. In `shinobi`, events annotated automatically
from the emulator's memory, such as player actions, killing an enemy or losing health, were
modelled session by session, together with the `hcptrt` conditions of the same participants
{cite:p}`harel2026gamer`. A linear classifier separated 27 types of maps, with
leave-one-session-out accuracy of 0.98 for killing an enemy and hitting, and above 0.9 for
most other game events. Rare events were decoded less reliably, down to 0.36 for health
losses in one participant, and errors mostly confused game events with each other or with
the motor task. Different aspects of a single continuous game thus evoked patterns as
distinct as those of separate cognitive tasks.

These studies decoded a closed set of conditions. The breadth of CNeuroMod opens larger
decoding spaces in the same individuals: thousands of object images in `things`
{cite:p}`St-Laurent2026-zc`, hours of continuous movies and dialogue in `friends` and
`movie10`, and gameplay in `shinobi` and `mario`, where stimulus and behaviour are recorded
frame by frame. Labels generated automatically from the stimuli can then define what to
decode. In `friends`, the dialogue was labelled as positive, neutral or negative from the
audio, with a speech emotion model, and from the subtitles, with text sentiment tools
{cite:p}`Corsico2026-hy`. Acoustic and combined sentiment labels tracked activity in the
salience and default mode networks better than subtitle-based labels, whose effects were
weaker and more localized. Upcoming datasets will add new benchmarks, such as word-level semantic
decoding with `triplets`, built on a published set of word triplets with human similarity
judgments {cite:p}`Borghesani2023-me`, and working memory with `multfs`, amongst others.

% TODO: confirm the content of multfs (no README in cneuromod.all yet).

---

## 5. Cognitive Neuroscience and Naturalistic Annotations

The research directions above use AI models to explain, predict or decode brain activity.
CNeuroMod also supports classic cognitive neuroscience questions about perception, emotion,
memory and language, increasingly asked with naturalistic stimuli. A movie or a game has no
experimental design set in advance: it has to be recovered from the stimulus. Annotations,
which describe what happens moment by moment, turn a naturalistic stimulus into a design that
standard tools, such as the general linear model, can analyse.

Movies are a natural testbed for how the brain combines what is seen and heard. Comparing
how well auditory and visual features predict each region over time revealed two
complementary organizations: regions that switch between modalities, arranged in a posterior
and an anterior "bow", and an axis of regions represented by both modalities, from lateral
occipital into temporal cortex {cite:p}`Pushpita2025-mr`. Functional connectivity during
naturalistic viewing localized a compact, replicable subnetwork of parcels critical for
multimodal integration {cite:p}`Fokin2025-ys`. Full-length movies also probe the timescale
of integration: short clips aligned with perceptual and early language regions, and longer
clips with higher-order integrative regions {cite:p}`Jindal2026-tr`.

Long narratives make it possible to follow the brain across an entire story. Hidden Markov
models fitted to each participant's six seasons of `friends` showed that each brain visits
roughly forty-five recurring states, from ones active in nearly every episode to
episode-specific ones. Episode content shifted which states were occupied, not which states
existed, and the repertoire transferred to other social-narrative films
{cite:p}`Chen2026-ef`. Emotional content can be annotated automatically, from the audio and
subtitles of the dialogue {cite:p}`Corsico2026-hy` (see Brain Decoding). A dedicated
repository, still in development,
[`friends.annotations`](https://github.com/courtois-neuromod/friends.annotations), describes
each half-episode watched in the scanner along several dimensions: automated transcription
with speaker identity, edited fan-made transcripts, face positions of named characters,
soundscape tags, predicted gaze locations, automated shot and manual scene segmentations, and
summaries of episodes and characters. Such annotations let users test cognitive hypotheses,
for instance about speakers, characters or scene changes, with standard analyses and without
training AI models.

Controlled tasks complement these stimuli for language and memory. `harrypotter` reproduces,
in five CNeuroMod participants, the word-by-word reading paradigm of an existing fMRI
dataset. Brain encoding of a computational representation of composed, "supra-word" meaning
found that hubs thought to process lexical meaning also maintain supra-word meaning
{cite:p}`Toneva2022-bf`, and a methods paper from the same group found its inferences
strikingly consistent across two naturalistic fMRI datasets {cite:p}`Toneva2022-vu`. In
`things`, participants performed a continuous recognition task in which each image was shown
three times, within and across weekly sessions, and reported whether it was new or seen
before, and how confident they were {cite:p}`St-Laurent2026-zc`. This supports the study of
recognition memory over delays of weeks, in the same participants who watched the movies.

% TODO: confirm which fMRI datasets Toneva2022-vu used.

Games can be annotated without manual coding. In `shinobi` and `mario`, events such as
player actions, kills or health losses are extracted from the emulator's memory and released
with the data, ready for event-related analyses {cite:p}`harel2026gamer`. The 22 `mario`
levels are also split into 313 short scenes, each labelled with the game design patterns it
contains, such as gaps, enemy hordes or stairs, released as a standalone resource
{cite:p}`Harel2025-scenes`. Scenes provide a unit of analysis for comparing gameplay and
brain activity across attempts and participants.

---

## 6. Foundation Models and the Digital Brain

CNeuroMod was designed to answer a question that a sample of many people cannot: can a
model reproduce one specific brain across a wide range of cognitive functions? This
requires many hours of data from the same person, recorded under many different tasks.
Individual models trained on CNeuroMod already predict brain activity for new stimuli,
improve with more data from the same person, and often match or outperform group models.
The next steps are to scale these models up, to transfer them to new individuals, and to
extend them to new recording modalities.

Modelling is scaling up first. TRIBE, trained only on CNeuroMod, kept improving with more
training data without reaching a plateau {cite:p}`d-Ascoli2026-hf`. Its successor, TRIBE
v2, aims to be a foundation model of brain responses to video, audio and language, which
generalizes to new stimuli, tasks and participants. It combines CNeuroMod with three other
deeply sampled datasets, and is evaluated on more than 1,000 hours of fMRI from 720
participants {cite:p}`dascoli2026tribev2`. CNeuroMod supplies most of its training fMRI,
268.7 of 451.6 hours, and is the only training dataset that combines video, audio and
text. How much the other datasets add to the model's performance has not been measured.

Data collection is scaling up as well. Building on CNeuroMod, the
[Digital Brain Project](https://digitalbrainproject.org/) aims to "build a functional model
of the human brain" from recordings acquired during complex, interactive tasks. Funded by
Meta with US$15M, it will collect 15,000 hours of brain activity across nine teams, with
"a few subjects over many sessions", and release deidentified data in BIDS format.
CNeuroMod is one of its two contributing labs, and its infrastructure of standardized
formats, versioned datasets and reproducible pipelines provides a template for collecting
and sharing data at this scale.

Deep individual models raise the question of how to transfer them to a new person, for
whom only a short recording is available. Optimal transport (OT) is a promising tool for
this data-efficient alignment. OT finds the least costly way to move the functional signal
of one brain onto another, as a soft matching between cortical locations with similar
responses. Piecewise OT was among the best functional alignment methods for inter-subject
decoding at the whole-brain scale {cite:p}`Bazeille2021-ea`. Fused unbalanced
Gromov-Wasserstein (FUGW) matches cortical surfaces on their responses while penalizing
distortions of each brain's topography, and allows functional areas to differ in size
between individuals {cite:p}`Thual2022-fugw`. Alignments computed from movie watching
improved out-of-subject decoding of visual semantics by up to 75%, and beat single-subject
decoders when less than 100 minutes of data were available for the new participant
{cite:p}`Thual2023-ab`. The same tools compare brains with AI models: the soft matching
distance uses OT to match the units of two systems of different sizes, voxel by voxel or
neuron by neuron {cite:p}`Khosla2024-sm`, and a partial version leaves unreliable voxels
unmatched {cite:p}`Kapoor2026-ps`.

CNeuroMod is well suited to these methods, which learn alignments from responses to shared
stimuli. Its participants watched the same movies, saw the same images and played the same
games for tens of hours. Each of them can serve as a dense functional template, onto which
a new person is mapped from a short movie-watching session, so that an individual model
trained on hundreds of hours can be reused with little new data. The same approach could
align CNeuroMod with other deeply sampled datasets wherever they share stimuli, including
those of the Digital Brain Project, and test how many minutes of data a new individual needs
for a transferred model to match a model trained on their own data.

CNeuroMod itself is expanding across recording modalities. A magnetoencephalography (MEG)
extension is about to be collected: about 10 hours of MEG per participant for five
participants, covering most CNeuroMod tasks with a reduced set of stimuli. The tasks of the
Digital Brain Project will also be recorded in `sub-01` with both EEG and MEG. These
extensions will give the same tasks in the same individuals with complementary temporal and
spatial resolution, to build individual brain models that generalize across recording
modalities as well as across stimuli and tasks.

---

## Accessing the Data

[Instructions for requesting access and downloading data via the CNeuroMod data portal. Include links to the data agreement, DataLad/datalad-cneuromod repository, and OpenNeuro/OSF deposits where applicable.]

## Known Limitations

[Describe known issues: small N (6 subjects), site-specific scanner characteristics, missing sessions for some subjects/tasks, motion in active paradigms, and task-specific exclusion criteria. Refer readers to the Data Record section for per-dataset details.]

## Recommended Practices

[Suggest best practices: use fMRIPrep outputs, leverage provided confound regressors, cite the relevant task papers when using specific datasets, check the CNeuroMod documentation for versioned data releases.]
