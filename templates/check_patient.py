import sqlite3

DB_PATH = "D:/IDT/database/patients.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

qr_id = "vikram_20061226"
cursor.execute("SELECT name, dob, blood_group, conditions, allergies, image_path FROM patients WHERE qr_id = ?", (qr_id,))
row = cursor.fetchone()

conn.close()

if row:
    print("Patient found:", row)
else:
    print("No patient found with qr_id:", qr_id)
