from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "blog" / "fort-bend-senior-property-tax-exemptions.html"
BLOG_INDEX = ROOT / "blog" / "index.html"
HOME = ROOT / "index.html"
GUIDE_PATH = "/blog/fort-bend-senior-property-tax-exemptions.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.links = []
        self.title = []
        self.in_title = False
        self.h1_count = 0
        self.canonicals = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a":
            self.links.append(values.get("href"))
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "link" and values.get("rel") == "canonical":
            self.canonicals.append(values.get("href"))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        self.text.append(data)
        if self.in_title:
            self.title.append(data)


class SeniorPropertyTaxGuideContract(unittest.TestCase):
    def setUp(self):
        self.source = GUIDE.read_text(encoding="utf-8") if GUIDE.exists() else ""
        self.parser = PageParser()
        self.parser.feed(self.source)
        self.visible = " ".join(" ".join(self.parser.text).split())

    def test_guide_has_unique_search_identity(self):
        self.assertEqual(self.parser.h1_count, 1)
        self.assertIn("Fort Bend County Property Tax Exemptions for Homeowners 65+", self.visible)
        self.assertIn("Fulshear", " ".join(self.parser.title))
        self.assertEqual(
            self.parser.canonicals,
            ["https://fulsheartxdirectory.com" + GUIDE_PATH],
        )

    def test_guide_explains_the_action_path_and_roles(self):
        for phrase in (
            "Fort Bend Central Appraisal District decides exemption eligibility",
            "Fort Bend County Tax Office handles tax bills and payments",
            "Form 50-114",
            "principal residence",
            "driver’s license or Texas ID",
            "Source check: August 29, 2026",
            "not legal or tax advice",
        ):
            self.assertIn(phrase, self.visible)

    def test_primary_official_sources_are_linked(self):
        expected = {
            "https://www.fbcad.org/homestead-exemptions/",
            "https://www.fbcad.org/exemption-application/",
            "https://www.fbcad.org/contact/",
            "https://comptroller.texas.gov/taxes/property-tax/exemptions/",
            "https://comptroller.texas.gov/forms/50-114.pdf",
            "https://www.fortbendcountytx.gov/government/departments/tax-assessor-collector/property-taxes",
        }
        self.assertTrue(expected.issubset(set(self.parser.links)), expected - set(self.parser.links))

    def test_guide_is_contextually_linked_from_existing_surfaces(self):
        self.assertIn(GUIDE_PATH, BLOG_INDEX.read_text(encoding="utf-8"))
        self.assertIn(GUIDE_PATH, HOME.read_text(encoding="utf-8"))

    def test_no_guaranteed_savings_or_current_tax_bill_claim(self):
        lowered = self.visible.lower()
        for claim in ("guaranteed savings", "will lower your bill", "guaranteed approval"):
            self.assertNotIn(claim, lowered)


if __name__ == "__main__":
    unittest.main()
