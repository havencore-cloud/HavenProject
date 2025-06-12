import sqlite3

conn = sqlite3.connect("ember_trust_cache.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scan_cache (
    mint TEXT PRIMARY KEY,
    data_json TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
