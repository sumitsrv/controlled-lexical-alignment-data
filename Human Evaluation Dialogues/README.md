# Human Evaluation Dialogues

**12 dialogues** (6 pairs) used in the human preference study comparing baseline (w=0) vs. optimized weights.

## Study Design

Paired comparison: participants evaluated baseline vs. alignment-weighted dialogues.

## Dialogue Pairs

| Model | Topic | Baseline | Optimized |
|-------|-------|----------|-----------|
| BlenderBot-3B | culture | 0 | 25 |
| BlenderBot-3B | culture2 | 0 | 75 |
| Llama-2-7b-chat | environment | 0 | 1000 |
| Llama-2-7b-chat | health | 0 | 750 |
| Phi-3.5-mini-instruct | culture | 0 | 3500 |
| Phi-3.5-mini-instruct | education | 0 | 3250 |

## Structure

```
{Model}/{Topic}/
├── 0w.csv       # Baseline
└── {weight}w.csv # Optimized
```

## Generation Setup

- **Speaker 1**: LLM acting as human (GPT-4o-mini or Claude)
- **Speaker 2**: Generator model with controlled alignment weight

## File Format

Tab-separated CSV:
```
speaker_model:  utterance text
speaker_model:  response text
```
