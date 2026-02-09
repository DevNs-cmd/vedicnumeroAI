from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from fastapi.responses import JSONResponse

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OpenCV face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

@app.post("/face-reading")
async def face_reading(file: UploadFile = File(...)):
    image_bytes = await file.read()
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return JSONResponse({"error": "No face detected"})

    (x, y, w, h) = faces[0]

    # --- SIMPLE FACIAL ANALYSIS ---
    face_width = w
    face_height = h

    ratio = face_height / face_width

    # Emotion logic (basic but real geometry)
    if ratio > 1.35:
        emotion = "Calm & Thoughtful"
        confidence = 0.86
        numerology_trait = "Spiritual thinker, destiny aligned with wisdom"
    elif ratio < 1.15:
        emotion = "Bold & Energetic"
        confidence = 0.82
        numerology_trait = "Leader energy, strong Mars influence"
    else:
        emotion = "Balanced & Observant"
        confidence = 0.88
        numerology_trait = "Stable life path, strong Number 2 energy"

    return {
        "emotion": emotion,
        "confidence_score": round(confidence * 100, 2),
        "numerology_prediction": numerology_trait
    }
