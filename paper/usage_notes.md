# Usage Notes

The CNeuroMod dataset has been used in a growing body of research spanning brain encoding, brain decoding, cognitive neuroscience, and AI alignment with neural data. This section provides an overview of key research directions enabled by the dataset and practical guidance for new users.

## Overview of Publications

[Summary paragraph: briefly enumerate the main research communities using CNeuroMod data, total number of publications or preprints to date, and the main venues (NeurIPS, ICLR, Imaging Neuroscience, PLOS ONE, etc.).]

---

## 1. Individual Brain Encoding Models

[Overview: CNeuroMod has emerged as a key resource for building high-quality voxelwise encoding models of individual brains.]

### The Algonauts 2025 Competition

[Describe the Algonauts 2025 challenge: goals, dataset used (CNeuroMod HCP-style or Friends/Shinobi?), number of participants, main findings. Highlight how the competition structure promoted individual-level modeling.]

### The TRIBE Model

[Describe the TRIBE model: what it does, what data it was trained on, key results in terms of brain prediction accuracy. Reference the relevant paper(s).]

### New Directions: Auto-Regressive and Brain Encoding in One Model

[Discuss Paugam et al.'s work combining auto-regressive modeling with brain encoding in a unified framework. Explain why this is a significant conceptual advance and what it implies for future encoding model architectures. Add citation.]

---

## 2. Brain Encoding Models of the Active Brain

[Overview: CNeuroMod's active tasks — particularly videogame paradigms — enable a new class of encoding models that capture brain activity during goal-directed, embodied behavior.]

### Atari Games

[Discuss Cross et al. and Tomov et al. using Atari game stimuli for brain encoding. Summarize key findings linking RL agent representations to neural activity. Add citations.]

### Videogame Controller and Motor Signals

[Discuss Harel et al. (PLOS ONE) examining controller inputs and neural correlates. Summarize findings on motor and planning signals in fMRI. Add citation.]

### Clean BOLD Signal in Active Tasks

[Describe Harel et al. (Imaging Neuroscience) demonstrating that high-quality BOLD signal is recoverable during active gameplay despite motion and arousal confounds. Add citation.]

### Imitation Learning in the Brain

[Describe Kemtur et al. (Imaging Neuroscience) using imitation learning frameworks to model behavior and brain activity. Add citation.]

### Learning Trajectories in Mario

[Describe Harel & Bellec (RLC Workshop on Videogames in RL) characterizing how neural representations evolve as subjects learn to play Super Mario Bros. Add citation. Note this as a major area for future competitions.]

---

## 3. Towards Better AI with Neural Data

[Overview: Growing excitement in the ML community about using neural recordings as a source of inductive biases or alignment signals for AI models.]

### The Case for Neuro-Aligned AI

[Reference Mineault et al. white paper and recent review articles arguing for integrating neural data into AI training pipelines. Summarize the main arguments.]

### SoundNet Trained on Neural Data

[Describe Freteault et al. (Imaging Neuroscience) training a SoundNet-style audio model using CNeuroMod fMRI responses as supervision signal. Summarize results showing improved audio representations. Add citation.]

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

### Large-Scale Annotation Efforts

[Describe the team's ongoing effort to release large-scale annotations of naturalistic stimuli, including Friends and Mario scenes (scene segmentation, character identity, emotional valence, actions, etc.). Explain how these annotations will enable purely cognitive neuroscience-driven analyses without requiring ML expertise.]

---

## 6. Foundation Models and the Digital Brain

[Overview: CNeuroMod individual brain models are positioning themselves as building blocks for foundation models that generalize across individuals, datasets, acquisition sites, and modalities.]

### TRIBE V2 and the Digital Brain Project

[Describe TRIBE V2 and its role in the broader Digital Brain initiative. Explain how scaling individual encoding models across CNeuroMod subjects and linking to other large datasets (e.g., HCP, UK Biobank) could yield a generalizable neural foundation model. Add citations/links.]

### Optimal Transport for Data-Efficient Alignment

[Discuss the opportunity to apply optimal transport (OT) methods for aligning neural representations across subjects and datasets in a data-efficient manner. Reference work from Aimy Wenegrat's lab and the INRIA DANDI team. Explain why OT is particularly well-suited to the small-N, high-dimensional regime of deep phenotyping datasets like CNeuroMod.]

---

## Accessing the Data

[Instructions for requesting access and downloading data via the CNeuroMod data portal. Include links to the data agreement, DataLad/datalad-cneuromod repository, and OpenNeuro/OSF deposits where applicable.]

## Known Limitations

[Describe known issues: small N (6 subjects), site-specific scanner characteristics, missing sessions for some subjects/tasks, motion in active paradigms, and task-specific exclusion criteria. Refer readers to the Data Record section for per-dataset details.]

## Recommended Practices

[Suggest best practices: use fMRIPrep outputs, leverage provided confound regressors, cite the relevant task papers when using specific datasets, check the CNeuroMod documentation for versioned data releases.]
