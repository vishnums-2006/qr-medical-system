import sqlite3

conn = sqlite3.connect("database/patients.db")  # Make sure this path is correct
cursor = conn.cursor()

# Add new column to existing table
try:
    cursor.execute("ALTER TABLE patients ADD COLUMN image_path TEXT")
    print("✅ Column 'image_path' added to patients table.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Error: {e}")

conn.commit()
conn.close()
