import cv2
import json
import pandas as pd
import datetime
import numpy as np
from pathlib import Path
from recognition_utils import recognize_faces_from_image

# Configuration
MODEL_PATH      = "trainer.yml"
LABELS_PATH     = "labels.json"
ATT_FILE        = "attendance.xlsx"
CASCADE_PATH    = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
CONF_THRESHOLD  = 60  # adjust looser (higher) or stricter (lower)

# Load the trained LBPH model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_PATH)

# Load label mappings
with open(LABELS_PATH, 'r') as f:
    labels = json.load(f)  # e.g. {"0":"pal","1":"riya","2":"yatri"}

# Initialize face detector
detector = cv2.CascadeClassifier(CASCADE_PATH)

# Load or create attendance DataFrame
def load_attendance():
    if Path(ATT_FILE).exists():
        return pd.read_excel(ATT_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Date", "Time"])

att_df = load_attendance()

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Could not open webcam")
print("📸 Camera started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    names, att_df = recognize_faces_from_image(frame, att_df)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    recognized = []

    # current timestamp
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    print(f"DEBUG → Detected {len(faces)} face(s)")

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        id_, conf = recognizer.predict(face_img)
        # decide label or Unknown based on confidence
        name = labels.get(str(id_), "Unknown") if conf < CONF_THRESHOLD else "Unknown"
        print(f"DEBUG → {name} (conf={conf:.1f})")
        recognized.append(name)

        # Log every name (including Unknown) once per day
        if name != "Unknown" and not ((att_df.Name == name) & (att_df.Date == date_str)).any():
            att_df.loc[len(att_df)] = [name, date_str, time_str]
            att_df.to_excel(ATT_FILE, index=False)
            print(f"✅ Logged {name} at {time_str}")

        # Draw box and label
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Display frame
    cv2.imshow("Recognition", frame)
    # Optional: print recognized list
    print("DEBUG → Returning names:", recognized)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
df_final = att_df  # data saved already
cap.release()
cv2.destroyAllWindows()
