from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ml_inference import FEATURES, ModelInputError, ModelService  # noqa: E402

service = ModelService()
example = pd.read_csv("dataset.csv")
example = example[FEATURES]

#Convert NaN -> None so the validator treats them as missing, not as bad floats
def row_to_payload(row: pd.Series) -> dict:
    return {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}

#Predict on a single row (first interaction)
payload = row_to_payload(example.iloc[0])
result = service.predict(payload)
print("p_correct  :", result["p_next_interaction_correct"])
print("p_incorrect:", result["p_next_interaction_incorrect"])

import sqlite3
conn = sqlite3.connect("tutor.db")
example.to_sql("secondarydata",conn,if_exists="replace", index=False)
conn.close()