import sqlite3
import qrcode
import os
import shutil

# Define folders for QR codes and images
QR_FOLDER = "static/qr_codes"
IMAGE_FOLDER = "static/patient_images"

os.makedirs(QR_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Make sure database folder exists
os.makedirs("database", exist_ok=True)

# Database path
DB_PATH = "D:/IDT/database/patients.db"

# Connect to DB
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create patients table with image_path column
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dob TEXT,
    blood_group TEXT,
    conditions TEXT,
    allergies TEXT,
    qr_id TEXT UNIQUE,
    image_path TEXT
)
""")
conn.commit()

def add_patient(name, dob, blood_group, conditions, allergies, image_file_path=None):
    qr_id = f"{name.lower().replace(' ', '')}_{dob.replace('-', '')}"

    # Save the image if provided
    saved_image_path = None
    if image_file_path:
        ext = os.path.splitext(image_file_path)[1]
        saved_image_path = f"{IMAGE_FOLDER}/{qr_id}{ext}"
        shutil.copy(image_file_path, saved_image_path)

    try:
        cursor.execute("""
            INSERT INTO patients (name, dob, blood_group, conditions, allergies, qr_id, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (name, dob, blood_group, conditions, allergies, qr_id, saved_image_path))
        conn.commit()

        # Change here: set your server IP or localhost if testing on the same PC
        server_ip = "172.20.8.223"  # <-- Replace with your computer's local IP address or "localhost"

        qr_url = f"http://{server_ip}:5000/patient?qr_id={qr_id}"

        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        pc_ip = " 172.20.8.223"  # replace with your actual IP from Step 2
        qr_url = f"http://{pc_ip}:5000/patient?qr_id={qr_id}"
        qr.add_data(qr_url)

        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"{QR_FOLDER}/{qr_id}.png")

        print(f"✅ QR saved at {QR_FOLDER}/{qr_id}.png")
        if saved_image_path:
            print(f"🖼️ Image saved at {saved_image_path}")

    except sqlite3.IntegrityError:
        print(f"⚠️ Patient with QR ID '{qr_id}' already exists. Skipping insert.")

def get_patient_input():
    print("Enter patient details:")
    name = input("Name: ")
    dob = input("DOB (YYYY-MM-DD): ")
    blood_group = input("Blood Group: ")
    conditions = input("Medical Conditions: ")
    allergies = input("Allergies: ")
    image_path = input("Image file path (leave blank if none): ").strip()
    if image_path == "":
        image_path = None
    return name, dob, blood_group, conditions, allergies, image_path

def regenerate_qr(qr_id):
    qr = qrcode.make(qr_id)
    path = f"{QR_FOLDER}/{qr_id}.png"
    qr.save(path)
    print(f"✅ QR regenerated at {path}")

if __name__ == "__main__":
    # Uncomment below to add example patient without input
    # add_patient("pranesh", "1990-01-01", "O+", "Cancer", "None")

    # Or get input from user
    name, dob, blood_group, conditions, allergies, image_path = get_patient_input()
    add_patient(name, dob, blood_group, conditions, allergies, image_path)

    conn.close()
