import json
import os

# --- Project Config (projects.json) ---

def load_projects(config_path='config/projects.json'):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Project config not found at: {config_path}")
    with open(config_path, 'r') as file:
        return json.load(file)

def save_projects(projects, config_path='config/projects.json'):
    with open(config_path, 'w') as file:
        json.dump(projects, file, indent=2)


# --- Analytics Data (analytics.json) ---

def load_analytics(path='analytics/analytics.json'):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as file:
        return json.load(file)

def save_analytics(data, path='analytics/analytics.json'):
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)
