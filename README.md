# Controlled Lexical Alignment - Supplementary Data

This repository contains supplementary data for the research paper on controlled lexical alignment in conversational AI systems.

## Overview

This dataset accompanies our research on understanding and controlling lexical alignment behavior in Large Language Model (LLM)-based conversational agents. Lexical alignment refers to the tendency of conversation partners to adopt each other's vocabulary and expressions during dialogue, a phenomenon well-documented in human-human communication.

Our work introduces a method to control the degree of lexical alignment in LLM-generated responses through weighted lexicon-based generation, enabling systematic study of how alignment affects conversation quality and user perception.

## Dataset Contents

This repository contains two main datasets:

### 1. Automatic Evaluation Dialogues (DailyDialog based)
**Location:** `Automatic Evaluation Dialogues (DailyDialog based)/`

A large-scale dataset of **10,545 dialogues** generated across four conversational AI models with varying alignment weight configurations. These dialogues were used for automated evaluation of lexical alignment metrics.

| Model | Dialogues | Weight Range |
|-------|-----------|--------------|
| BlenderBot-3B | 1,425 | 25 - 1000 |
| DialoGPT-small | 1,330 | 25 - 1000 |
| Llama-2-7b-chat | 3,895 | 25 - 7500 |
| Phi-3.5-mini-instruct | 3,895 | 25 - 7500 |

**Data Source:** Modified versions of dialogues from the [DailyDialog dataset](https://aclanthology.org/I17-1099/) (Li et al., 2017).

### 2. Human Evaluation Dialogues
**Location:** `Human Evaluation Dialogues/`

A curated set of **12 dialogues** (6 pairs) used in the human evaluation study. Each pair compares a baseline dialogue (weight = 0) with an alignment-weighted dialogue.

| Model | Topics | Weight Comparisons |
|-------|--------|-------------------|
| BlenderBot-3B | culture, culture2 | 0 vs 25, 0 vs 75 |
| Llama-2-7b-chat | environment, health | 0 vs 1000, 0 vs 750 |
| Phi-3.5-mini-instruct | culture, education | 0 vs 3500, 0 vs 3250 |

## Generator Models

| Model | Source | Type |
|-------|--------|------|
| BlenderBot-3B | facebook/blenderbot-3B | Encoder-Decoder |
| DialoGPT-small | microsoft/DialoGPT-small | Decoder-only (GPT-2) |
| Llama-2-7b-chat | meta-llama/Llama-2-7b-chat-hf | Decoder-only (LLaMA) |
| Phi-3.5-mini-instruct | microsoft/Phi-3.5-mini-instruct | Decoder-only (Phi) |

## Alignment Weight Parameter

The alignment weight (`w`) controls the strength of lexical alignment in generated responses:
- **w = 0**: Baseline generation (no alignment bias)
- **Low w** (25-100): Subtle alignment tendency
- **Medium w** (500-1000): Moderate alignment
- **High w** (2000+): Strong alignment tendency

The optimal weight varies by model architecture and scale.

## File Formats

### Dialogue Files (.csv)
Tab-separated format with speaker and utterance:
```
speaker_model:	utterance text
speaker_model:	response text
```

### Alignment Metrics (.tsv)
Tab-separated files containing computed lexical alignment metrics including:
- Expression Variety (EV)
- Expression Repetition (ER)
- Vocabulary Overlap
- Entropy (ENTR)
- Self-Repetition metrics

## Quick Start

```python
import pandas as pd
import os

# Load automatic evaluation metrics
auto_eval_path = "Automatic Evaluation Dialogues (DailyDialog based)"
metrics_df = pd.read_csv(
    os.path.join(auto_eval_path, "alignment_data_20250329.tsv"), 
    sep='\t'
)

# Filter by model
llama_dialogues = metrics_df[metrics_df['mname'] == 'meta-llama/Llama-2-7b-chat-hf']

# Load a human evaluation dialogue
human_eval_path = "Human Evaluation Dialogues"
with open(os.path.join(human_eval_path, "Llama-2-7b-chat/health/750w.csv")) as f:
    dialogue = f.read()
    print(dialogue)
```

## Citation

If you use this dataset in your research, please cite our paper (citation details will be added upon publication).

## References

- Li, Y., Su, H., Shen, X., Li, W., Cao, Z., & Niu, S. (2017). DailyDialog: A Manually Labelled Multi-Turn Dialogue Dataset. In *Proceedings of the 8th International Joint Conference on Natural Language Processing (IJCNLP 2017)*.

## License

This dataset is provided for research purposes. Please refer to the original DailyDialog dataset license for terms regarding the base dialogue data.

## Contact

For questions regarding this dataset, please refer to the corresponding author information in the associated paper.
