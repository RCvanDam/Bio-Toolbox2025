import pytest
import html5lib
from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    try:
        parser = html5lib.HTMLParser(strict=True, namespaceHTMLElements=False)
        htmldoc = parser.parse(response.data)
    except html5lib.html5parser.ParseError as error:
        pytest.fail(f'{error.__class__.__name__}: {str(error)}', pytrace=False)
    items = htmldoc.findall(".div/ul")

    questions_list = []
    for item in items:
        questions_list.append(item.find(".question").text)
    return questions_list
    assert questions_list == {"Which genes are involved in specific biological pathways and processes?", "How are certain metabolic pathways organized, and which enzymes play a role in them?", "What are the orthologous genes of different species for a given function? How can experimental data (e.g., gene expression) be integrated with known biological pathways?",
    "What molecular mechanisms underlie certain diseases?", "Which biochemical reactions are related to specific chemical compounds or enzymes?"}