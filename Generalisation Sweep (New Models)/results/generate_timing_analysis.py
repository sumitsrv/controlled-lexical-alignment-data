"""
Generation-timing analysis: does beam width / top_k / decay / weight move latency?

Goes to PER-TURN latency_s (not the pre-aggregated config medians), so we can
show median + IQR per parameter value and control for output length (ms/token).

Sources (each a list of per-config entries {config, timing, dialogue_results}):
  beam, topk : sweep_output/sweep_*.json           (knob: num_samples / top_k)
  decay      : decay_sweep_assembled.json           (knob: decay_mode+param)
  weight     : sweep_output/checkpoints/weight__*.json  (one config per FILE)

Latency is a fair cross-config comparison as-is: max_new_tokens is fixed, so each
turn generates ~the same budget PER candidate, and beam's cost shows up as more
candidates. We still report ms/generated-word as a length-controlled secondary.

Run:  python timing_analysis.py            # tables + timing_analysis_output.csv
      python timing_analysis.py --self-check
"""
import csv
import glob
import json
import os
import sys

import numpy as np

SWEEP_GLOB = "sweep_output/sweep_*.json"
DECAY_JSON = "generated_backup_20260712/decay_sweep_output/decay_sweep_assembled.json"
WEIGHT_GLOB = "sweep_output/checkpoints/weight__*.json"
OUT_CSV = "timing_analysis_output.csv"

# Drop the first dialogue of each config as a light warm-up guard (cold CUDA
# kernels / autotuning on a config's first generation). NOTE: this does NOT fix
# the run-ORDER confound -- the first config run per model can be slow from
# thermal/contention -- which post-hoc filtering can't remove. Trends are robust
# (medians); treat a single anomalous config value with that caveat.
WARMUP_DIALOGUES = 1


def _turn_latencies(entry, warmup=WARMUP_DIALOGUES):
    """Yield (latency_s, n_words) for every scored turn in one config entry,
    skipping the first `warmup` dialogues."""
    for d_idx, dr in enumerate(entry.get("dialogue_results", [])):
        if d_idx < warmup:
            continue
        for t in dr.get("turns", []):
            lat = t.get("latency_s")
            if lat is None:
                continue
            words = max(1, len((t.get("generated") or "").split()))
            yield float(lat), words


def _stats(pairs):
    """(median, iqr_lo, iqr_hi, n, median_ms_per_word) from (latency, words) pairs."""
    if not pairs:
        return None
    lat = np.array([p[0] for p in pairs])
    mspw = np.array([p[0] * 1000.0 / p[1] for p in pairs])
    return (
        float(np.median(lat)),
        float(np.percentile(lat, 25)),
        float(np.percentile(lat, 75)),
        len(lat),
        float(np.median(mspw)),
    )


def _load_sweeps():
    """Return rows: (sweep, model, param_name, param_value, entry)."""
    rows = []

    # beam / topk from the assembled sweep JSON (latest by name that actually
    # holds beam/topk -- skip sweep_weight_assembled.json, which only has "weight").
    files = [f for f in sorted(glob.glob(SWEEP_GLOB))
             if any(k in json.load(open(f)) for k in ("beam", "topk"))]
    if files:
        sw = json.load(open(files[-1]))
        for sweep, knob in (("beam", "num_samples"), ("topk", "top_k")):
            for model, entries in sw.get(sweep, {}).items():
                if not isinstance(entries, list):
                    continue  # e.g. a failed generation: {"error": ...}
                for e in entries:
                    rows.append((sweep, model, knob, e["config"].get(knob), e))

    # decay from its assembled backup
    if os.path.exists(DECAY_JSON):
        for model, entries in json.load(open(DECAY_JSON)).items():
            for e in entries:
                c = e["config"]
                pv = f"{c.get('decay_mode')}_{c.get('decay_param', c.get('decay_factor'))}"
                rows.append(("decay", model, "decay", pv, e))

    # weight: one config PER checkpoint file (skip partial/malformed ones)
    for f in sorted(glob.glob(WEIGHT_GLOB)):
        if "__partial" in f:
            continue
        e = json.load(open(f))
        c = e.get("config", {})
        if c.get("model_key") and c.get("weight") is not None:
            rows.append(("weight", c["model_key"], "weight", c["weight"], e))

    return rows


def analyse():
    rows = _load_sweeps()
    # aggregate: (sweep, model, param, value) -> stats
    agg = {}
    for sweep, model, pname, pval, entry in rows:
        pairs = list(_turn_latencies(entry))
        st = _stats(pairs)
        if st:
            agg[(sweep, model, pname, pval)] = st

    # print tables + collect CSV
    csv_rows = []
    for sweep in ("beam", "topk", "decay", "weight"):
        keys = [k for k in agg if k[0] == sweep]
        if not keys:
            continue
        print(f"\n================ {sweep.upper()}  (median per-turn latency s, [IQR]) ================")
        for model in sorted({k[1] for k in keys}):
            mkeys = sorted([k for k in keys if k[1] == model],
                           key=lambda k: (k[3] is None, k[3]))
            cells, meds = [], []
            for k in mkeys:
                med, lo, hi, n, mspw = agg[k]
                cells.append(f"{k[3]}={med:.2f}[{lo:.1f}-{hi:.1f}]")
                meds.append(med)
                csv_rows.append({
                    "sweep": sweep, "model": model, "param": k[2], "value": k[3],
                    "n_turns": n, "median_latency_s": round(med, 3),
                    "iqr_lo_s": round(lo, 3), "iqr_hi_s": round(hi, 3),
                    "median_ms_per_word": round(mspw, 2),
                })
            span = f"{max(meds) / min(meds):.1f}x" if len(meds) > 1 and min(meds) > 0 else "-"
            print(f"  {model:16s} {'  '.join(cells)}   [span {span}]")

    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(csv_rows[0].keys()))
        w.writeheader()
        w.writerows(csv_rows)
    print(f"\nWrote {len(csv_rows)} rows -> {OUT_CSV}")


def self_check():
    # _stats: 3 turns, known latencies/words -> known median + ms/word
    pairs = [(2.0, 2), (4.0, 4), (6.0, 3)]  # ms/word = 1000, 1000, 2000
    med, lo, hi, n, mspw = _stats(pairs)
    assert med == 4.0 and n == 3, (med, n)
    assert mspw == 1000.0, mspw
    # warmup drop: first dialogue skipped
    entry = {"dialogue_results": [
        {"turns": [{"latency_s": 99, "generated": "x"}]},   # d0 -> dropped
        {"turns": [{"latency_s": 1.0, "generated": "a b"}]},
    ]}
    got = list(_turn_latencies(entry, warmup=1))
    assert got == [(1.0, 2)], got
    print("timing_analysis self-check passed")


if __name__ == "__main__":
    if "--self-check" in sys.argv:
        self_check()
    else:
        analyse()
