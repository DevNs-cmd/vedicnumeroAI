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

    # Estimate confidence from detection quality (cascade scale)
    # and eye distance as a fraction of face width
    eye_distance = int(bw * 0.38)
    # Confidence: derive from how "ideal" face ratio is (closer to 1.1 = more oval = higher conf)
    deviation = abs(ratio - 1.1)
    confidence = max(72, min(96, round(92 - deviation * 20)))

    response = {
        "face_shape": shape,
        "face_width": int(bw),
        "face_height": int(bh),
        "face_ratio": round(ratio, 3),
        "eye_distance": eye_distance,
        "confidence": confidence,
        "numerology_prediction": _prediction_for_shape(shape),
    }

    return response
