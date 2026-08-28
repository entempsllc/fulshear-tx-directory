from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

RECORDS = (
    {
        "name": "Amada Senior Care – Fulshear",
        "url": "https://www.amadaseniorcare.com/houston-senior-care-central/fulshear-home-care/",
        "phone": "tel:2816525492",
        "service": "Non-medical in-home care",
    },
    {
        "name": "Homewatch CareGivers of Katy – Fulshear",
        "url": "https://www.homewatchcaregivers.com/katy/fulshear/",
        "phone": "tel:8329521495",
        "service": "In-home care",
    },
    {
        "name": "Simplicity Bath & Shower",
        "url": "https://simplicitybath.com/service-areas/fulshear-tx/walk-in-bathtubs/",
        "phone": "tel:8323045911",
        "service": "Walk-in tubs & grab bars",
    },
    {
        "name": "Caroline OnTheGo Fulshear Notary Services",
        "url": "https://carolineonthegofulshearnotary.com/",
        "phone": "tel:3463804031",
        "service": "Mobile notary",
    },
    {
        "name": "Lee's Mobile and Online Notary",
        "url": "https://leenotarypublic.com/mobile-notary-fulshear/",
        "phone": "tel:8327413190",
        "service": "Mobile notary",
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


class SeniorSupportExpansionContract(unittest.TestCase):
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
