from typing import Dict, Any

import cv2
import numpy as np


def _classify_face_shape(ratio: float) -> str:
    if ratio >= 1.25:
        return "long"
    if ratio <= 0.9:
        return "round"
    return "oval"


def _prediction_for_shape(shape: str) -> str:
    if shape == "long":
        return "Saturn influence: disciplined, thoughtful, and resilient."
    if shape == "round":
        return "Venus influence: warm, affectionate, and artistic."
    return "Jupiter influence: balanced, wise, and growth-oriented."


def analyze_face(image_bytes: bytes) -> Dict[str, Any]:
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    if img is None:
        return {"error": "Invalid image"}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces) == 0:
        return {"error": "No face detected"}

    x, y, bw, bh = faces[0]
    ratio = bh / bw if bw else 0
    shape = _classify_face_shape(ratio)

    response = {
        "face_shape": shape,
        "face_width": int(bw),
        "face_height": int(bh),
        "face_ratio": round(ratio, 3),
        "eye_distance": None,
        "confidence": None,
        "numerology_prediction": _prediction_for_shape(shape),
    }

    return response
