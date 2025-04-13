import pytest
from app import app

@pytest.fixture
def client():
    """Provides a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_base_structure(client):
    """Checks that common navbar elements are present on all implemented pages"""
    # List of routes that should be implemented
    pages = ['/', '/about', '/contact', '/kegg_tool']

    for page in pages:
        response = client.get(page)
        # Verify the page loads successfully
        assert response.status_code == 200, f"Failed to load {page}"

        # Check if the navigation bar and expected links are included
        assert b'<div class="navbar">' in response.data
        assert b'<a href="/">Home</a>' in response.data
        assert b'<a href="/kegg_tool">KEGG Tools</a>' in response.data
        assert b'<a href="/about">About Us</a>' in response.data
        assert b'<a href="/contact">Contact Info</a>' in response.data


def test_home_page(client):
    """Checks that the home page includes key content and questions"""
    response = client.get('/')

    # Content that should always appear on the home page
    content_checks = [
        b"Map My KEGG",
        b"What is Map My KEGG?",
        b"Explore Tools",
        b"https://www.genome.jp/kegg/docs/fig/kegg_model.png",
    ]

    for content in content_checks:
        assert content in response.data, f"Missing content: {content}"

    # Verify that questions are shown on the home page
    expected_questions = [
        "Which genes are involved in specific biological pathways and processes?",
        "How are certain metabolic pathways organized, and which enzymes play a role in them?",
        "What are the orthologous genes of different species for a given function?",
        "How can experimental data (e.g., gene expression) be integrated with known biological pathways?",
        "What molecular mechanisms underlie certain diseases?"
    ]

    for question in expected_questions:
        assert question.encode() in response.data, f"Question not found: {question}"


def test_about_page(client):
    """Checks that the about page contains section headings, tools, and a CTA link"""
    response = client.get('/about')

    content_checks = [
        b"Behind Map My KEGG",
        b"Who Are We?",
        b"Our Vision",
        b"What We Offer",
        b"The Tools We Use",
        b"KEGG Pull",
        b"KEGG Mapper",
        b'<a href="/kegg_tool" class="cta-button">'
    ]

    for content in content_checks:
        assert content in response.data, f"Missing content: {content}"


def test_contact_page(client):
    """Verifies that the contact page lists all team members and includes their GitHub links"""
    response = client.get('/contact')

    content_checks = [
        b"Contact Us",
        b"Our Team",
        b"Emiel Bosma",
        b"Michelle Hazeveld",
        b"Keren Saint Fleur",
        b"Ruben van Dam",
        b"GitHub: emielbosma",
        b"GitHub: michellehazeveld",
        b"GitHub: Keren8272",
        b"GitHub: RCvanDam"
    ]

    for content in content_checks:
        assert content in response.data, f"Missing content: {content}"

    # Confirm that exactly four contact cards are rendered
    assert response.data.count(b'contact-card') == 4


def test_kegg_tool_page(client):
    """Checks that the KEGG tool page includes form fields and species options"""
    response = client.get('/kegg_tool')

    # Check for the presence of form elements and key labels
    content_checks = [
        b"KEGG Tool",
        b"Generate KEGG Pathways",
        b"Choose a species:",
        b"Enter Gene Names",
        b"Find KEGG Pathway",
        b'<form method="POST"'
    ]

    for content in content_checks:
        assert content in response.data, f"Missing content: {content}"

    # Check that all predefined species options are available in the dropdown
    species_options = [
        b"Human (Homo sapiens)",
        b"House Mouse (Mus musculus)",
        b"Rat (Rattus norvegicus)",
        b"E. coli (Escherichia coli)",
        b"Yeast (Saccharomyces cerevisiae)"
    ]

    for option in species_options:
        assert option in response.data, f"Missing species option: {option}"


def test_kegg_tool_form_submission(client):
    """Sends example POST requests to the KEGG form and checks for feedback messages"""
    test_cases = [
        {'species': 'hsa', 'genes': 'BRCA1, TP53'},
        {'species': 'mmu', 'genes': 'Trp53, Brca1'},
    ]

    for case in test_cases:
        response = client.post('/kegg_tool', data=case)

        # Should return a successful page load regardless of KEGG response
        assert response.status_code == 200

        # Ensure either success or error feedback is shown
        assert (b"alert alert-success" in response.data) or (b"alert alert-danger" in response.data)


def test_page_titles(client):
    """Verifies that each page contains the correct <title> tag text"""
    pages = {
        '/'         : b'Map My KEGG',
        '/about'    : b'Behind Map My KEGG',
        '/contact'  : b'Contact Us',
        '/kegg_tool': b'KEGG_pull - Map My KEGG'
    }

    for path, title in pages.items():
        response = client.get(path)
        # Look for the expected title text inside the page HTML
        assert title in response.data, f"Missing title {title} on {path}"
