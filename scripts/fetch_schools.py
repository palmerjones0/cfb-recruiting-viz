import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.collegefootballdata.com"
HEADERS = {"Authorization": f"Bearer {os.environ['CFBD_API_KEY']}"}
OUT_PATH = "data/raw/schools_raw.json"


def fetch_fbs_teams():
    resp = requests.get(f"{BASE_URL}/teams/fbs", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    teams = fetch_fbs_teams()
    with open(OUT_PATH, "w") as f:
        json.dump(teams, f, indent=2)
    print(f"Fetched {len(teams)} FBS teams → {OUT_PATH}")
