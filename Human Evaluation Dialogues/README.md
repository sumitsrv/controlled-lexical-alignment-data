# Human Evaluation Dialogues

**12 dialogues** (6 pairs) used in the human preference study comparing baseline (w=0) vs. optimized weights.

## Study Design

Pairwise comparison: 50 participants (recruited via Prolific) evaluated baseline vs. alignment-weighted dialogues, ranking each pair from best (1) to worst (2).

### Participant Instructions

> Rank the following dialogues from the best (1) to the worst (2) based on the relevance and coherence of the responses by S2.
>
> **Relevance:** The appropriateness of responses to immediate conversational context, i.e., the previous utterance of Speaker 1 (S1).
>
> **Coherence:** The maintenance of thematic consistency and logical progression with respect to the full dialogue.

### Inter-Rater Agreement

| Statistic | Value |
|-----------|-------|
| Participants | 50 |
| Dialogue pairs | 6 |
| Average percentage agreement | **58.3%** |
| Average normalized entropy | 0.849 |

> **Note:** Traditional IRR metrics such as Fleiss' κ are not well-suited for this single-item pairwise design. Percentage agreement and normalized entropy are reported as more appropriate measures.

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
