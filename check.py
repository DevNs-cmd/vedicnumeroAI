import cv2
import time
import random

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Predictions
personality = [
    "You are a natural leader",
    "You are creative and intelligent",
    "You are calm and emotionally strong",
    "You are adventurous and bold",
]

career = [
    "Entrepreneur",
    "Software Engineer",
    "Artist / Designer",
    "Business Leader",
]

strength = [
    "Strong communication skills",
    "Creative thinking",
    "High emotional intelligence",
    "Leadership ability",
]


def generate_prediction():
    return {
        "personality": random.choice(personality),
        "career": random.choice(career),
        "strength": random.choice(strength),
        "lucky_number": random.randint(1, 99)
    }


cap = cv2.VideoCapture(0)

start_time = time.time()
countdown = 5
captured = False
prediction = None

print("Camera Started")

while True:

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    elapsed = int(time.time() - start_time)

    # Countdown
    if elapsed < countdown:

        text = f"Scanning in {countdown-elapsed} seconds..."
        cv2.putText(frame, text, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,255,255), 2)

    else:

        if not captured:

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray,1.3,5)

            if len(faces) > 0:

                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

                cv2.putText(frame,"Face Detected", (50,50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,(0,255,0),2)

                time.sleep(2)

                cv2.putText(frame,"Analyzing Face...", (50,90),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,(255,255,0),2)

                cv2.imshow("Face Reading", frame)
                cv2.waitKey(2000)

                prediction = generate_prediction()
                captured = True

        else:

            # Show result
            cv2.putText(frame,"FACE READING RESULT", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,(0,255,255),2)

            cv2.putText(frame,f"Personality: {prediction['personality']}",
                        (50,120),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

            cv2.putText(frame,f"Strength: {prediction['strength']}",
                        (50,160),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

            cv2.putText(frame,f"Career: {prediction['career']}",
                        (50,200),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

            cv2.putText(frame,f"Lucky Number: {prediction['lucky_number']}",
                        (50,240),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    cv2.imshow("Face Reading System", frame)

    key = cv2.waitKey(1)

    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()