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
- ASSISTments 2009-2010 Dataset
- EdNet Dataset
- ConvoLearn Dataset
- StudyChat Dataset

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