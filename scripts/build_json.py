import os
import json


def load_raw_schools():
    with open("data/raw/schools_raw.json") as f:
        return json.load(f)


def load_raw_recruits():
    all_recruits = []
    for year in range(2015, 2025):
        path = f"data/raw/recruits_{year}.json"
        if not os.path.exists(path):
            print(f"Warning: {path} not found, skipping")
            continue
        with open(path) as f:
            all_recruits.extend(json.load(f))
    return all_recruits


def build_schools_json(raw_teams):
    schools = []
    for t in raw_teams:
        school_name = t.get("school")
        if not school_name:
            continue
        loc = t.get("location") or {}
        lat = loc.get("latitude")
        lng = loc.get("longitude")
        if lat is None or lng is None:
            print(f"Warning: no location for {school_name}, skipping")
            continue
        schools.append({
            "id": school_name,
            "name": school_name,
            "abbreviation": t.get("abbreviation", ""),
            "conference": t.get("conference", ""),
            "lat": lat,
            "lng": lng,
        })
    return schools


def build_recruits_json(raw_recruits, valid_school_ids):
    recruits = []
    stats = {"no_coords": 0, "no_school": 0, "international": 0}

    for r in raw_recruits:
        country = (r.get("country") or "USA").upper()
        if country not in ("USA", "US", ""):
            stats["international"] += 1
            continue

        committed_to = r.get("committedTo")
        if not committed_to or committed_to not in valid_school_ids:
            stats["no_school"] += 1
            continue

        hw = r.get("hometownInfo") or {}
        lat = hw.get("latitude")
        lng = hw.get("longitude")
        if not lat or not lng or lat == 0 or lng == 0:
            stats["no_coords"] += 1
            continue

        recruits.append({
            "name": r.get("name", ""),
            "school_id": committed_to,
            "position": r.get("position", ""),
            "stars": r.get("stars") or 0,
            "rating": round(r.get("rating") or 0, 4),
            "year": r.get("year"),
            "hometown_city": r.get("city", ""),
            "hometown_state": r.get("stateProvince", ""),
            "lat": lat,
            "lng": lng,
        })

    print(f"Built {len(recruits)} recruits")
    print(f"  Dropped {stats['no_coords']} (no hometown coordinates)")
    print(f"  Dropped {stats['no_school']} (uncommitted or unknown school)")
    print(f"  Dropped {stats['international']} (international)")
    return recruits


if __name__ == "__main__":
    raw_teams = load_raw_schools()
    raw_recruits = load_raw_recruits()

    schools = build_schools_json(raw_teams)
    valid_school_ids = {s["id"] for s in schools}
    recruits = build_recruits_json(raw_recruits, valid_school_ids)

    os.makedirs("public", exist_ok=True)
    with open("public/schools.json", "w") as f:
        json.dump(schools, f, separators=(",", ":"))
    with open("public/recruits.json", "w") as f:
        json.dump(recruits, f, separators=(",", ":"))

    print(f"\nWrote {len(schools)} schools → public/schools.json")
    print(f"Wrote {len(recruits)} recruits → public/recruits.json")
