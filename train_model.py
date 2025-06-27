def train_model():
    import cv2, json, numpy as np
    from pathlib import Path

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces, labels, names = [], [], {}
    label_id = 0

    for person_dir in sorted(Path("known_faces").iterdir()):
        if not person_dir.is_dir() or person_dir.name.startswith('.'):
            continue
        names[label_id] = person_dir.name

        for img_path in person_dir.glob("*.*"):
            img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
            if img is None:
                print(f"⚠️ Couldn't read image: {img_path}")
                continue

            rects = detector.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in rects:
                face = img[y:y+h, x:x+w]

                # Normalize size and contrast
                face = cv2.resize(face, (200, 200))
                face = cv2.equalizeHist(face)

                # Append original
                faces.append(face)
                labels.append(label_id)

                # Data Augmentation: flipped face
                face_flipped = cv2.flip(face, 1)
                faces.append(face_flipped)
                labels.append(label_id)

        label_id += 1

    if not faces:
        print("❌ No faces found. Training aborted.")
        return False

    recognizer.train(faces, np.array(labels, dtype=np.int32))
    recognizer.write("trainer.yml")
    with open("labels.json", "w") as f:
        json.dump(names, f)

    print(f"✅ Model trained on {len(faces)} faces across {len(names)} individuals.")
    return True
