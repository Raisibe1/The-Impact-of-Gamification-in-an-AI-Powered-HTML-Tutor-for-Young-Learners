

\# Section 4: Pipeline \& Workflow Automation



\*\*Responsible: Data Engineer (Tshiamo) + Backend Developer (Sizwe)\*\* | 



\---



\## PART A: OVERVIEW



The AI Tutor system follows a modular pipeline that connects data processing, model training, backend API, and frontend interaction into a single reproducible workflow.



\### Full System Architecture

┌─────────────────────────────────────────────────────────┐

│ LEARNER INTERFACE │

│ (HTML Lessons, Quizzes, Coding Exercises) │

└─────────────────────────────────────────────────────────┘

│

▼

┌─────────────────────────────────────────────────────────┐

│ FRONTEND APPLICATION │

│ (HTML + CSS + JavaScript) │

│ Captures learner interaction │

└─────────────────────────────────────────────────────────┘

│

▼

┌─────────────────────────────────────────────────────────┐

│ FastAPI BACKEND │

│ (API Routes + Authentication + Sessions) │

└─────────────────────────────────────────────────────────┘

│ │ │

▼ ▼ ▼

┌─────────────┐ ┌─────────────┐ ┌─────────────┐

│ SQL Database│ │Trained Model│ │Personalized │

│(Interaction │ │ (Classifier)│ │ Feedback │

│ Logs) │ │ │ │ Generator │

└─────────────┘ └─────────────┘ └─────────────┘

│

▼

┌─────────────────────────────────────────────────────────┐

│ DATA \& ML PIPELINE │

│ 1. Data Collection 4. Model Training │

│ 2. Data Cleaning 5. Model Validation │

│ 3. Feature Eng. 6. Model Deployment │

└─────────────────────────────────────────────────────────┘



text



\---



\## PART B: DATA ENGINEER DELIVERABLES



\### B1. How does raw data enter the system?



Raw data is downloaded from Hugging Face and Google Drive, then placed in the `data/raw/` folder.



| Dataset | Source | Location | Size |

| :--- | :--- | :--- | :--- |

| StudyChat | Hugging Face (`wmcnicho/StudyChat`) | `data/raw/studychat.csv` | \~47 MB |

| ASSISTments | Hugging Face (`Atomi/ASSISTments2009`) | `data/raw/assistments.csv` | \~20 MB |

| ConvoLearn | Hugging Face (`masharma/convolearn`) | `data/raw/convolearn.csv` | \~3 MB |

| EdNet-KT3 | Zenodo / Google Drive | `data/raw/KT3/` | \~4.3 GB |



\### B2. How is it cleaned?



Each dataset has a dedicated preprocessing script:



| Dataset | Script | What It Does |

| :--- | :--- | :--- |

| StudyChat | `scripts/preprocess\_studychat.py` | Extracts labels, groups meta-categories, engineers features |

| ASSISTments | `scripts/preprocess\_assistments.py` | (To be created) |

| ConvoLearn | `scripts/preprocess\_convolearn.py` | (To be created) |



\*\*StudyChat cleaning steps:\*\*

1\. Extract `label` from `llm\_label` JSON column

2\. Group 15+ granular labels into 5 meta-categories

3\. Engineer features: `prompt\_length`, `prompt\_word\_count`, `response\_length`, `num\_turns`

4\. Drop unnecessary columns

5\. Save cleaned data



\### B3. How is it transformed?



\*\*StudyChat transformation:\*\*



| Stage | Input | Output |

| :--- | :--- | :--- |

| Extract label | `llm\_label` (JSON) | `label` (string) |

| Group categories | 15+ labels | 5 meta-categories |

| Feature engineering | raw text | `prompt\_length`, `num\_turns`, etc. |

| Column selection | 13 columns | 11 columns |



\### B4. How is it prepared for the model?



\- \*\*Input features:\*\* `prompt` (text), `prompt\_length`, `prompt\_word\_count`, `num\_turns`

\- \*\*Target variable:\*\* `label` (5 classes)

\- \*\*Output:\*\* `data/processed/studychat\_cleaned.csv`



\### B5. Can preprocessing be repeated automatically?



\*\*Yes.\*\* Run the master pipeline script:

