"""
Initialize Compliance Department database schema
"""

import sqlite3
from pathlib import Path

db_path = Path("sentinel.db")
schema_path = Path("Departments/Compliance/database_schema.sql")

print("Initializing Compliance Department database schema...")
print(f"Database: {db_path}")
print(f"Schema: {schema_path}")
print()

# Read schema
with open(schema_path, 'r') as f:
    schema_sql = f.read()

# Execute schema
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.executescript(schema_sql)
conn.commit()
conn.close()

print("Database schema initialized successfully!")
print()

# Verify tables
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table' AND name LIKE 'compliance_%'
    ORDER BY name
""")

tables = cursor.fetchall()
conn.close()

print("Compliance tables created:")
for table in tables:
    print(f"  - {table[0]}")
print()
print("Ready for testing!")
