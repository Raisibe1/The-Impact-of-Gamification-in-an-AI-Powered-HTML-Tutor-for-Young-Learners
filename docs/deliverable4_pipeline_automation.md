# Pipeline & Workflow Automation

## Overview

This document describes the complete pipeline and workflow automation for the AI-Powered HTML Tutor project, covering both the **Data Engineering** and **Backend Development** sides.

---

## PART A: DATA ENGINEER — Data Pipeline

### A1. How does raw data enter the system?

Raw data is downloaded from Hugging Face and Google Drive, then placed in the `data/raw/` folder.

| Dataset | Source | Location | Size |
| :--- | :--- | :--- | :--- |
| StudyChat | Hugging Face (wmcnicho/StudyChat) | `data/raw/studychat.csv` | ~47 MB |
| ASSISTments | Hugging Face (Atomi/ASSISTments2009) | `data/raw/assistments.csv` | ~20 MB |
| ConvoLearn | Hugging Face (masharma/convolearn) | `data/raw/convolearn.csv` | ~3 MB |
| EdNet-KT3 | Zenodo / Google Drive | `data/raw/KT3/` | ~4.3 GB |

### A2. How is it cleaned?

Each dataset has a dedicated preprocessing script:

| Dataset | Script | What It Does |
| :--- | :--- | :--- |
| StudyChat | `scripts/preprocess_studychat.py` | Extracts labels, groups meta-categories, engineers features |
| ASSISTments | `scripts/preprocess_assistments.py` | (To be created) |
| ConvoLearn | `scripts/preprocess_convolearn.py` | (To be created) |

### A3. How is it transformed?

**StudyChat pipeline:**
1. Extract `label` from `llm_label` JSON column
2. Group 15+ granular labels into 5 meta-categories (Writing, Conceptual, Contextual, Providing Context, Verification)
3. Engineer features: `prompt_length`, `prompt_word_count`, `response_length`, `num_turns`
4. Drop unnecessary columns
5. Save cleaned data to `data/processed/studychat_cleaned.csv`

### A4. How is it prepared for the model?

- **Input features:** `prompt` (text), `prompt_length`, `prompt_word_count`, `num_turns`
- **Target variable:** `label` (5 classes)
- **Output:** `data/processed/studychat_cleaned.csv`

### A5. Can preprocessing be repeated automatically?

**Yes.** Run the master pipeline script:

