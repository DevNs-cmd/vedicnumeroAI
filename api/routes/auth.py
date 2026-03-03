from datetime import datetime
from fastapi import APIRouter, HTTPException, status

from database import users_collection
from models.user import UserCreate, UserLogin
from auth.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(payload: UserCreate):
    existing = users_collection.find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_doc = {
        "full_name": payload.full_name,
        "email": payload.email.lower(),
        "password_hash": hash_password(payload.password),
        "dob": payload.dob,
        "birth_place": payload.birth_place,
        "created_at": datetime.utcnow(),
    }

    result = users_collection.insert_one(user_doc)
    token = create_access_token({"sub": str(result.inserted_id)})

    return {"success": True, "token": token}


@router.post("/login")
def login(payload: UserLogin):
    user = users_collection.find_one({"email": payload.email.lower()})
    if not user or not verify_password(payload.password, user.get("password_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["_id"])})
    return {"success": True, "token": token}
