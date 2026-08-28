import pytest
from bs4 import BeautifulSoup
import os

def test_senior_listings_contract():
    # Load index.html from the project root
    path = os.path.join(os.path.dirname(__file__), '../index.html')
    with open(path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # Check Senior Living category in grid (class cb)
    senior_cat = soup.find('a', class_='cb', href='#senior')
    assert senior_cat is not None
    assert 'Senior Living' in senior_cat.get_text()
    
    # Check Senior Living section
    senior_sec = soup.find('div', id='senior')
    assert senior_sec is not None
    assert 'Senior Living & Care' in senior_sec.get_text()
    
    # Verify exact business records added
    listings = [
        "Fulshear Senior Center (Irene Stern)",
        "Home Instead – Fulshear",
        "Providence Assisted Living Solutions",
        "Bonterra at Cross Creek Ranch",
        "Affectionate Care Assisted Living",
        "Fort Bend Seniors Meals on Wheels"
    ]
    
    content_text = senior_sec.get_text()
    for listing in listings:
        assert listing in content_text

def test_senior_listings_in_footer():
    path = os.path.join(os.path.dirname(__file__), '../index.html')
    with open(path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    footer = soup.find('footer')
    assert footer is not None
    senior_link = footer.find('a', href='#senior')
    assert senior_link is not None
    assert 'Senior Care' in senior_link.get_text()
