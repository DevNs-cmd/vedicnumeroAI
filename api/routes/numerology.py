from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from auth.dependencies import get_current_user
from database import numerology_collection
from models.numerology import NumerologyRequest
from services.numerology import calculate_moolank_and_bhagyank

router = APIRouter(prefix="/api", tags=["numerology"])


@router.post("/numerology")
def numerology(payload: NumerologyRequest, user=Depends(get_current_user)):
    try:
        moolank, bhagyank, prediction = calculate_moolank_and_bhagyank(payload.dob)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    doc = {
        "user_id":    str(user.get("_id", "")),
        "email":      user.get("email", ""),
        "dob":        payload.dob,
        "moolank":    moolank,
        "bhagyank":   bhagyank,
        "prediction": prediction,
        "created_at": datetime.utcnow().isoformat(),
    }
    numerology_collection.insert_one(doc)   # saved to db.json

    return {
        "success":    True,
        "moolank":    moolank,
        "bhagyank":   bhagyank,
        "prediction": prediction,
    }
