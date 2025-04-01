import unittest
from unittest.mock import patch
from app import app  # Import your Flask app here


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


if __name__ == '__main__':
    unittest.main()
