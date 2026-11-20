"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
import logging
from fastapi import APIRouter, Request, HTTPException
from core.security import get_current_student
from core.config import DATABASE_PATH as CODEVERSE_DB_PATH
from backend.learning_routes import is_quiz_active
from schemas.predictions import PredictRequest
from services.ml_service import sample_features, predict_checkpoint_pass,FEATURES
from pydantic import BaseModel, EmailStr, Field


logger = logging.getLogger('tutor')
router = APIRouter(tags=['ML Prediction'])
# Preserve API output while avoiding an undefined ModelInputError exception.
class PredictRequest(BaseModel):
    # We only need the student's history, but for testing 
    # we can allow passing features directly.
    features: dict

@router.post('/api/predict-next-correct')
def predict_next_correct(request: Request, payload: PredictRequest):
    # 1. Require auth (optional, but good if this is for a specific user)
    student = get_current_student(request)
    if student is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if is_quiz_active(CODEVERSE_DB_PATH, student["student_id"]):
        raise HTTPException(status_code=423, detail="AI support is disabled during an active quiz.")

    try:

        #testing ML_Model
        print("Try this Bad request? Inside ml_prediction")
        features = sample_features()
        result = predict_checkpoint_pass(features)
        probability = float(result["probability_checkpoint_pass"])
        print("Model Prediction")
        print("------------------")
        print("\nProbability of passing:",probability )

        return {
            "probability_checkpoint_pass": probability,
            "percentage": round(probability * 100, 2),
            "student_id": student["student_id"]
        }
    
    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"ML Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")