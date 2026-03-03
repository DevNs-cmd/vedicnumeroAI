from datetime import datetime
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

from auth.dependencies import get_current_user
from database import face_collection
from services.face import analyze_face

router = APIRouter(prefix="/api", tags=["face"])


@router.post("/face-read")
async def face_read(file: UploadFile = File(...), user=Depends(get_current_user)):
    image_bytes = await file.read()
    result = analyze_face(image_bytes)

    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])

    doc = {
        "user_id": user["_id"],
        "filename": file.filename,
        "analysis": result,
        "created_at": datetime.utcnow(),
    }
    face_collection.insert_one(doc)

    return {"success": True, **result}
