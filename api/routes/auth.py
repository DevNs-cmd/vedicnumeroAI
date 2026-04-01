"""
routes/auth.py  —  Signup & Login endpoints
Data is saved to the JSON file via the JsonCollection in database.py.
All signup details (name, email, dob, birth_place, created_at) are persisted.
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, status

from database import users_collection
from models.user import UserCreate, UserLogin
from auth.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(payload: UserCreate):
    # ── Validate required fields ──────────────────────────────────────
    if not payload.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )
    if not payload.password or len(payload.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters"
        )

    # ── Check duplicate ───────────────────────────────────────────────
    existing = users_collection.find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered. Please login instead."
        )

    # ── Build & save user document ────────────────────────────────────
    user_doc = {
        "full_name":     payload.full_name or "",
        "email":         payload.email.lower(),
        "password_hash": hash_password(payload.password),
        "dob":           payload.dob or "",
        "birth_place":   payload.birth_place or "",
        "created_at":    datetime.utcnow().isoformat(),
    }

    result = users_collection.insert_one(user_doc)          # written to db.json
    token  = create_access_token({"sub": str(result.inserted_id)})

    return {
        "success":   True,
        "token":     token,
        "full_name": user_doc["full_name"],
        "email":     user_doc["email"],
    }


@router.post("/login")
def login(payload: UserLogin):
    if not payload.email or not payload.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    user = users_collection.find_one({"email": payload.email.lower()})
    hashed = user.get("password_hash") if user else None
    
    if not user or not hashed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. Please check your credentials."
        )
        
    try:
        is_valid = verify_password(payload.password, hashed)
    except Exception:
        is_valid = False

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. Please check your credentials."
        )

    token = create_access_token({"sub": str(user["_id"])})
    return {
        "success":   True,
        "token":     token,
        "full_name": user.get("full_name", ""),
        "email":     user.get("email", ""),
    }


@router.get("/me")
def me_endpoint(token_data: dict = None):
    """Quick health-check — returns auth status."""
    return {"status": "ok"}
