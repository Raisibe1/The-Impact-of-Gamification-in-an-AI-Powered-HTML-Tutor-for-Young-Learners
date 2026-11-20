"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
"""Existing model integration; copy your trained ml_inference.py and model artifacts."""
from ml_inference import predict_checkpoint_pass, FEATURES

def sample_features():
    values = {name: 0.5 for name in FEATURES if name != "topic_id"}
    values.update({
        "practice_interaction_count": 8,
        "unique_question_count": 5,
        "mean_attempt_count": 1.5,
        "mean_review_visits": 0.5,
        "mean_response_time_seconds": 24,
        "median_response_time_seconds": 20,
        "correct_streak_end": 2,
        "mean_question_difficulty": 2,
        "prior_topics_completed": 1,
        "previous_topic_mastery_label": 1,
        "last_interaction_first_correct": 1,
        "topic_id": "T002",
    })
    return values

if __name__ == "__main__":
    test = sample_features()
    result = predict_checkpoint_pass(test)
    print(result)