# Human Evaluation Materials

Study materials for the human preference evaluation reported in *Lexically Aligned
Generation with LLMs* (INLG). The dialogues themselves are in
[`../Human Evaluation Dialogues/`](../Human%20Evaluation%20Dialogues/); this folder holds
everything else that was put in front of the judges.

## Ethics approval

Reviewed by the **Computer & Information Sciences (CIS) Ethics Committee, University of
Twente**, application nr. **251366**, *"Evaluation of lexically aligned dialogue generation
using large language models"* (researcher: Sumit Srivastava; supervisor: Mariët Theune).
Positive advice issued **2 June 2025**.

Questions about participant rights: `ethicscommittee-cis@utwente.nl`, quoting application
nr. 251366.

## Contents

| Path | What it is |
|------|------------|
| `consent/information_letter_and_consent.pdf` | Information letter, informed consent, and post-task debriefing shown to judges |
| `stimuli/*.html` | The 12 rendered comparison pages, exactly as presented |
| `stimuli/generate_htmls.py` | Script that produced the pages from the dialogue CSVs |
| `stimuli/generation_log.txt` | Generation log for the pages |

## Stimuli and counterbalancing

Six dialogue pairs were shown, each pair rendered in **both display orders** to
counterbalance position within the pair, giving 12 files:

| Pair | Model | Topic | Weights (baseline / weighted) | Files |
|------|-------|-------|-----------------|-------|
| 1 | BlenderBot-3B | culture (2) | 0 / 75 | `bb3b_culture2_order1-2`, `bb3b_culture2_order2-1` |
| 2 | BlenderBot-3B | culture | 0 / 25 | `bb3b_culture_order1-2`, `bb3b_culture_order2-1` |
| 3 | Llama-2-7b-chat | health | 0 / 750 | `llama_health_order1-2`, `llama_health_order2-1` |
| 4 | Llama-2-7b-chat | environment | 0 / 1000 | `llama_environment_order1-2`, `llama_environment_order2-1` |
| 5 | Phi-3.5-mini-instruct | culture | 0 / 3500 | `phi_culture_order1-2`, `phi_culture_order2-1` |
| 6 | Phi-3.5-mini-instruct | education | 0 / 3250 | `phi_education_order1-2`, `phi_education_order2-1` |

In an `order1-2` page the **baseline (weight 0)** dialogue is shown as Dialogue A; in the
corresponding `order2-1` page the **weighted** dialogue is shown as Dialogue A. Each judge
saw one order per pair. The six pairs themselves were presented in a fixed sequence; only
the order *within* each pair was counterbalanced. `stimuli/generation_log.txt` records the
exact source CSV and weight behind every A/B slot.

## Participant instructions

Shown above each comparison:

> **Rank the following dialogues from the best (1) to the worst (2) based on the relevance
> and coherence of the responses by S2.**
>
> **Relevance:** The appropriateness of responses to immediate conversational context,
> i.e., the previous utterance of Speaker 1 (S1).
>
> **Coherence:** The maintenance of thematic consistency and logical progression with
> respect to the full dialogue.

Judges selected the better dialogue in each pair, or *No Difference*.

## Procedure

50 judges were recruited through Prolific and paid an hourly wage of €14.60. Each judge saw
all six pairs in a single session of roughly 15 minutes, yielding 300 preference judgments.
Consent was collected online, actively and anonymously, before the task began.

## Response data

`responses/` holds the judgments from all **50 judges** (300 judgments, 6 per judge).

| File | What it is |
|------|------------|
| `responses_long.csv` | Tidy format, one row per judgment (300 rows). Start here. |
| `responses_anonymised.csv` | The full platform export, one row per judge (50 rows), identifiers removed |
| `anonymise.py` | The script that produced both files from the raw export |

### `responses_long.csv`

| Column | Meaning |
|--------|---------|
| `judge_id` | Pseudonym, `judge_01`–`judge_50` |
| `model`, `topic`, `weight` | Which pair was judged, and the weight of its weighted version |
| `order_shown` | Which counterbalanced page the judge saw (`order1-2` or `order2-1`) |
| `choice_as_shown` | The raw answer: `Dialogue A`, `Dialogue B`, or `No Difference` |
| `choice_resolved` | The answer mapped to condition: `baseline`, `weighted`, or `no_difference` |

**Use `choice_resolved`, not `choice_as_shown`.** Because presentation order was
counterbalanced, "Dialogue A" means the baseline version on an `order1-2` page and the
weighted version on an `order2-1` page. Aggregating the raw labels across orders is
meaningless. Counting `choice_resolved` per pair reproduces the preference table in the
paper exactly (totals: 113 baseline, 130 weighted, 57 no difference).

In the wide file, each pair occupies two columns, one per order, and every judge has a
value in exactly one of them: Q24/Q25 (culture-2), Q30/Q31 (culture), Q36/Q37 (health),
Q42/Q43 (environment), Q48/Q49 (Phi culture), Q60/Q61 (Phi education). In each of these,
the first column is the `order1-2` page and the second the `order2-1` page. The `QID15_*`
columns are the consent items and `Q*_Page Submit` the per-pair response times.

### Anonymisation

Three participant-identifying columns were removed before release: `ResponseId`,
`QID16`, and `PROLIFIC_PID`, the last two being Prolific participant identifiers. They
were replaced by sequential pseudonyms, and the pseudonym-to-identifier lookup is held
privately by the researcher and is deliberately not published. The export contains no IP
address or geolocation fields. Response timestamps and durations are retained, since they
carry no identifying information on their own and are needed to check order effects.
