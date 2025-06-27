import cv2
import numpy as np
import json
import datetime
from pathlib import Path
import pandas as pd

CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()
RECOGNIZER.read("trainer.yml")

with open("labels.json") as f:
    LABELS = json.load(f)

def recognize_faces_from_image(frame, att_df, threshold=60):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = CASCADE.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    names, now = [], datetime.datetime.now()
    date_str, time_str = now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]
        id_, conf = RECOGNIZER.predict(roi)
        name = LABELS.get(str(id_), "Unknown") if conf < threshold else "Unknown"
        names.append(name)

        if name != "Unknown" and not ((att_df.Name == name) & (att_df.Date == date_str)).any():
            att_df.loc[len(att_df)] = [name, date_str, time_str]
            att_df.to_excel("attendance.xlsx", index=False)

    return sorted(set(names)), att_df
