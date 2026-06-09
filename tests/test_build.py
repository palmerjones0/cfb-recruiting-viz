import unittest
from scripts.build_json import build_schools_json, build_recruits_json

SAMPLE_TEAMS = [
    {
        "school": "Alabama",
        "abbreviation": "UA",
        "conference": "SEC",
        "division": "West",
        "location": {"latitude": 33.208, "longitude": -87.550},
    }
]

SAMPLE_RECRUIT_BASE = {
    "name": "Test Player",
    "committedTo": "Alabama",
    "position": "QB",
    "stars": 5,
    "rating": 0.9956,
    "year": 2024,
    "city": "Nashville",
    "stateProvince": "TN",
    "country": "USA",
    "hometownInfo": {"latitude": 36.174, "longitude": -86.767},
}


class TestBuildSchools(unittest.TestCase):
    def test_basic_school_fields(self):
        schools = build_schools_json(SAMPLE_TEAMS)
        self.assertEqual(len(schools), 1)
        s = schools[0]
        self.assertEqual(s["id"], "Alabama")
        self.assertEqual(s["name"], "Alabama")
        self.assertEqual(s["conference"], "SEC")
        self.assertAlmostEqual(s["lat"], 33.208)
        self.assertAlmostEqual(s["lng"], -87.550)

    def test_school_missing_lat_dropped(self):
        teams = [{"school": "Nowhere", "location": {"longitude": -90.0}}]
        schools = build_schools_json(teams)
        self.assertEqual(len(schools), 0)

    def test_school_missing_location_dropped(self):
        teams = [{"school": "Ghost U", "location": {}}]
        schools = build_schools_json(teams)
        self.assertEqual(len(schools), 0)


class TestBuildRecruits(unittest.TestCase):
    def _run(self, overrides=None, school_ids=None):
        r = {**SAMPLE_RECRUIT_BASE, **(overrides or {})}
        ids = school_ids if school_ids is not None else {"Alabama"}
        return build_recruits_json([r], ids)

    def test_basic_recruit_fields(self):
        recruits = self._run()
        self.assertEqual(len(recruits), 1)
        r = recruits[0]
        self.assertEqual(r["name"], "Test Player")
        self.assertEqual(r["school_id"], "Alabama")
        self.assertEqual(r["position"], "QB")
        self.assertEqual(r["stars"], 5)
        self.assertEqual(r["year"], 2024)
        self.assertAlmostEqual(r["lat"], 36.174)
        self.assertAlmostEqual(r["lng"], -86.767)

    def test_international_dropped(self):
        self.assertEqual(len(self._run({"country": "Canada"})), 0)

    def test_no_hometown_info_dropped(self):
        self.assertEqual(len(self._run({"hometownInfo": None})), 0)

    def test_zero_coords_dropped(self):
        self.assertEqual(len(self._run({"hometownInfo": {"latitude": 0, "longitude": 0}})), 0)

    def test_unknown_school_dropped(self):
        self.assertEqual(len(self._run(school_ids={"NotAlabama"})), 0)

    def test_no_committed_to_dropped(self):
        self.assertEqual(len(self._run({"committedTo": None})), 0)

    def test_rating_rounded(self):
        recruits = self._run({"rating": 0.99563})
        self.assertEqual(recruits[0]["rating"], 0.9956)


if __name__ == "__main__":
    unittest.main()
