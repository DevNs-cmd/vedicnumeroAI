import cv2
import numpy as np
import math


# ─────────────────────────────────────────────
#  ASTROLOGY / NUMEROLOGY KNOWLEDGE BASE
# ─────────────────────────────────────────────

FACE_SHAPE_DATA = {
    "Oval": {
        "planet": "Jupiter",
        "element": "Air",
        "personality": (
            "Your oval face reflects Jupiter's balanced energy. You are naturally wise, "
            "diplomatic, and growth-oriented. People are drawn to your calm presence and "
            "open-minded thinking. You adapt easily to changing situations."
        ),
        "career": (
            "Jupiter blesses you with versatility. Ideal careers: Counselor, Teacher, "
            "Diplomat, Writer, Public Relations, Entrepreneur, or Philosopher."
        ),
        "relationship": (
            "You are a harmonious partner who values equality and intellectual connection. "
            "You thrive in relationships built on mutual respect and shared growth."
        ),
    },
    "Round": {
        "planet": "Venus / Moon",
        "element": "Water",
        "personality": (
            "Your round face carries Venus and Moon energy — warm, nurturing, and deeply "
            "creative. You are empathetic, imaginative, and emotionally intelligent. "
            "Social warmth comes naturally to you."
        ),
        "career": (
            "Venus guides you toward beauty, care, and creativity. Ideal careers: Artist, "
            "Musician, Nurse, Chef, Interior Designer, Social Worker, or Actor."
        ),
        "relationship": (
            "You are a devoted and affectionate partner. You love deeply and create a "
            "nurturing home environment. Loyalty and emotional safety are your priorities."
        ),
    },
    "Long": {
        "planet": "Saturn",
        "element": "Earth",
        "personality": (
            "Your long face resonates with Saturn's disciplined vibration. You are "
            "methodical, resilient, and highly principled. You think deeply before acting "
            "and command natural authority."
        ),
        "career": (
            "Saturn rewards your discipline with lasting success. Ideal careers: Lawyer, "
            "Engineer, Scientist, Executive, Accountant, Researcher, or Architect."
        ),
        "relationship": (
            "You are loyal and serious in love. You value stability and long-term "
            "commitment over short-lived romance. Trust is everything to you."
        ),
    },
    "Square": {
        "planet": "Mars / Sun",
        "element": "Fire",
        "personality": (
            "Your square face pulses with Mars and Sun energy — bold, decisive, and "
            "action-driven. You are a natural leader with strong willpower and determination. "
            "Challenges fuel rather than deter you."
        ),
        "career": (
            "Mars drives you toward competitive and impactful roles. Ideal careers: Military, "
            "Sports, Business Leader, Surgeon, Politician, Police, or Athlete."
        ),
        "relationship": (
            "You are passionate and protective in relationships. You pursue love with the "
            "same intensity as your goals. You need a partner who matches your energy and independence."
        ),
    },
    "Heart": {
        "planet": "Venus / Mercury",
        "element": "Air",
        "personality": (
            "Your heart-shaped face reflects Venus and Mercury's charm. You are charismatic, "
            "intuitive, and highly expressive. Your mind works fast and your creativity is "
            "a natural gift."
        ),
        "career": (
            "Your charm and intellect open many doors. Ideal careers: Marketing, Acting, "
            "Fashion, Journalist, Public Speaker, Designer, or Influencer."
        ),
        "relationship": (
            "You are romantic and idealistic in love. You seek a deep soul connection and "
            "are highly perceptive of your partner's emotions. Passion and beauty matter greatly to you."
        ),
    },
}

FOREHEAD_DATA = {
    "Wide": {
        "meaning": "Wide forehead — Mercury's blessing: exceptional intelligence, quick thinking, and strong planning ability.",
        "trait": "Strategic thinker, problem-solver, mentally sharp.",
    },
    "Narrow": {
        "meaning": "Narrow forehead — Saturn's influence: practical, detail-focused, and action-oriented over theory.",
        "trait": "Hands-on, pragmatic, values experience over speculation.",
    },
    "Medium": {
        "meaning": "Balanced forehead — Jupiter's balance: blends analytical and creative thinking harmoniously.",
        "trait": "Well-rounded thinker with natural wisdom.",
    },
    "High": {
        "meaning": "High forehead — Uranus influence: highly imaginative, philosophical, ahead of their time.",
        "trait": "Visionary, inventor, deep thinker.",
    },
    "Low": {
        "meaning": "Low forehead — Mars influence: instinctive, quick to act, highly energetic.",
        "trait": "Doer, athlete, energetic go-getter.",
    },
}

