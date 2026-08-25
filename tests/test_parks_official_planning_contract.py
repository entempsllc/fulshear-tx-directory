from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PARKS_PAGE = ROOT / "blog" / "fulshear-parks.html"
OFFICIAL_BASE = "https://www.fulsheartexas.gov/about-us/departments-h-z"


class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs))

    def handle_data(self, data):
        self.text.append(data)


class ParksOfficialPlanningContract(unittest.TestCase):
    def setUp(self):
        self.source = PARKS_PAGE.read_text(encoding="utf-8")
        self.parser = VisibleTextParser()
        self.parser.feed(self.source)
        self.visible = " ".join(" ".join(self.parser.text).split())
        self.hrefs = {link.get("href") for link in self.parser.links}

    def test_official_city_park_planning_section_is_visible(self):
        for phrase in (
            "Plan a Visit to a City-Managed Park",
            "Frances Smart Park",
            "Irene Stern Community Center",
            "Eagle Landing Park",
            "Primrose Park",
            "field and community-center rentals",
        ):
            self.assertIn(phrase, self.visible)

    def test_current_official_sources_are_linked(self):
        expected = {
            f"{OFFICIAL_BASE}/parks-and-recreation",
            f"{OFFICIAL_BASE}/parks-and-recreation/eagle-landing-park",
            f"{OFFICIAL_BASE}/parks-and-recreation/primrose-park",
            f"{OFFICIAL_BASE}/irene-stern-community-center",
            f"{OFFICIAL_BASE}/parks-and-recreation/parks-and-pathways-master-plan",
        }
        self.assertTrue(expected.issubset(self.hrefs), expected - self.hrefs)

    def test_source_note_and_status_check_are_present(self):
        self.assertIn("Source checked August 25, 2026", self.visible)
        self.assertIn("check the City pages before leaving", self.visible)


if __name__ == "__main__":
    unittest.main()
