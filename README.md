# Weighted Decoding for Controlled Lexical Alignment in LLM-based Dialogues

Supplementary data for the research paper.

## Contents

```
├── Automatic Evaluation Dialogues (DailyDialog based)/
│   ├── models/                          # Generated dialogues by model and weight
│   ├── alignment_data_20250329.tsv      # Alignment metrics for all dialogues
│   └── README.md
├── Human Evaluation Dialogues/
│   ├── {Model}/{Topic}/                 # Dialogue pairs per model and topic
│   └── README.md
├── figures/                             # High-resolution figures from the paper
├── inter_model_evaluation_results.tsv   # Inter-model comparison evaluations
├── intra_model_evaluation_results.tsv   # Intra-model weight comparison evaluations
└── bradley_terry_rankings.json          # Bradley-Terry model rankings
```

## Datasets

### Automatic Evaluation Dialogues
**10,545 dialogues** generated from DailyDialog with varying alignment weights.

| Model | Dialogues | Weight Range |
|-------|-----------|--------------|
| BlenderBot-3B | 1,425 | 25–1000 |
| DialoGPT-small | 1,330 | 25–1000 |
| Llama-2-7b-chat | 3,895 | 25–7500 |
| Phi-3.5-mini-instruct | 3,895 | 25–7500 |

### Human Evaluation Dialogues
**12 dialogues** (6 pairs) for human preference study comparing baseline (w=0) vs. optimized weights.

## Evaluation Data Files

| File | Description |
|------|-------------|
| `inter_model_evaluation_results.tsv` | LLM-as-judge rankings comparing dialogues across different generator models |
| `intra_model_evaluation_results.tsv` | LLM-as-judge rankings comparing weight configurations within the same model |
| `bradley_terry_rankings.json` | Aggregated Bradley-Terry rankings from pairwise comparisons of intra model dialogues |

## Figures

High-resolution versions of figures from the paper (in `figures/`):

| File | Description |
|------|-------------|
| `alignment_scores_low_weights.png` | Alignment scores for weights ≤1000 |
| `alignment_scores_high_weights.png` | Alignment scores for weights >1000 |
| `perplexity_low_weights.png` | Perplexity for weights ≤1000 |
| `perplexity_high_weights.png` | Perplexity for weights >1000 |
| `inter_model_win_rates.png` | Inter-model comparison win rates |
| `intra_model_bradley_terry_rankings.png` | Intra-model Bradley-Terry rankings |

### File Formats

**inter_model_evaluation_results.tsv**
```
evaluator_model  alignment_range  model_candidates  preference_ranking
```

**intra_model_evaluation_results.tsv**
```
evaluator_model  target_model  dialogue_id  weight_candidates  preference_ranking
```

## Generator Models

| Model | Type |
|-------|------|
| BlenderBot-3B | Encoder-Decoder |
| DialoGPT-small | Decoder-only |
| Llama-2-7b-chat | Decoder-only |
| Phi-3.5-mini-instruct | Decoder-only |

## References

Yanran Li, Hui Su, Xiaoyu Shen, Wenjie Li, Ziqiang Cao, and Shuzi Niu. 2017. DailyDialog: A Manually Labelled Multi-turn Dialogue Dataset. In Proceedings of the Eighth International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pages 986–995, Taipei, Taiwan. Asian Federation of Natural Language Processing.

## Citation

Citation details will be added upon publication.

## License

For research purposes. See DailyDialog license for base dialogue data terms.