EYE_DATA = {
    "Wide-set": {
        "planet": "Jupiter",
        "meaning": "Wide-set eyes: open-minded, adventurous, and sees the big picture. Blessed by Jupiter.",
        "trait": "Broad perspective, tolerant, explorer.",
    },
    "Close-set": {
        "planet": "Mercury",
        "meaning": "Close-set eyes: intense focus, detail-oriented, and highly analytical. Mercury's precision.",
        "trait": "Perfectionist, concentrated, sharp-minded.",
    },
    "Normal": {
        "planet": "Sun",
        "meaning": "Balanced eye spacing: harmonious outlook, grounded, and socially adaptable.",
        "trait": "Balanced, clear-eyed, socially intelligent.",
    },
}

NOSE_DATA = {
    "Large": {
        "planet": "Jupiter",
        "meaning": "Large nose: entrepreneurial spirit, financial acumen, and generous nature. Jupiter's abundance.",
        "trait": "Business-minded, ambitious, generous.",
    },
    "Small": {
        "planet": "Mercury",
        "meaning": "Small nose: detail-loving, precise, and prefers intimacy over crowds.",
        "trait": "Private, meticulous, selective.",
    },
    "Medium": {
        "planet": "Venus",
        "meaning": "Medium nose: balanced ambition, sociable, and aesthetically inclined.",
        "trait": "Social, balanced drive, appreciates beauty.",
    },
}

LIP_DATA = {
    "Full": {
        "planet": "Venus",
        "meaning": "Full lips: sensual, generous, and highly expressive. Venus blesses with charm.",
        "trait": "Warm, communicative, pleasure-loving.",
    },
    "Thin": {
        "planet": "Saturn",
        "meaning": "Thin lips: disciplined speech, thoughtful, and values precision in communication.",
        "trait": "Reserved, precise, strategic communicator.",
    },
    "Medium": {
        "planet": "Mercury",
        "meaning": "Medium lips: balanced communicator — persuasive, articulate, and adaptable.",
        "trait": "Persuasive, adaptable, clear speaker.",
    },
}

JAWLINE_DATA = {
    "Strong": {
        "planet": "Mars",
        "meaning": "Strong jawline: powerful will, determination, and natural leadership. Mars energy.",
        "trait": "Leader, determined, physically strong.",
    },
    "Soft": {
        "planet": "Moon",
        "meaning": "Soft jawline: flexible, empathetic, and emotionally intelligent. Moon's grace.",
        "trait": "Adaptable, compassionate, intuitive.",
    },
    "Medium": {
        "planet": "Venus",
        "meaning": "Balanced jawline: blend of strength and sensitivity — diplomatic and effective.",
        "trait": "Diplomatic, balanced, socially effective.",
    },
}

EYEBROW_DATA = {
    "Thick": {
        "planet": "Mars / Sun",
        "meaning": "Thick eyebrows: strong personality, confidence, and decisive nature.",
        "trait": "Assertive, bold, natural authority.",
    },
    "Thin": {
        "planet": "Venus",
        "meaning": "Thin eyebrows: refined taste, sensitivity, and artistic temperament.",
        "trait": "Aesthetic, sensitive, refined.",
    },
    "Arched": {
        "planet": "Moon",
        "meaning": "Arched eyebrows: expressive, dramatic, and highly perceptive of others.",
        "trait": "Expressive, intuitive, emotionally aware.",
    },
    "Straight": {
        "planet": "Saturn",
        "meaning": "Straight eyebrows: logical, direct, and prefers facts over emotions.",
        "trait": "Analytical, straightforward, reliable.",
    },
    "Medium": {
        "planet": "Mercury",
        "meaning": "Balanced eyebrows: versatile thinking, clear communication, and mental agility.",
        "trait": "Communicative, versatile, mentally sharp.",
    },
}

SYMMETRY_DATA = {
    "High": {
        "meaning": "High facial symmetry: strong life force, natural charisma, and consistent energy.",
        "trait": "Magnetic, reliable, balanced vitality.",
    },
    "Medium": {
        "meaning": "Moderate symmetry: unique character with interesting contrasts — creative and original.",
        "trait": "Creative, distinctive, authentic.",
    },
    "Low": {
        "meaning": "Asymmetry present: rich inner life, complex personality, and deep emotional depth.",
        "trait": "Deeply complex, emotionally rich, introspective.",
    },
}


# ─────────────────────────────────────────────
#  FEATURE CLASSIFIERS
# ─────────────────────────────────────────────

