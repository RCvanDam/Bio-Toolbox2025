import unittest
from unittest.mock import patch
from app import app  # Import your Flask app here
import pytest
import html5lib


class KeggToolTestCase(unittest.TestCase):
    """
    Unit tests for the `/kegg_tool` route of the Flask application.
    This test suite covers:
    - GET request for rendering the tool page.
    - POST request for processing KEGG IDs.
    - Error handling for invalid or failed backend processing.
    """

    def initialize_resources(self):
        """
        Sets up the test client for the Flask application.
        The test client simulates HTTP requests to the `/kegg_tool` route.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_kegg_tool_route_get(self):
        """
        Test the `/kegg_tool` route (GET method).
        Ensures that the page loads successfully with status code 200
        and contains the expected form fields for input.
        """
        response = self.app.get('/kegg_tool')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"KEGG ID to Look For", response.data)

    @patch('app.backend.process_request')  # Mocking the backend
    def test_kegg_tool_route_post(self, mock_process_request):
        """
        Test form submission on the `/kegg_tool` route (POST method).
        Simulates a valid form submission with a single KEGG ID
        and mocks successful backend processing.
        """
        mock_process_request.return_value = None  # Mock successful processing

        response = self.app.post('/kegg_tool', data={'single_kegg_id': 'hsa:1234'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Pathway visualization generated successfully!", response.data)

    @patch('app.backend.process_request')  # Mocking the backend
    def test_kegg_tool_route_post_error(self, mock_process_request):
        """
        Test form submission on the `/kegg_tool` route (POST method).
        Simulates a form submission where the backend raises an exception
        to test error handling.
        """
        mock_process_request.side_effect = Exception("Backend error")  # Mock exception

        response = self.app.post('/kegg_tool', data={'single_kegg_id': 'hsa:1234'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Error: Unable to process the KEGG ID", response.data)


class TestAboutPage(unittest.TestCase):
    def setUp(self):
        # Use the imported app instance for testing
        app.config['TESTING'] = True
        self.client = app.test_client()  # Create a test client

    def test_about_page_loads(self):
        """
        Test that the /about page loads correctly and contains expected content.
        """
        response = self.client.get('/about')

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check for specific content in the HTML response (as bytes)
        self.assertIn(b'Behind Map My KEGG', response.data)
        self.assertIn(b'Who Are We?', response.data)
        self.assertIn(b'Our Vision', response.data)
        self.assertIn(b'What We Offer', response.data)
        self.assertIn(b'The Tools We Use', response.data)
        self.assertIn(b'Explore Tools', response.data)


    @pytest.fixture
    def client(self):
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


if __name__ == '__main__':
    unittest.main()
