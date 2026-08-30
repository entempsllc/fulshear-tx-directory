from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

RECORDS = (
    {
        "name": "Visiting Angels East Bernard – Fulshear",
        "url": "https://www.visitingangels.com/east_bernard/home-care-fulshear",
        "phone": "tel:9793354025",
        "service": "In-home senior care",
    },
    {
        "name": "Right at Home Rosenberg – Fulshear",
        "url": "https://www.rightathome.net/rosenberg/about-us/city-served-fulshear-homecare",
        "phone": "tel:3462660333",
        "service": "In-home care for seniors & adults",
    },
    {
        "name": "Harbor Home Care – Fulshear",
        "url": "https://homecare-houston.com/home-care-in-fulshear/",
        "phone": "tel:7133602273",
        "service": "In-home care & skilled nursing",
    },
    {
        "name": "Fort Bend County Transit – Demand Response",
        "url": "https://www.fortbendcountytx.gov/government/departments/public-transportation/services/demand-response-service",
        "phone": "tel:8667518747",
        "service": "Scheduled shared-ride service",
    },
    {
        "name": "H-GAC Medicare Benefits Counseling",
        "url": "https://www.h-gac.com/area-agency-on-aging/medicare-benefits-counseling",
        "phone": "tel:18004377396",
        "service": "Free, unbiased Medicare counseling",
    },
)


class ListingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href"))

    def handle_data(self, data):
        self.text.append(data)


class SeniorPracticalSupportContract(unittest.TestCase):
    def test_five_first_party_records_are_present_once_on_both_surfaces(self):
        for filename in ("index.html", "listings.html"):
            source = (ROOT / filename).read_text(encoding="utf-8")
            parser = ListingParser()
            parser.feed(source)
            visible = " ".join(" ".join(parser.text).split())
            for record in RECORDS:
                with self.subTest(filename=filename, name=record["name"]):
                    self.assertEqual(visible.count(record["name"]), 1)
                    self.assertIn(record["service"], visible)
                    self.assertEqual(parser.links.count(record["url"]), 1)
                    self.assertEqual(parser.links.count(record["phone"]), 1)

    def test_new_records_make_no_rating_review_or_verification_claim(self):
        for filename in ("index.html", "listings.html"):
            source = unescape((ROOT / filename).read_text(encoding="utf-8"))
            for record in RECORDS:
                start = source.index(record["name"])
                end = source.find("</div>", start)
                fragment = source[start:end].lower()
                with self.subTest(filename=filename, name=record["name"]):
                    self.assertNotIn("stars", fragment)
                    self.assertNotIn("reviews", fragment)
                    self.assertNotIn("verified", fragment)


if __name__ == "__main__":
    unittest.main()
