# Before/After Data Summary — StudyChat

## Before Preprocessing

| Metric | Value |
| :--- | :--- |
| Rows | 16,851 |
| Columns | 13 |
| Missing values | (fill in) |
| Duplicates | (fill in) |
| Target classes | 15+ |
| Target encoding | JSON string |

## After Preprocessing

| Metric | Value |
| :--- | :--- |
| Rows | 16,851 |
| Columns | 11 |
| Missing values | 0 |
| Duplicates | 0 |
| Target classes | 5 |
| Target encoding | String labels |

## Changes Made

| Action | Details |
| :--- | :--- |
| Columns removed | timestamp, chatTitle, llm_label, messages, interactionCount, chatStartTime, chatTotalInteractionCount |
| Features created | prompt_length, prompt_word_count, response_length, num_turns, label |
| Target variable | Extracted from llm_label JSON → grouped into 5 meta-categories |

## Final Columns

| Column | Type | Purpose |
| :--- | :--- | :--- |
| prompt | Text | Input feature |
| response | Text | Reference output |
| topic | Categorical | Context |
| label | Categorical | TARGET variable |
| prompt_length | Numerical | Feature |
| prompt_word_count | Numerical | Feature |
| response_length | Numerical | Feature |
| num_turns | Numerical | Feature |
| chat_id | String | Identifier |
| user_id | String | Identifier |
| semester | Categorical | Context |

## Evidence

- File: data/processed/studychat_cleaned.csv
- Screenshot: Before/after shape
- Screenshot: Preprocessing script output

\## Data Source



\- \*\*Original:\*\* Hugging Face (`wmcnicho/StudyChat`)

\- \*\*Reference:\*\* McNichols et al. (2026) — The StudyChat Dataset

\- \*\*License:\*\* CC BY 4.0

