"""In-process inference helper for the HTML Topic Mastery Predictor.

This module does NOT create an HTTP server or API. Import predict_checkpoint_pass()
from the backend's existing service and call it after building the 35-feature mapping.
Only load trusted model artifacts; joblib uses Python pickle serialization.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping

import joblib
import pandas as pd

MODEL_VERSION = "synthetic-logistic-regression-dev-1.0"
DEFAULT_MODEL_PATH = Path(__file__).resolve().parent / "model" / "synthetic_topic_mastery_predictor.joblib"

FEATURES = [
    "practice_interaction_count", "unique_question_count", "first_attempt_accuracy", "final_accuracy",
    "recent5_first_attempt_accuracy", "recent3_first_attempt_accuracy", "unassisted_first_attempt_accuracy",
    "accuracy_without_hint", "accuracy_after_review", "accuracy_when_hinted", "mean_attempt_count", "hint_rate",
    "review_rate", "mean_review_visits", "mean_response_time_seconds", "median_response_time_seconds",
    "correct_streak_end", "mean_question_difficulty", "support_gap", "recent5_hint_rate", "recent5_review_rate",
    "last_interaction_first_correct", "first_vs_recent_accuracy_gain", "initial_wrong_recovery_rate",
    "unassisted_interaction_rate", "prior_topics_completed", "previous_topic_checkpoint_score",
    "prior_topic_checkpoint_score_mean", "previous_topic_mastery_label", "prior_topic_mastery_rate",
    "prior_topic_first_attempt_accuracy_mean", "prior_topic_unassisted_accuracy_mean", "prior_topic_hint_rate_mean",
    "prior_topic_review_rate_mean", "topic_id",
]
NUMERIC_FEATURES = [name for name in FEATURES if name != "topic_id"]

_model_cache: Any = None
_model_path_cache: str | None = None
print("Creating model prediction")

def load_model(model_path: str | os.PathLike[str] | None = None):
    """Load the fitted scikit-learn pipeline once per process."""
    global _model_cache, _model_path_cache
    path = str(model_path or os.environ.get("HTML_TUTOR_ML_MODEL_PATH", DEFAULT_MODEL_PATH))
    if _model_cache is None or _model_path_cache != path:
        _model_cache = joblib.load(path)
        _model_path_cache = path
    return _model_cache


def predict_checkpoint_pass(features: Mapping[str, Any], model_path: str | os.PathLike[str] | None = None) -> dict[str, Any]:
    """Return the estimated probability of passing a future independent topic checkpoint.

    `features` must contain exactly the 35 feature keys listed in README.md. Numeric
    features may be None when unavailable; the fitted pipeline imputes missing values.
    All feature calculations must use only events recorded before the checkpoint.
    """
    if not isinstance(features, Mapping):
        raise TypeError("features must be a mapping/dictionary")
    missing = [key for key in FEATURES if key not in features]
    extra = [key for key in features if key not in FEATURES]
    if missing or extra:
        parts = []
        if missing:
            parts.append("missing feature(s): " + ", ".join(missing))
        if extra:
            parts.append("unknown feature(s): " + ", ".join(map(str, extra)))
        raise ValueError("; ".join(parts))

    topic_id = features["topic_id"]
    if not isinstance(topic_id, str) or topic_id not in {f"T{i:03d}" for i in range(1, 10)}:
        raise ValueError("topic_id must be one of T001 through T009")

    row = {}
    for key in NUMERIC_FEATURES:
        value = features[key]
        if value is None:
            row[key] = None
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{key} must be a number or None; booleans are not accepted")
        row[key] = value
    
    row["topic_id"] = topic_id
    frame = pd.DataFrame([row], columns=FEATURES)
    model = load_model(model_path)
    print("SEE MODEL")
    print(model)
    probability = float(model.predict_proba(frame)[0][1])
    imputed = [key for key in NUMERIC_FEATURES if row[key] is None]
    
    return {
        "probability_checkpoint_pass": probability,
        "model_name": "HTML Topic Mastery Predictor",
        "model_version": MODEL_VERSION,
        "evidence_status": "development_candidate_synthetic_data_only",
        "imputed_features": imputed,
        "progression_authorized": False,
        "required_next_step": "Use an independent checkpoint and approved progression policy; do not progress based on this probability alone.",
    }
