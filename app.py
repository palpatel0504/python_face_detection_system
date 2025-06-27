import io
import base64
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    send_file
)
import pandas as pd
import json
import cv2
import datetime
import numpy as np
from pathlib import Path
from train_model import train_model
from recognition_utils import recognize_faces_from_image


# Initialize Flask app
app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"

# File paths
USERS_FILE  = "users.xlsx"
MODEL_FILE  = "trainer.yml"
LABELS_FILE = "labels.json"
ATT_FILE    = "attendance.xlsx"
CONF_THRESHOLD = 60  # adjust looser (higher) or stricter (lower)
CASCADE_FILE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Load LBPH recognizer and labels
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_FILE)
with open(LABELS_FILE, 'r') as f:
    labels = json.load(f)

detector = cv2.CascadeClassifier(CASCADE_FILE)

# Load users dataframe
users_df = pd.read_excel(USERS_FILE)

# Initialize or load attendance dataframe
def get_attendance_df():
    try:
        return pd.read_excel(ATT_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Date", "Time"])

att_df = get_attendance_df()

# Login route
def validate_user(u, p):
    try:
        df = pd.read_excel(USERS_FILE)
    except FileNotFoundError:
        return False
    return not df[(df.username == u) & (df.password == p)].empty

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username'].strip()
        p = request.form['password'].strip()
        if validate_user(u, p):
            session['user'] = u
            return redirect(url_for('attendance'))
    return render_template('login.html')

# Attendance (camera) page
@app.route('/attendance')
def attendance():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('attendance.html')

# Face recognition endpoint
@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.json.get("image", "")
    if not data:
        return jsonify({"names": []})

    img_bytes = base64.b64decode(data.split(",")[1])
    np_img = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    global att_df
    names, att_df = recognize_faces_from_image(frame, att_df)
    return jsonify({"names": names})

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard: display attendance log
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    df = get_attendance_df()
    records = df.to_dict(orient='records')
    return render_template('dashboard.html', records=records)

@app.route('/retrain', methods=['POST'])
def retrain():
    success = train_model()
    if success:
        recognizer.read(MODEL_FILE)  # Reload in-memory recognizer
        with open(LABELS_FILE, 'r') as f:
            global labels
            labels = json.load(f)
        return jsonify({"message": "Model retrained."})
    return jsonify({"error": "Training failed"}), 500

@app.route('/register_face', methods=['POST'])
def register_face():
    data = request.json
    name = data.get("name")
    image_b64 = data.get("image")
    if not name or not image_b64:
        return jsonify({"error": "Missing name or image"}), 400

    # Decode and save image
    folder = Path("known_faces") / name
    folder.mkdir(parents=True, exist_ok=True)

    img_data = base64.b64decode(image_b64.split(",")[1])
    img_path = folder / f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    with open(img_path, "wb") as f:
        f.write(img_data)

    return jsonify({"message": "Face saved. Retraining model..."}), 200

# Download CSV of attendance log
@app.route('/download_csv')
def download_csv():
    if 'user' not in session:
        return redirect(url_for('login'))
    df = get_attendance_df()
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return send_file(
        io.BytesIO(buf.read().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='recognition_log.csv'
    )

# User administration: add/delete users
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user' not in session:
        return redirect(url_for('login'))
    df = pd.read_excel(USERS_FILE)
    # Add a new user
    if request.method == 'POST' and request.form.get('action') == 'add':
        new_u = request.form['new_username'].strip()
        new_p = request.form['new_password'].strip()
        if new_u and new_p and not (df.username == new_u).any():
            df.loc[len(df)] = {"username": new_u, "password": new_p}
            df.to_excel(USERS_FILE, index=False)
        return redirect(url_for('admin'))
    # Delete an existing user
    delete_user = request.args.get('delete')
    if delete_user:
        df = df[df.username != delete_user]
        df.to_excel(USERS_FILE, index=False)
        return redirect(url_for('admin'))
    users = df.to_dict(orient='records')
    return render_template('admin.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
