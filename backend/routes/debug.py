from bson import ObjectId
from fastapi import APIRouter, HTTPException

from database import users_collection, numerology_collection, face_collection

router = APIRouter(prefix="/_debug", tags=["debug"])


@router.get("/user")
def user_exists(email: str):
    user = users_collection.find_one({"email": email})
    return {"exists": bool(user), "user_id": str(user["_id"]) if user else None}


@router.get("/numerology")
def numerology_exists(user_id: str, dob: str):
    try:
        oid = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    record = numerology_collection.find_one({"user_id": oid, "dob": dob})
    return {"exists": bool(record)}


@router.get("/face")
def face_exists(user_id: str, filename: str):
    try:
        oid = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    record = face_collection.find_one({"user_id": oid, "filename": filename})
    return {"exists": bool(record)}
