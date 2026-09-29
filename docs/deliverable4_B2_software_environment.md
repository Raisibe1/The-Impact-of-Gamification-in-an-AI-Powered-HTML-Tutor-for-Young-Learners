# B2: Software Environment

## Overview

The project uses a Python virtual environment to isolate dependencies from the host machine. This ensures reproducibility across different development environments.

---

## Technology Stack

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| Language | Python | 3.14 | Backend & data processing |
| Virtual Environment | venv | built-in | Isolate dependencies |
| Backend Framework | FastAPI | 0.141.1 | REST API |
| ASGI Server | Uvicorn | 0.54.0 | Run FastAPI |
| Templating | Jinja2 | (see requirements) | Server-rendered HTML |
| Validation | Pydantic | (see requirements) | Request data validation |
| Database | SQLite | built-in | Persistent storage |
| Password Hashing | pwdlib | (see requirements) | Secure password storage |
| Data Processing | pandas | 3.0.6 | Data manipulation |
| Machine Learning | scikit-learn | 1.9.1 | Model training |
| Datasets | Hugging Face | (see requirements) | Data download |
| Version Control | Git | 2.55.0 | Source control |

---

## Environment Setup Steps

### Step 1: Create Virtual Environment