def classify_face_shape(ratio, face_w, face_h, jaw_w=None):
    """Classify face shape using height/width ratio and optional jaw estimation."""
    if jaw_w is not None:
        jaw_ratio = jaw_w / face_w
        if jaw_ratio > 0.85 and ratio < 1.15:
            return "Square"
        if jaw_ratio < 0.65 and ratio < 1.1:
            return "Heart"
    if ratio >= 1.3:
        return "Long"
    if ratio <= 0.92:
        return "Round"
    if ratio <= 1.05:
        return "Square"
    return "Oval"


def classify_forehead(forehead_w, forehead_h, face_w, face_h):
    fw_ratio = forehead_w / face_w
    fh_ratio = forehead_h / face_h
    if fw_ratio >= 0.88:
        return "Wide"
    if fw_ratio <= 0.65:
        return "Narrow"
    if fh_ratio >= 0.28:
        return "High"
    if fh_ratio <= 0.18:
        return "Low"
    return "Medium"


def classify_eye_distance(left_eye, right_eye, face_w):
    if left_eye is None or right_eye is None:
        return "Normal"
    lx = left_eye[0] + left_eye[2] / 2
    rx = right_eye[0] + right_eye[2] / 2
    eye_gap = abs(rx - lx)
    ratio = eye_gap / face_w
    if ratio >= 0.45:
        return "Wide-set"
    if ratio <= 0.32:
        return "Close-set"
    return "Normal"


def classify_nose(nose_w, face_w, nose_h, face_h):
    wR = nose_w / face_w
    hR = nose_h / face_h
    if wR >= 0.3 or hR >= 0.32:
        return "Large"
    if wR <= 0.18 or hR <= 0.18:
        return "Small"
    return "Medium"


def classify_lips(lip_w, lip_h):
    if lip_h == 0:
        return "Medium"
    ratio = lip_h / lip_w
    if ratio >= 0.38:
        return "Full"
    if ratio <= 0.22:
        return "Thin"
    return "Medium"


def classify_jawline(face_w, face_h, bottom_face_w=None):
    if bottom_face_w is None:
        bottom_face_w = face_w
    ratio = bottom_face_w / face_w
    if ratio >= 0.82:
        return "Strong"
    if ratio <= 0.62:
        return "Soft"
    return "Medium"


def classify_eyebrows(brow_h, face_h):
    ratio = brow_h / face_h
    if ratio >= 0.055:
        return "Thick"
    if ratio <= 0.025:
        return "Thin"
    return "Medium"


def compute_symmetry(img, x, y, w, h):
    """Estimate facial symmetry by comparing left/right halves."""
    face_roi = img[y:y+h, x:x+w]
    gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    mid = w // 2
    left_half = gray_face[:, :mid]
    right_half = cv2.flip(gray_face[:, mid:mid*2], 1)
    if left_half.shape != right_half.shape:
        min_w = min(left_half.shape[1], right_half.shape[1])
        left_half = left_half[:, :min_w]
        right_half = right_half[:, :min_w]
    diff = cv2.absdiff(left_half, right_half)
    score = 100 - (np.mean(diff) / 128 * 100)
    if score >= 72:
        return "High", round(score, 1)
    if score >= 50:
        return "Medium", round(score, 1)
    return "Low", round(score, 1)


# ─────────────────────────────────────────────
#  CONFIDENCE ESTIMATOR
# ─────────────────────────────────────────────

def estimate_confidence(ratio: float) -> int:
    deviation = abs(ratio - 1.1)
    base = 78.0
    bonus = max(0.0, (0.5 - deviation) * 30.0)
    return int(min(97, round(base + bonus)))


# ─────────────────────────────────────────────
#  MAIN ANALYSIS ENGINE
# ─────────────────────────────────────────────

