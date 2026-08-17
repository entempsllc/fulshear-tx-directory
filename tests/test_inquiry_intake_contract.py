import re
import unittest
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
RECIPIENT = "entempsllc@gmail.com"
EXPECTED = {
    "Submit Your Business": "Fulshear TX Directory - Business Listing Submission",
    "Featured Listing & Sponsorship Inquiries": "Fulshear TX Directory - Featured Listing or Sponsorship Inquiry",
    "Update a Listing": "Fulshear TX Directory - Listing Update",
    "Contact Us": "Fulshear TX Directory - General Contact",
}


class InquiryIntakeContract(unittest.TestCase):
    def test_footer_inquiry_routes_are_attributable_mailtos(self):
        html = HOME.read_text(encoding="utf-8")
        for label, expected_subject in EXPECTED.items():
            with self.subTest(label=label):
                html_label = label.replace("&", "&amp;")
                pattern = r'<a\s+href="([^"]+)">' + re.escape(html_label) + r'</a>'
                match = re.search(pattern, html, re.I)
                self.assertIsNotNone(match, f"Missing footer action: {label}")
                parsed = urlparse(match.group(1).replace("&amp;", "&"))
                self.assertEqual(parsed.scheme, "mailto")
                self.assertEqual(parsed.path.lower(), RECIPIENT)
                subject = unquote(parse_qs(parsed.query)["subject"][0])
                self.assertEqual(subject, expected_subject)
                self.assertNotIn('href="#"', match.group(0))


if __name__ == "__main__":
    unittest.main()
