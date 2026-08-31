# Generalisation Sweep (New Models)

This directory documents the **second study** in the paper (Appendices F, G and H): a check that
weighted decoding generalises beyond the four original models and beyond datacenter-class hardware.
It reuses the exact same weighted-decoding method described in the [main README](../README.md), but
swaps in newer, more recent-generation models, runs on a single consumer GPU (NVIDIA RTX 4060,
8GB VRAM), and sweeps four hyperparameters instead of one. It is **supplementary** to the main study
in `../Automatic Evaluation Dialogues (DailyDialog based)/`, not a replacement for it — the paper's
primary results still come from the original four models on datacenter hardware.

## Models

| Key | Model | Notes |
|-----|-------|-------|
| `Qwen3.5-2B` | Qwen/Qwen3.5-2B | |
| `blenderbot-3b` | facebook/blenderbot-3B | carried over from the original 4-model set, as an anchor |
| `llama-3.2-1b` | meta-llama/Llama-3.2-1B-Instruct | |
| `gemma-4-E2B-it` | google/gemma-4-E2B-it | 4-bit quantized (only quantized model in the set) |
| `gemma_prompted` | google/gemma-4-E2B-it | same weights as above + a one-line "You are a dialogue partner in a conversation." persona on turn 1. Treated as a distinct model throughout — isolates the effect of a minimal prompt from the effect of weighted decoding. |
| `dialogpt-medium` | microsoft/DialoGPT-medium | **decay sweep only** — dropped from the other three sweeps and from the current model registry; kept only to extend the decay-schedule comparison |

## Sweep grids

