import sqlite3

conn = sqlite3.connect("database/patients.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(patients)")
columns = cursor.fetchall()

print("Columns in patients table:")
for col in columns:
    print(col)

conn.close()
input("Press Enter to exit...")
