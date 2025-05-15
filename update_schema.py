import sqlite3

DB_PATH = "D:/IDT/database/patients.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE patients ADD COLUMN image_path TEXT")
    print("✅ Column 'image_path' added successfully.")
except sqlite3.OperationalError as e:
    print(f"⚠️ {e}")

conn.commit()
conn.close()
