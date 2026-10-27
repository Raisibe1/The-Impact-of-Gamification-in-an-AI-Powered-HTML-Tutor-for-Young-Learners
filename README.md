## Included files

- `model/synthetic_topic_mastery_predictor.joblib` — trained scikit-learn preprocessing + Logistic Regression pipeline.
- `inference.py` — in-process helper function; no web server is created.
- `feature_contract.json` — machine-readable list/order of the 35 expected feature names and core rules.
- `requirements.txt` — versions used to load the provided artifact.
- `tests/test_inference.py` — minimal local smoke tests.
- `README.md` — setup notes and the full feature dictionary.

## What the model predicts

It estimates the probability of passing a **future independent HTML-topic checkpoint**. The development target used a checkpoint pass threshold of at least 4/5 correct (80%). It is a prediction, not proof of mastery.

**Evidence limitation:** the model was trained and evaluated using synthetic learner interaction and checkpoint data. It has not been validated on real learners or the live tutor event schema. Use it in shadow/advisory mode until it has been evaluated appropriately. Never use the probability alone to award mastery, block a learner, or unlock a topic; use the independent checkpoint and the team's approved progression policy.

## Quick integration

Recommended Python environment: Python 3.11, with package versions from `requirements.txt` installed in the backend's environment (coordinate dependency compatibility with the existing application before changing its shared environment).

```bash
python -m pip install -r requirements.txt
```

Copy this folder into the backend repository or place the model artifact where the backend can read it. From backend Python code:

```python
from inference import predict_checkpoint_pass

# `features` must be a dictionary containing all 35 keys listed below.
result = predict_checkpoint_pass(features)
probability = result["probability_checkpoint_pass"]
```

This is a **Python function call**, not an HTTP call. Your team can wrap it in the existing endpoint/controller however it sees fit. The function validates that all feature keys are present and rejects unknown keys. Numeric values may be `None` when genuinely unavailable; the fitted pipeline imputes missing values and returns the names of imputed fields. `topic_id` must be one of `T001`–`T009`.

If the model is stored in another location, set `HTML_TUTOR_ML_MODEL_PATH` to the trusted `.joblib` file path before the application process starts, or pass `model_path=` to `predict_checkpoint_pass()`. **Only load a trusted model file**: joblib uses Python pickle serialization.

## The 35 required model features

All 35 keys must be supplied on every prediction call. Use the exact spelling below. Feature calculations must match the definitions used during training. Unless specified otherwise, a rate/accuracy/score is a fraction from `0` to `1`, not a percentage from `0` to `100`. Counts should be non-negative. Numeric fields may be `None` only when unavailable; do not invent data to fill gaps.

| # | Exact feature key | Meaning / calculation guidance |
|---:|---|---|
| 1 | `practice_interaction_count` | Number of practice questions answered before the current topic checkpoint. |
| 2 | `unique_question_count` | Number of distinct question IDs encountered in practice for this topic. |
| 3 | `first_attempt_accuracy` | Mean correctness on the first attempt across topic practice. |
| 4 | `final_accuracy` | Mean final correctness after retries across topic practice. |
| 5 | `recent5_first_attempt_accuracy` | First-attempt accuracy over the most recent five practice interactions. If unavailable, use `None`. |
| 6 | `recent3_first_attempt_accuracy` | First-attempt accuracy over the most recent three practice interactions. If unavailable, use `None`. |
| 7 | `unassisted_first_attempt_accuracy` | First-attempt accuracy where neither a hint nor a content review preceded the response. |
| 8 | `accuracy_without_hint` | First-attempt accuracy on interactions without a hint, whether or not content was reviewed. |
| 9 | `accuracy_after_review` | Final correctness on interactions preceded by content review. |
| 10 | `accuracy_when_hinted` | First-attempt accuracy on interactions where a hint was used before answering. |
| 11 | `mean_attempt_count` | Average number of attempts recorded per practice question. |
| 12 | `hint_rate` | Share of practice interactions with a hint used before the answer. |
| 13 | `review_rate` | Share of practice interactions preceded by at least one content-review visit. |
| 14 | `mean_review_visits` | Average number of content-review visits before practice answers. |
| 15 | `mean_response_time_seconds` | Mean response time in seconds for topic practice interactions. |
| 16 | `median_response_time_seconds` | Median response time in seconds for topic practice interactions. |
| 17 | `correct_streak_end` | Number of consecutive first-attempt correct responses at the end of the practice history. |
| 18 | `mean_question_difficulty` | Average editorial difficulty rating of questions encountered. Preserve the same difficulty scale used in training. |
| 19 | `support_gap` | `final_accuracy - unassisted_first_attempt_accuracy`. May be negative. |
| 20 | `recent5_hint_rate` | Share of the last five practice interactions with a hint used. |
| 21 | `recent5_review_rate` | Share of the last five practice interactions preceded by content review. |
| 22 | `last_interaction_first_correct` | Whether the most recent practice response was correct on the first attempt; encode as `1` or `0`. |
| 23 | `first_vs_recent_accuracy_gain` | First-attempt accuracy in the later half of practice minus first-attempt accuracy in the earlier half. May be negative. |
| 24 | `initial_wrong_recovery_rate` | Share of initially incorrect practice responses ultimately corrected on a later attempt. Use `None` if no initial errors make it undefined. |
| 25 | `unassisted_interaction_rate` | Share of practice interactions without either a preceding hint or content review. |
| 26 | `prior_topics_completed` | Count of earlier topics in the defined curriculum sequence with recorded practice/checkpoint outcomes. Earlier topics only. |
| 27 | `previous_topic_checkpoint_score` | Checkpoint score from the immediately preceding topic, recorded before the current-topic prediction. |
| 28 | `prior_topic_checkpoint_score_mean` | Mean checkpoint score across all earlier topics. Earlier topics only. |
| 29 | `previous_topic_mastery_label` | Pass/fail label from the immediately preceding topic checkpoint, encoded consistently as `1`/`0`. Never use the current topic's label. |
| 30 | `prior_topic_mastery_rate` | Fraction of earlier topic checkpoints passed before the current topic. |
| 31 | `prior_topic_first_attempt_accuracy_mean` | Mean first-attempt accuracy across earlier topic practice histories. |
| 32 | `prior_topic_unassisted_accuracy_mean` | Mean unassisted first-attempt accuracy across earlier topics. |
| 33 | `prior_topic_hint_rate_mean` | Mean hint-use rate across earlier topics. Hint use is not automatically a deficit. |
| 34 | `prior_topic_review_rate_mean` | Mean content-review rate across earlier topics. Reviewing is not automatically a deficit. |
| 35 | `topic_id` | Stable ID for the current HTML topic; accepted values are `T001` through `T009`. |

### Feature calculation rules

- Calculate features server-side from persisted tutor events; the model does **not** derive them from raw events.
- Only use information available before the checkpoint being predicted. Do not leak the current checkpoint score/outcome into features.
- For prior-topic features, include only topics completed earlier in the agreed curriculum sequence.
- Accuracy/rate/score fields are fractions in `[0, 1]`; never send `75` to mean 75%—send `0.75`.
- `support_gap` and `first_vs_recent_accuracy_gain` can be negative.
- Use the same units and definitions as training for response time and question difficulty.
- Keep question/topic IDs and event definitions stable. If the live app's events differ, document and review the mapping before using predictions.
- Do not use an empty or missing value as a made-up zero. Use `None` when a numeric feature cannot be calculated.
