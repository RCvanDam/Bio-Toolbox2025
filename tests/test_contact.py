import pytest
from app import app

@pytest.fixture()
def client():
    return app.test_client()  # Create and return a test client for the app


def test_contact_page_load(client):
    """Test the about route."""
    response = client.get('/contact')
    assert response.status_code == 200  # Check if the page loads successfully


def test_contact_page_members(client):
    """Check team details on contact page."""
    team_members = {
        "Emiel Bosma": "GitHub: emielbosma",
        "Michelle Hazeveld": "GitHub: michellehazeveld",
        "Keren Saint Fleur": "GitHub: Keren8272",
        "Ruben van Dam": "GitHub: RCvanDam"
    }

    response = client.get('/contact')

    # Check if all expected team members are present in the response
    for name, github in team_members.items():
        assert name.encode() in response.data, f"{name} is missing from the contact page."
        assert github.encode() in response.data, f"{github} is missing from the contact page."

