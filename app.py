import os
from flask import Flask, request, render_template
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(__file__), 'patient.db')


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/patient')
def patient_info():
    qr_id = request.args.get('qr_id')
    if not qr_id:
        return "⚠️ QR ID not provided", 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, dob, blood_group, conditions, allergies, image_path FROM patient WHERE qr_id = ?", (qr_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return "❌ Patient not found", 404

    name, dob, blood_group, conditions, allergies, image_path = row
    print("Patient data fetched:", name, dob, blood_group, conditions, allergies, image_path)
    return render_template('patient.html',
                           qr_id=qr_id,
                           name=name,
                           dob=dob,
                           blood_group=blood_group,
                           conditions=conditions,
                           allergies=allergies,
                           image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")


