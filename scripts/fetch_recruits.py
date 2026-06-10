import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.collegefootballdata.com"
YEARS = range(2015, 2029)

_api_key = os.environ.get("CFBD_API_KEY")
if not _api_key:
    raise ValueError("CFBD_API_KEY environment variable not set — copy .env.example to .env and add your key")
HEADERS = {"Authorization": f"Bearer {_api_key}"}


def fetch_recruits_for_year(year):
    resp = requests.get(
        f"{BASE_URL}/recruiting/players",
        params={"year": year},
        headers=HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    for year in YEARS:
        path = f"data/raw/recruits_{year}.json"
        if os.path.exists(path):
            print(f"{year}: already cached, skipping")
            continue
        recruits = fetch_recruits_for_year(year)
        with open(path, "w") as f:
            json.dump(recruits, f, indent=2)
        print(f"{year}: {len(recruits)} recruits")
        time.sleep(0.5)