def analyze_face(image_input) -> dict:
    """
    Full astrological face reading.

    Returns a dict with face classifications and predictions.
    """
    # Handle both bytes and file path for testing
    if isinstance(image_input, dict) and 'file_path' in image_input:
        # For testing with file path
        with open(image_input['file_path'], 'rb') as f:
            image_bytes = f.read()
    else:
        image_bytes = image_input
    
    # ── Decode image ──────────────────────────────────────────────
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image — could not decode.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # ── Load cascades ─────────────────────────────────────────────
    base = cv2.data.haarcascades
    
    # Primary face detector
    face_cascade = cv2.CascadeClassifier(base + "haarcascade_frontalface_default.xml")
    if face_cascade.empty():
        # backup path
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml")
        
    if face_cascade.empty():
        raise RuntimeError("Could not load any face cascade classifier. Check opencv-python installation.")
    
    # Feature detectors
    eye_cascade = cv2.CascadeClassifier(base + "haarcascade_eye.xml")
    nose_cascade = cv2.CascadeClassifier(base + "haarcascade_frontalface_alt.xml")
    mouth_cascade = cv2.CascadeClassifier(base + "haarcascade_smile.xml")

    # ── Detect face ───────────────────────────────────────────────
    # Try different parameters if first pass fails
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))
    if len(faces) == 0:
        # try more sensitive settings
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(60, 60))
        
    if len(faces) == 0:
        raise ValueError("No face detected. Please ensure you are in a well-lit area and facing the camera directly.")

    # Use the largest face detected
    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
    x, y, w, h = faces[0]
    
    # ── Confidence Adjustment ──────────────────────────────────────
    # Low-light or blur check could go here
    
    ratio = h / w

    face_roi_gray = gray[y:y+h, x:x+w]
    face_roi_color = img[y:y+h, x:x+w]

    # ── Face shape ────────────────────────────────────────────────
    face_shape = classify_face_shape(ratio, w, h)

    # ── Forehead (top 30% of face) ────────────────────────────────
    forehead_h = int(h * 0.30)
    forehead_region = face_roi_gray[:forehead_h, :]
    forehead_w = w  # approximate; cascade detects full width
    forehead_type = classify_forehead(forehead_w, forehead_h, w, h)

    # ── Eyes ──────────────────────────────────────────────────────
    eye_region = face_roi_gray[:int(h * 0.55), :]
    eye_distance_type = "Normal"
    if not eye_cascade.empty():
        eyes = eye_cascade.detectMultiScale(eye_region, 1.1, 5)
        left_eye = right_eye = None
        if len(eyes) >= 2:
            eyes = sorted(eyes, key=lambda e: e[0])
            left_eye, right_eye = eyes[0], eyes[-1]
            eye_distance_type = classify_eye_distance(left_eye, right_eye, w)

    # ── Eyebrows (top 20-35% region) ─────────────────────────────
    brow_region = face_roi_gray[int(h*0.18):int(h*0.35), :]
    # Estimate brow thickness via edge density
    edges = cv2.Canny(brow_region, 50, 150)
    brow_density = np.sum(edges > 0) / (edges.size + 1e-6)
    brow_h_est = brow_density * h * 5  # scale to face height units
    eyebrow_type = classify_eyebrows(brow_h_est, h)

    # ── Nose ──────────────────────────────────────────────────────
    nose_region = face_roi_gray[int(h*0.35):int(h*0.70), :]
    nose_type = "Medium"
    if not nose_cascade.empty():
        noses = nose_cascade.detectMultiScale(nose_region, 1.1, 4)
        if len(noses) > 0:
            nx, ny, nw, nh = noses[0]
            nose_type = classify_nose(nw, w, nh, h)

    # ── Lips ─────────────────────────────────────────────────────
    mouth_region = face_roi_gray[int(h*0.60):, :]
    lip_type = "Medium"
    if not mouth_cascade.empty():
        mouths = mouth_cascade.detectMultiScale(mouth_region, 1.7, 11)
        if len(mouths) > 0:
            mx, my, mw, mh = mouths[0]
            lip_type = classify_lips(mw, mh)

    # ── Jawline ───────────────────────────────────────────────────
    jawline_type = classify_jawline(w, h)

    # ── Symmetry ─────────────────────────────────────────────────
    symmetry_level, symmetry_score = compute_symmetry(img, x, y, w, h)

    # ── Confidence ────────────────────────────────────────────────
    confidence = estimate_confidence(ratio)

    # ── Pull predictions ──────────────────────────────────────────
    shape_data    = FACE_SHAPE_DATA.get(face_shape, FACE_SHAPE_DATA["Oval"])
    forehead_data = FOREHEAD_DATA.get(forehead_type, FOREHEAD_DATA["Medium"])
    eye_data      = EYE_DATA.get(eye_distance_type, EYE_DATA["Normal"])
    nose_data     = NOSE_DATA.get(nose_type, NOSE_DATA["Medium"])
    lip_data      = LIP_DATA.get(lip_type, LIP_DATA["Medium"])
    jaw_data      = JAWLINE_DATA.get(jawline_type, JAWLINE_DATA["Medium"])
    brow_data     = EYEBROW_DATA.get(eyebrow_type, EYEBROW_DATA["Medium"])
    sym_data      = SYMMETRY_DATA.get(symmetry_level, SYMMETRY_DATA["Medium"])

    # ── Build 3-level prediction ──────────────────────────────────
    personality = (
        f"🪐 Primary Influence — {shape_data['planet']} ({face_shape} face): "
        f"{shape_data['personality']} "
        f"Your {forehead_type.lower()} forehead adds: {forehead_data['trait']}. "
        f"Eye spacing ({eye_distance_type}) reveals: {eye_data['trait']}. "
        f"Facial symmetry is {symmetry_level.lower()} ({symmetry_score}%) — {sym_data['trait']}."
    )

    career = (
        f"💼 {shape_data['career']} "
        f"Your {nose_type.lower()} nose ({nose_data['planet']}) supports: {nose_data['trait']}. "
        f"Combined with your {jawline_type.lower()} jawline ({jaw_data['planet']}): {jaw_data['trait']}."
    )

    relationship = (
        f"❤️ {shape_data['relationship']} "
        f"Your {lip_type.lower()} lips ({lip_data['planet']}) show: {lip_data['trait']}. "
        f"Eyebrows ({eyebrow_type}, {brow_data['planet']}): {brow_data['trait']}."
    )

    # ── Dominant planet count ─────────────────────────────────────
    planets = [
        shape_data["planet"],
        eye_data["planet"],
        nose_data["planet"],
        lip_data["planet"],
        jaw_data["planet"],
        brow_data["planet"],
    ]
    from collections import Counter
    dominant_planet = Counter(planets).most_common(1)[0][0]

    return {
        # Raw classifications
        "face_shape":      face_shape,
        "forehead":        forehead_type,
        "eye_distance":    eye_distance_type,
        "eyebrows":        eyebrow_type,
        "nose":            nose_type,
        "lips":            lip_type,
        "jawline":         jawline_type,
        "symmetry":        symmetry_level,
        "symmetry_score":  symmetry_score,
        "confidence":      confidence,

        # 3-level predictions
        "personality_analysis": personality,
        "career_prediction":    career,
        "relationship_traits":  relationship,

        # Per-feature detailed astrological readings
        "detailed_readings": {
            "face_shape":  {"type": face_shape,        **shape_data},
            "forehead":    {"type": forehead_type,     **forehead_data},
            "eyes":        {"type": eye_distance_type, **eye_data},
            "eyebrows":    {"type": eyebrow_type,      **brow_data},
            "nose":        {"type": nose_type,         **nose_data},
            "lips":        {"type": lip_type,          **lip_data},
            "jawline":     {"type": jawline_type,      **jaw_data},
            "symmetry":    {"type": symmetry_level,    **sym_data},
        },

        # Summary
        "planet_summary": (
            f"Your dominant planetary energy is {dominant_planet}. "
            f"Face shape ruled by {shape_data['planet']} ({shape_data['element']} element)."
        ),
    }


