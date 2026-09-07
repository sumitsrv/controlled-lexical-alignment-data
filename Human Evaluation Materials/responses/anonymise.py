#!/usr/bin/env python3
"""Anonymise the V3 human-evaluation responses for public release.

Replaces every participant identifier with a sequential pseudonym (judge_01..judge_50)
and writes the pseudonym -> identifier lookup to a SEPARATE private file that must
never be committed to the public data repository.
"""
import csv, os

RAW = ("/home/sumit-srivastava/Documents/PhD/Research/Lexical aligning agents/recovered/"
       "old_code/User Study/V3/Data/lingalignmodels_study_November 11, 2025_04.24.csv")
REPO = "/home/sumit-srivastava/Documents/PhD/Research/Controlled Lexical Alignment - Data"
OUT_DIR = os.path.join(REPO, "Human Evaluation Materials", "responses")
PRIVATE = "/home/sumit-srivastava/Documents/PhD/Research/_private_lookups"

ID_COLS = ["ResponseId", "QID16", "PROLIFIC_PID"]   # all participant-identifying columns

# pair -> (order1-2 column, order2-1 column, model, topic, weight)
PAIRS = [("Q24", "Q25", "BlenderBot-3B",         "culture-2",   75),
         ("Q30", "Q31", "BlenderBot-3B",         "culture",     25),
         ("Q36", "Q37", "Llama-2-7b-chat",       "health",     750),
         ("Q42", "Q43", "Llama-2-7b-chat",       "environment",1000),
         ("Q48", "Q49", "Phi-3.5-mini-instruct", "culture",   3500),
         ("Q60", "Q61", "Phi-3.5-mini-instruct", "education", 3250)]

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PRIVATE, exist_ok=True)

rows = list(csv.reader(open(RAW, encoding="utf-8")))
header, data = rows[0], rows[1:]
idx = {c: header.index(c) for c in header}

# ---- assign pseudonyms in file order ----
lookup = []
for n, row in enumerate(data, start=1):
    jid = "judge_%02d" % n
    lookup.append([jid] + [row[idx[c]] for c in ID_COLS])
    for c in ID_COLS:
        row[idx[c]] = jid if c == "ResponseId" else ""
    row[idx["ResponseId"]] = jid

# rename ResponseId -> judge_id, drop the now-empty identifier columns
drop = {idx["QID16"], idx["PROLIFIC_PID"]}
header[idx["ResponseId"]] = "judge_id"
keep = [i for i in range(len(header)) if i not in drop]

with open(os.path.join(OUT_DIR, "responses_anonymised.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow([header[i] for i in keep])
    for row in data:
        w.writerow([row[i] for i in keep])

# ---- tidy long format, with A/B resolved to condition ----
long_rows = []
for row in data:
    jid = row[idx["ResponseId"]]
    for c1, c2, model, topic, weight in PAIRS:
        a, b = row[idx[c1]], row[idx[c2]]
        if a:
            shown, raw = "order1-2", a           # Dialogue A = baseline
            res = {"Dialogue A": "baseline", "Dialogue B": "weighted",
                   "No Difference": "no_difference"}[raw]
        elif b:
            shown, raw = "order2-1", b           # Dialogue A = weighted
            res = {"Dialogue A": "weighted", "Dialogue B": "baseline",
                   "No Difference": "no_difference"}[raw]
        else:
            continue
        long_rows.append([jid, model, topic, weight, shown, raw, res])

with open(os.path.join(OUT_DIR, "responses_long.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["judge_id", "model", "topic", "weight", "order_shown",
                "choice_as_shown", "choice_resolved"])
    w.writerows(long_rows)

# ---- private lookup, OUTSIDE the public repo ----
lp = os.path.join(PRIVATE, "human_eval_251366_judge_lookup.csv")
with open(lp, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["judge_id"] + ID_COLS)
    w.writerows(lookup)
os.chmod(lp, 0o600)

print("judges:            %d" % len(lookup))
print("long-format rows:  %d" % len(long_rows))
print("public  -> %s" % OUT_DIR)
print("private -> %s (mode 600)" % lp)
