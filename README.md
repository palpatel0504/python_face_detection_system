# 🧠 Face Recognition Based Attendance System

This is an AI-powered attendance system that uses **live face recognition** to mark attendance. Built with Python and Flask, it uses OpenCV to detect faces in real time and logs attendance into an Excel file. Users must log in, and recognized individuals are auto-logged with date and time.

---

## 🚀 Features

- 🔐 User login with session authentication
- 📷 Live face detection via webcam
- 📝 Real-time attendance logging in `attendance.xlsx`
- 📁 Model training from custom images
- 👤 Admin panel for user management
- 📊 Dashboard to view logs and download attendance
- 📦 Fully local – works offline

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Python (Flask)
- **AI/ML**: OpenCV (`cv2.face` from `opencv-contrib-python`)
- **Database**: `.xlsx` files (`users.xlsx`, `attendance.xlsx`)
- **Other**: pandas, numpy, openpyxl

---

## 📁 Folder Structure

```
face_recognition_shreya/
│
├── app.py                    # Main Flask application
├── face_recog.py             # Webcam face recognition script
├── gui_login.py              # GUI-based login (optional)
├── recognition_utils.py      # Core face recognition utilities
├── train_model.py            # Model trainer script
├── trainer.yml               # Saved face model
├── labels.json               # JSON label mappings
│
├── attendance.xlsx           # Attendance log
├── users.xlsx                # User list with credentials
│
├── known_faces/              # Upload user face images here
│   └── <username>/           # Create folder with user's name & add their photos
│
├── static/
│   ├── css/style.css         # Styling
│   └── js/attendance.js      # Optional JS
│
├── templates/                # HTML templates
│   ├── login.html
│   ├── base.html
│   ├── dashboard.html
│   ├── attendance.html
│   └── admin.html
```

---

## 🧑‍🏫 How to Use

### 1. 📦 Clone the Repository
```bash
git clone https://github.com/your-username/face_recognition_pal.git
cd face_recognition_pal
```

### 2. 🐍 Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate    # On macOS/Linux
venv\Scripts\activate       # On Windows
```

### 3. 🔧 Install Required Libraries
```bash
pip install opencv-contrib-python flask numpy pandas openpyxl
```

### 4. 📸 Upload Your Face Images
Create a new folder inside `known_faces/` with your name and upload 5–10 clear images of your face.

Example:
```
known_faces/pal/
    - img1.jpg
    - img2.jpg
    - ...
```

### 5. 🧠 Train the Model
Once images are uploaded, use the web interface’s **“Register & Retrain”** button to train the face recognizer.

### 6. 🚀 Run the Flask App
```bash
python app.py
```

Then open your browser and go to:
```
http://127.0.0.1:5000
```

Login using any registered user from `users.xlsx`.

---

## 🧠 How It Works

- Opens webcam and detects face
- If face not recognized: asks to register
- If recognized: marks attendance with date and time
- All logs are stored in `attendance.xlsx`
- Admin can manage users and view/download logs

---

## 📬 Contributions

Feel free to fork, contribute, and improve! PRs are welcome.

---

## 📸 Screenshots

📁 `known_faces` ➝  
Upload your images like this:  
```
known_faces/pal_patel/img1.jpg
known_faces/pal_patel/img2.jpg
```

✅ Successful Recognition ➝  
`"Recognized: pal_patel"`  
📝 Logs: `attendance.xlsx`

---

## 🧾 License

This project is open-source for educational purposes.

---

## 🤝 Author

**Pal Rakesh Patel**  
Computer Engineering, SVIT Vasad  
