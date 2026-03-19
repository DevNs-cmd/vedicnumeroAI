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

@router.post("/face-read")
async def face_read(
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

    return {
        "face_shape": result.get("face_shape"),
        "confidence": result.get("confidence"),
        "personality_analysis": result.get("personality_analysis"),
        "career_prediction": result.get("career_prediction"),
        "relationship_traits": result.get("relationship_traits"),
        "planet_summary": result.get("planet_summary"),
        "detailed_readings": result.get("detailed_readings"),
    }
