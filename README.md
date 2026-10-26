# The-Impact-of-Gamification-in-an-AI-Powered-HTML-Tutor-for-Young-Learners

## What this branch does

The service loads a trained scikit-learn model and exposes an HTTP API
that estimates a learner's probability of passing a future independent
HTML-topic checkpoint, using a defined set of **35 input features**.

The prediction is intended to support evaluation and tutor adaptation.
It is **not a substitute for the learner's actual checkpoint result**
and must not independently grant or block progression.

## Important status and limitations

-   Training interactions and checkpoint labels used for the current
    model are **synthetic**.
-   Reported model metrics are development results, not evidence of
    validated performance with real learners.
-   Start in **shadow/advisory mode** while the application team
    validates feature mapping, reliability, privacy, and behaviour.
-   Use the approved independent checkpoint and progression policy to
    determine mastery.
-   Do not send names or other directly identifying learner information
    to the model service. Use a pseudonymous ID only if needed.

## Repository contents

The handover package for this branch is expected to include:

-   `app.py` --- API application and prediction endpoint.
-   `requirements.txt` --- Python dependencies.
-   `synthetic_topic_mastery_predictor.joblib` --- trained model
    artifact.
-   `feature_contract.json` --- expected model feature names and
    contract.
-   `tests/` --- basic API and input-validation tests.
-   `README.md` --- this file.

If your branch uses different paths or filenames, update this list to
match the repository.

## Requirements

-   Python 3.11 recommended.
-   `pip`
-   The files listed above, including the model artifact and feature
    contract.

## Run locally

From the directory containing `app.py`:

### 1. Create and activate a virtual environment

**Windows PowerShell**

``` powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

``` bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the API

``` bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

The service should now be available locally.

## API endpoints

  -----------------------------------------------------------------------
  Method                  Endpoint                Purpose
  ----------------------- ----------------------- -----------------------
  `GET`                   `/health`               Check whether the
                                                  service is running and
                                                  the model loaded.

  `GET`                   `/schema`               Inspect the expected
                                                  feature contract.

  `POST`                  `/predict`              Submit the feature
                                                  values and receive a
                                                  predicted
                                                  checkpoint-pass
                                                  probability.

  `GET`                   `/docs`                 Open the interactive
                                                  API documentation
                                                  (FastAPI/Swagger UI).
  -----------------------------------------------------------------------

### Example request

The exact feature names and allowed values are defined by
`feature_contract.json` and the `/schema` endpoint. Send **all required
feature keys** with values computed by the application backend from
information available before the checkpoint.

``` json
{
  "learner_id": "pseudonymous-learner-001",
  "features": {
    "replace_with_feature_name_from_schema": 0.5
  }
}
```

This is an illustrative shape only, **not a complete valid request**.
Replace the placeholder with the actual schema and include all required
feature fields. Do not invent feature names or send a partial feature
object.

### Example response

The precise response fields are defined by the running service. A
successful prediction should provide an estimated probability and
relevant model/status metadata. Treat the probability as advisory, not
as a mastery decision.

## Integrating with the tutor backend

1.  **Inspect the contract.** Open `/schema` or read
    `feature_contract.json` and confirm the exact 35 feature names,
    types, and expected ranges.
2.  **Map source events.** Map the contract to the tutor's actual
    database tables/event logs (for example, attempts, correctness,
    hints, reviews, response times, and topic context where those are
    defined in the contract).
3.  **Calculate features server-side.** Build the feature object from
    events recorded before the checkpoint. Avoid data leakage: do not
    include the checkpoint outcome or any information recorded after it.
4.  **Validate values.** Follow the contract for numeric ranges, missing
    values, and categorical encodings. Fractions should use the scale
    specified by the contract.
5.  **Call the API server-to-server.** Keep the model service behind the
    backend; do not expose it directly to the browser.
6.  **Handle failures safely.** Add a timeout, log operational errors
    without sensitive learner data, and provide a neutral fallback if
    the service is unavailable.
7.  **Keep progression separate.** The independent checkpoint and the
    approved progression rules remain authoritative.
8.  **Validate before use.** Compare predictions with later real
    checkpoint outcomes and review performance across relevant learner
    groups before considering broader use.

## Run tests

If the repository includes the supplied tests, run:

``` bash
pytest -q
```
