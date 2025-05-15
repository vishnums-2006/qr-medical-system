import sqlite3
import os

# Make sure the database folder exists
os.makedirs("database", exist_ok=True)

# Connect to the database
conn = sqlite3.connect("database/patients.db")
cursor = conn.cursor()

# Create the table with image_path included
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
conn.close()

print("✅ patients table created successfully with image_path column.")