| Sweep | Values | Models covered | Source dialogues per config |
|-------|--------|-----------------|------------------------------|
| `weight` | model-specific λ grids (7–9 points, incl. one negative value for bidirectional control) | all 5 | 10 |
| `topk` | 5, 10, 20, 50, 100 | all 5 | 10 |
| `beam` (K, candidate count) | 1, 3, 5, 10 | Qwen3.5-2B, blenderbot-3b, llama-3.2-1b, gemma_prompted (plain gemma-4-E2B-it was generated but never judged — see `dialogues/raw_checkpoints/beam/` for its untouched checkpoints if that's ever revisited) | 10 |
| `decay` | geometric (rate 0.5), geometric (rate 0.97), power-law | Qwen3.5-2B, blenderbot-3b, dialogpt-medium only | 10 |

Row counts in `results/quality_table.csv` per sweep: weight 43, topk 25, beam 16, decay 8 —
matches the model coverage above (row = one model × one parameter value).

**Known gap:** the decay sweep's raw generated dialogue text was never saved to this machine — only
the aggregated judge rankings (`judge_raw/decay/`) and quality metrics (`results/quality_table.csv`)
survive. The generation script (`colab_experiments/run_decay_sweep.py`) checkpoints to
`decay_sweep_output/checkpoints/`, which doesn't exist locally; if the raw decay dialogues are ever
needed, that script would need to be re-run. `dialogues/{weight,topk,beam}/` have no such gap — every
config has both raw checkpoint JSON and a rendered `.txt` per dialogue.

## Structure

```
├── dialogues/
│   ├── {weight,topk,beam}/{model}/{param}={value}/{n}.txt   # rendered, human-readable
│   └── raw_checkpoints/{weight,topk,beam}/{model}__{param}__{value}.json   # untouched generation output
├── judge_raw/
│   ├── {weight,topk,beam,decay}/judge_eval_summary.json     # aggregated BT scores/win rates per sweep
│   ├── {weight,topk,beam,decay}/intra/{model}/tournament_intra_results.json  # raw per-judge, per-dialogue rankings
│   └── weight/inter/inter_model_results.json                # raw inter-model comparisons incl. full judge free-text reasoning
├── results/
│   ├── quality_table.csv       # BT score + win rate per sweep × model × config
│   ├── weight_metrics.csv      # median perplexity + ER (alignment) vs weight, new models
│   ├── inter_model_table.csv   # cross-model BT ranking (weight sweep only)
│   ├── agreement_table.csv     # inter-judge agreement (Cohen's κ, Fleiss' κ, Kendall's τ)
│   ├── timing_analysis_output.csv     # per-turn generation latency (RTX 4060), one row per sweep×model×config
│   ├── generate_timing_analysis.py    # script that produced it, kept for provenance
│   └── figures/                # rendered PNGs of the above
└── decay_curve_fitting/        # DailyDialog/TopicalChat empirical decay-rate fits used to justify
                                  # the decay=geometric(0.5) design choice — NOT the decay sweep above
    ├── dailydialog/
    ├── topicalchat/
    └── decay_all_datasets.json
```

## File formats

### dialogues/{sweep}/{model}/{param}={value}/{n}.txt
Same convention as `../Automatic Evaluation Dialogues (DailyDialog based)/`: `Human 1:` is the
DailyDialog source turn (unmodified), `Human 2 (generated):` is the model's weighted-decoding output.
Unlike the main study, S1's DailyDialog ground truth for that turn position is also included as a
`#`-prefixed comment line — it's what S2 would have said in DailyDialog, kept only for reference, not
part of the model's input.

### dialogues/raw_checkpoints/{sweep}/*.json
The untouched output of the generation run: `config` (model/weight/top_k/decay/sample-count settings),
`metrics` (aggregate ELS/EV/TO/ER/perplexity for the whole checkpoint), and `dialogue_results` (one
entry per dialogue: full turn-by-turn `conversation` with per-turn latency and DailyDialog ground
truth). This is the authoritative source the rendered `.txt` files were derived from.

### judge_raw/{sweep}/intra/{model}/tournament_intra_results.json
`per_dialogue_rankings[judge][dialogue_id]` gives each judge's raw preference ranking (best→worst) of
the configs compared for that dialogue — the primary unit the Bradley-Terry scores in
`judge_eval_summary.json` and `results/quality_table.csv` are computed from.

### judge_raw/weight/inter/inter_model_results.json
`raw` is a list of individual judge calls: `{judge, bucket, idx, models, response}`, where `response`
is the judge's full free-text reasoning per comparison (not just a ranking) before it was parsed into
the win-rate matrices under `result.buckets`.

## Generation performance benchmark

Unlike the main study (single NVIDIA H100 PCIe, `../benchmark_results.json`), this sweep ran on a
**single consumer GPU (NVIDIA RTX 4060, 8GB VRAM)** — reported separately since the two are not
comparable. `results/timing_analysis_output.csv` gives median + IQR per-turn latency and ms/generated-word
for every (sweep, model, parameter value) combination — 92 rows, one per row of `results/quality_table.csv`
plus decay — computed from the per-turn `latency_s` fields inside the raw generation checkpoints by
`results/generate_timing_analysis.py` (copied here for provenance; drops each config's first dialogue as
a cold-start guard). Baseline (unweighted, λ=0) per-turn latency per model:

| Model | Median (s) | IQR (s) |
|-------|-----------|---------|
| BlenderBot-3B | 1.409 | 1.361–1.437 |
| Gemma-4-E2B-it (prompted) | 11.117 | 9.196–13.623 |
| Gemma-4-E2B-it | 17.065 | 16.205–18.929 |
| Llama-3.2-1B | 22.928 | 20.007–24.687 |
| Qwen3.5-2B | 23.073 | 21.560–25.115 |

Latency generally rises with weight/top-k/K away from these baselines (see `results/timing_analysis_output.csv`
for the full grid); Table G.3 in the paper reports the beam(K)-vs-latency slice of this same data.
Per-config wall time is also embedded directly in each `dialogues/raw_checkpoints/{sweep}/*.json` file
under its `timing` key. **Gap:** unlike the main study's `benchmark_results.json`, per-model load times
were printed during generation but never persisted to disk for this hardware, so they aren't reproduced here.

## Judges

Three open models via HF Inference API — **deepseek-v3.1, minimax-m3, ernie-4.5** — different from the
main study's judge panel (GPT-4.1-mini, GPT-4o-mini, Mistral-Large, Claude-3-5-Haiku; see
[main README](../README.md#automatic-evaluation-llm-as-judge)), because the commercial-API judges'
cost was prohibitive at sweep scale (a fresh 3-judge panel replaces them for these appendix sweeps
only). Same evaluation prompt and 20-criteria rubric as the main study.

## Generation setup

Single NVIDIA RTX 4060 (8GB VRAM), 10 source DailyDialog dialogues per configuration, 50-token
generation cap (30 for the main-paper generations). Main-paper default settings for anything not being
swept: top-k=20, K=10 candidates, geometric decay (rate 0.5) — matching the main study exactly so the
sweeps isolate one hyperparameter at a time.

## Relation to the paper

Maps to paper appendices: **F** (weight sweep, cross-model comparison), **G** (topk/beam/decay
hyperparameter sensitivity), **H** (inter-judge agreement, Table H.2 — the source of the per-sweep
model coverage table above).
