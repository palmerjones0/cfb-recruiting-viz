import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.collegefootballdata.com"
OUT_PATH = "data/raw/schools_raw.json"

_api_key = os.environ.get("CFBD_API_KEY")
if not _api_key:
    raise ValueError("CFBD_API_KEY environment variable not set — copy .env.example to .env and add your key")
HEADERS = {"Authorization": f"Bearer {_api_key}"}


def fetch_fbs_teams():
    resp = requests.get(f"{BASE_URL}/teams/fbs", headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    teams = fetch_fbs_teams()
    if not teams:
        print("Warning: API returned empty team list")
    with open(OUT_PATH, "w") as f:
        json.dump(teams, f, indent=2)
    print(f"Fetched {len(teams)} FBS teams → {OUT_PATH}")