# ─────────────────────────────────────────────
#  QUICK TEST  (run: python face_reading.py)
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys, json, pprint

    if len(sys.argv) < 2:
        print("Usage: python face_reading.py <image_path>")
        sys.exit(1)

    with open(sys.argv[1], "rb") as f:
        result = analyze_face(f.read())

    print("\n" + "="*60)
    print("  🔮  ASTROLOGICAL FACE READING REPORT")
    print("="*60)
    print(f"\n✦ Face Shape    : {result['face_shape']}")
    print(f"✦ Forehead      : {result['forehead']}")
    print(f"✦ Eye Distance  : {result['eye_distance']}")
    print(f"✦ Eyebrows      : {result['eyebrows']}")
    print(f"✦ Nose          : {result['nose']}")
    print(f"✦ Lips          : {result['lips']}")
    print(f"✦ Jawline       : {result['jawline']}")
    print(f"✦ Symmetry      : {result['symmetry']} ({result['symmetry_score']}%)")
    print(f"✦ Confidence    : {result['confidence']}%")
    print(f"\n🪐 Planet Summary:\n   {result['planet_summary']}")
    print(f"\n{'─'*60}")
    print(f"\n🧠 LEVEL 1 — PERSONALITY ANALYSIS\n{result['personality_analysis']}")
    print(f"\n{'─'*60}")
    print(f"\n💼 LEVEL 2 — CAREER PREDICTION\n{result['career_prediction']}")
    print(f"\n{'─'*60}")
    print(f"\n❤️  LEVEL 3 — RELATIONSHIP TRAITS\n{result['relationship_traits']}")
    print(f"\n{'─'*60}")
    print("\n📖 DETAILED FEATURE READINGS:")
    for feature, data in result["detailed_readings"].items():
        print(f"\n  [{feature.upper()}] — {data['type']}")
        meaning = data.get("meaning", "")
        if meaning:
            print(f"  {meaning}")