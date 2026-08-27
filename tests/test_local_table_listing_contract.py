from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_URL = "https://eatatlocaltable.com/locations/fulshear/"
NAME = "Local Table"
ADDRESS = "11525 S Fry Rd Ste 101, Fulshear, TX 77441"
PHONE_HREF = "tel:8324375317"


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


class LocalTableListingContract(unittest.TestCase):
    def test_first_party_listing_is_present_once_on_each_public_surface(self):
        for filename in ("index.html", "listings.html"):
            with self.subTest(filename=filename):
                source = (ROOT / filename).read_text(encoding="utf-8")
                parser = ListingParser()
                parser.feed(source)
                visible = " ".join(" ".join(parser.text).split())
                self.assertEqual(visible.count(NAME), 1)
                self.assertIn(ADDRESS, visible)
                self.assertEqual(parser.links.count(OFFICIAL_URL), 1)
                self.assertEqual(parser.links.count(PHONE_HREF), 1)

    def test_listing_does_not_add_rating_review_or_verification_claim(self):
        next_record = {
            "index.html": "Fulshear Flats Restaurant",
            "listings.html": "Texas Borders",
        }
        for filename, delimiter in next_record.items():
            source = (ROOT / filename).read_text(encoding="utf-8")
            start = source.index(NAME)
            end = source.index(delimiter, start)
            listing = source[start:end].lower()
            self.assertNotIn("stars", listing)
            self.assertNotIn("reviews", listing)
            self.assertNotIn("verified", listing)


if __name__ == "__main__":
    unittest.main()
