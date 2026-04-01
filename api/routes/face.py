from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from services.face import analyze_face

router = APIRouter(prefix="/api", tags=["Face"])

security = HTTPBearer()

ALLOWED_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


# @router.post("/face-read")
# async def face_read(
#     file: UploadFile = File(...),
#     credentials: HTTPAuthorizationCredentials = Depends(security),
# ):

from fastapi import Request

@router.post("/face-read")
async def face_read(
    request: Request,
    file: UploadFile = File(...)
):


    # validate file
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Invalid image type. Upload JPG or PNG."
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image too large (max 5MB)"
        )

    try:
        result = analyze_face(image_bytes)

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail=f"Face analysis failed: {str(e)}"
        )

    # Save to JSON database
    from database import face_collection
    from datetime import datetime
    
    # Try to extract user ID if they are logged in
    user_id = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            from auth.security import decode_access_token
            payload = decode_access_token(token)
            user_id = payload.get("sub")
        except Exception:
            pass
            
    doc = {
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
        # Save all the extracted fields
        "face_shape": result.get("face_shape"),

        "forehead": result.get("forehead"),
        "eye_distance": result.get("eye_distance"),
        "eyebrows": result.get("eyebrows"),
        "nose": result.get("nose"),
        "lips": result.get("lips"),
        "jawline": result.get("jawline"),
        "symmetry": result.get("symmetry"),
        "symmetry_score": result.get("symmetry_score"),
        "confidence": result.get("confidence")
    }
    face_collection.insert_one(doc)


    return {
        # Core classifications
        "face_shape":     result.get("face_shape"),
        "forehead":       result.get("forehead"),
        "eye_distance":   result.get("eye_distance"),
        "eyebrows":       result.get("eyebrows"),
        "nose":           result.get("nose"),
        "lips":           result.get("lips"),
        "jawline":        result.get("jawline"),
        "symmetry":       result.get("symmetry"),
        "symmetry_score": result.get("symmetry_score"),
        "confidence":     result.get("confidence"),
        # Predictions
        "personality_analysis": result.get("personality_analysis"),
        "career_prediction":    result.get("career_prediction"),
        "relationship_traits":  result.get("relationship_traits"),
        "planet_summary":       result.get("planet_summary"),
        # Detailed readings per feature
        "detailed_readings":    result.get("detailed_readings"),
    }
