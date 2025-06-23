# backend/report_cache.py

import os
import json

CACHE_DIR = "trust_reports"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cached_report(mint: str):
    path = os.path.join(CACHE_DIR, f"{mint}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_report(mint: str, report: dict):
    path = os.path.join(CACHE_DIR, f"{mint}.json")
    try:
        with open(path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"[CACHE] Saved report to: {path}")
    except Exception as e:
        print(f"[ERROR] Failed to write report: {e}")

