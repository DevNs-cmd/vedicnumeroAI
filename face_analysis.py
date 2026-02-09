import cv2
import numpy as np

def vedic_face_reader(image_path):
    # 1. Load the detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # 2. Load and Prepare Image
    img = cv2.imread(image_path)
    if img is None:
        return "Error: Image not found. Check the filename."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces) == 0:
        return "No face detected. Try a clearer photo."

    for (x, y, w, h) in faces:
        # --- THE GEOMETRY ENGINE ---
        # Ratio > 1.2 means a long, narrow face (Saturn)
        # Ratio between 1.0 and 1.1 means a square/round face (Mars/Sun)
        face_height_ratio = h / w 
        
        # Calculate 'Skin Glow' (Brightness)
        face_roi = gray[y:y+h, x:x+w]
        brightness = np.mean(face_roi)

        # 3. THE PREDICTION LOGIC (Based on Samudrika Shastra)
        
        # SATURN (SHANI) - Priority 1: Structure
        # Saturn rules long, thin, and bony faces.
        if face_height_ratio > 1.22:
            prediction = {
                "Archetype": "The Disciplined Architect",
                "Planet": "Saturn (Shani)",
                "Nature": "Serious, Patient, and Hardworking",
                "Message": "Your long facial structure shows deep Shani influence. You are meant for great things, but success comes through discipline and after some struggle.",
                "Lucky_Day": "Saturday"
            }

        # MARS (MANGAL) - Priority 2: Width
        # Mars rules square, strong, and wide jawlines.
        elif w / h > 0.98:
            prediction = {
                "Archetype": "The Fearless Warrior",
                "Planet": "Mars (Mangal)",
                "Nature": "Energetic, Brave, and Straightforward",
                "Message": "A wide, strong face indicates high Mangal energy. You have the power to protect others and lead teams with courage.",
                "Lucky_Day": "Tuesday"
            }

        # VENUS (SHUKRA) - Priority 3: Radiance
        # Venus rules soft, glowing, and attractive faces.
        elif brightness > 165:
            prediction = {
                "Archetype": "The Creative Soul",
                "Planet": "Venus (Shukra)",
                "Nature": "Kind, Artistic, and Charming",
                "Message": "The glow on your face shows Shukra's blessing. You love beauty, comfort, and have a natural talent for the arts.",
                "Lucky_Day": "Friday"
            }

        # JUPITER (GURU) - Priority 4: Balance
        # Jupiter rules oval, balanced, and calm faces.
        else:
            prediction = {
                "Archetype": "The Wise Counselor",
                "Planet": "Jupiter (Guru)",
                "Nature": "Knowledgeable and Spiritual",
                "Message": "A balanced, oval face shows Guru energy. You are a seeker of truth and will gain respect through your wisdom.",
                "Lucky_Day": "Thursday"
            }

        # 4. DRAW RESULT ON IMAGE
        color = (255, 191, 63) # Golden Yellow
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 3)
        cv2.putText(img, f"Planet: {prediction['Planet']}", (x, y-15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Save and Output
    cv2.imwrite('prediction_result.jpg', img)
    return prediction
