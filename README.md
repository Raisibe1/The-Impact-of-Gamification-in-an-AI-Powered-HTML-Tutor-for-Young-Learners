# The Impact of Gamification in an AI-Powered HTML Tutor for Young Learners

## Project Overview
This project aims to design, build, and test a low-cost AI-powered study tutor that teaches HTML and web development to learners in Grades 7-9 in South Africa.

## Team Roles
- **Raisibe Sebetha** – Project Manager & UX Lead
- **Sizwe Makgalemele** – Software Engineer, Backend
- **Buyiswa Ngobeni** – Software Engineer, Frontend
- **Purity Bonyongwa** – Machine Learning Engineer
- **Lonwabo Ntikinca** – Machine Learning Engineer 
- **Tshiamo Matshaba** – Data Engineer & Analyst

## Data Engineering Repository Structure
├── notebooks/ # Jupyter notebooks for EDA and analysis
├── scripts/ # Python scripts for data cleaning & feature engineering
├── data/
│ ├── reference/ # Small reference files (syllabus, QA pairs, templates)
│ └── raw/ # Placeholder - large datasets stored elsewhere
├── outputs/
│ └── figures/ # Visualisations for dissertation
└── docs/ # Documentation (data dictionary, model specs)

## Data Sources
- EdNet Dataset
(## The raw data is **NOT** stored on GitHub due to file size limits.

### EdNet-KT3 Dataset

- **Source:** EdNet (Santa tutoring service, Korea)
- **Download:** [https://bit.ly/ednet-kt3](https://bit.ly/ednet-kt3)
- **Size:** 762 MB (compressed) / ~4.3 GB (extracted)
- **Format:** ZIP file → CSV files (one per student)
### Setup Instructions

1. Download the ZIP file from the link above
2. Extract the contents to `data/raw/KT3/`
3. You should see CSV files like `1.csv`, `2.csv`, etc.)

- ASSISTments 2009-2010 Dataset
- ConvoLearn Dataset
- StudyChat Dataset
(## The raw data is **NOT** stored on GitHub due to file size limits.

### Download from Google Drive

[**Download Raw Data Folder**](https://drive.google.com/drive/folders/1m1XdbMPcJKMS7myBaH5byA77xEnmgzMn?usp=sharing)

**Contents:**

| Dataset | Size | Description |
| :--- | :--- | :--- |
| ASSISTments | ~20 MB | Classic Knowledge Tracing benchmark |
| ConvoLearn | ~3 MB | Teacher-student tutoring dialogues |
| StudyChat | ~1 MB | Student-LLM conversations |

### Setup Instructions

1. Download the folder from Google Drive
2. Place it inside your project as `data/raw/`
3. Verify the path: `data/raw/convolearn.csv`, etc.
4. Run `python scripts/check_data.py` to verify everything is in place)

## Setup Instructions
```bash
# Create virtual environment
python -m venv venv_data

# Activate (Mac/Linux)
source venv_data/bin/activate

# Activate (Windows)
venv_data\Scripts\activate

# Install dependencies
pip install -r requirements.txt