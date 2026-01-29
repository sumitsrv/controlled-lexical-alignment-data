# Human Evaluation Dialogues

This folder contains the dialogues used in the human evaluation study for assessing lexical alignment in conversational AI systems.

## Overview

The human evaluation study compared dialogues generated with different alignment weight configurations. Participants were presented with pairs of dialogues (one with baseline/zero weight, one with an optimized weight) and asked to evaluate their preferences.

## Study Design

- **Comparison paradigm**: Paired comparison between baseline (0w) and alignment-weighted dialogues
- **Generator models**: 3 different LLM-based utterance generators
- **Conversation topics**: 6 different conversation topics across models
- **Dialogue pairs**: 6 pairs total (12 dialogues)

## Directory Structure

```
Human Evaluation Dialogues/
├── README.md
├── BlenderBot-3B/
│   ├── culture/
│   │   ├── 0w.csv          # Baseline (weight = 0)
│   │   └── 25w.csv         # Alignment weight = 25
│   └── culture2/
│       ├── 0w.csv          # Baseline (weight = 0)
│       └── 75w.csv         # Alignment weight = 75
├── Llama-2-7b-chat/
│   ├── environment/
│   │   ├── 0w.csv          # Baseline (weight = 0)
│   │   └── 1000w.csv       # Alignment weight = 1000
│   └── health/
│       ├── 0w.csv          # Baseline (weight = 0)
│       └── 750w.csv        # Alignment weight = 750
└── Phi-3.5-mini-instruct/
    ├── culture/
    │   ├── 0w.csv          # Baseline (weight = 0)
    │   └── 3500w.csv       # Alignment weight = 3500
    └── education/
        ├── 0w.csv          # Baseline (weight = 0)
        └── 3250w.csv       # Alignment weight = 3250
```

## Models and Weight Configurations

| Model | Topic | Baseline | Optimized Weight |
|-------|-------|----------|------------------|
| BlenderBot-3B | culture | 0 | 25 |
| BlenderBot-3B | culture2 | 0 | 75 |
| Llama-2-7b-chat | environment | 0 | 1000 |
| Llama-2-7b-chat | health | 0 | 750 |
| Phi-3.5-mini-instruct | culture | 0 | 3500 |
| Phi-3.5-mini-instruct | education | 0 | 3250 |

## Dialogue Generation Setup

These dialogues were generated using the following setup:
- **Speaker 1 (Human)**: Played by an LLM acting as a human conversation partner (GPT-4o-mini or Claude)
- **Speaker 2 (Agent)**: The generator model being evaluated (BlenderBot-3B, Llama-2-7b-chat, or Phi-3.5-mini-instruct)

The generator model's responses were produced using our lexical alignment-controlled generation method with the specified weight parameter.

## File Format

Each CSV file contains a dialogue in tab-separated format:
```
speaker_model:	utterance text
speaker_model:	response text
...
```

Example:
```
openai/gpt-4o-mini:	How do different cultures enrich our society?
facebook/blenderbot-3B:	It's hard to explain without going into a lot of detail...
```

## Conversation Topics

| Topic | Description |
|-------|-------------|
| culture | Cultural diversity and societal enrichment |
| culture2 | Cross-cultural experiences and perspectives |
| environment | Environmental issues and sustainability |
| health | Health habits and wellness practices |
| education | Learning strategies and skill development |

## Usage

To load a dialogue in Python:

```python
import csv

def load_dialogue(filepath):
    dialogue = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) >= 2:
                speaker = row[0].rstrip(':')
                utterance = row[1].strip()
                dialogue.append({'speaker': speaker, 'utterance': utterance})
    return dialogue

# Example
dialogue = load_dialogue('BlenderBot-3B/culture/25w.csv')
for turn in dialogue:
    print(f"{turn['speaker']}: {turn['utterance'][:50]}...")
```

## Citation

If you use this data in your research, please cite our paper (citation details will be added upon publication).

## Related Data

See the companion folder `Automatic Evaluation Dialogues (DailyDialog based)/` for the full set of generated dialogues across all weight configurations.
  year={2025}
}
```

## Related Data

See the companion folder `DailyDialog Generator Model Dialogues/` for the full set of generated dialogues across all weight configurations.
