import sqlite3
import json
from datetime import datetime, timedelta

DB_PATH = "ember_trust_cache.db"

def get_cached_report(mint: str, max_age_minutes=2):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT data_json, timestamp FROM scan_cache WHERE mint = ?", (mint,))
        row = cursor.fetchone()
        conn.close()

        if row:
            data_json, timestamp = row
            ts = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            if datetime.utcnow() - ts < timedelta(minutes=max_age_minutes):
                return json.loads(data_json)
    except Exception as e:
        print(f"[CACHE ERROR] {e}")
    return None

def save_report(mint: str, report: dict):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "REPLACE INTO scan_cache (mint, data_json, timestamp) VALUES (?, ?, ?)",
            (mint, json.dumps(report), datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[CACHE ERROR] Failed to save report: {e}")
