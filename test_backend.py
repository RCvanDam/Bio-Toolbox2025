import os
import unittest
from backend import KEGGHandler, Backend, PathwayVisualizer
from unittest.mock import patch
import pytest  # Ensure pytest is imported for exception testing


class TestKEGGHandler(unittest.TestCase):
    """
    Unit tests for the KEGGHandler class.
    This test suite focuses on the `parse_pathway_data` function, ensuring that it:
    - Extracts nodes correctly.
    - Extracts edges correctly.
    - Handles irregular data gracefully.
    """

    def setUp(self):
        """
        Sets up the KEGGHandler instance for testing.
        """
        self.kegg_handler = KEGGHandler()

    def test_fetch_pathway_data_success(self):
        """This function tests the fetch_pathway_data method with a valid KEGG ID."""
        kegg_id = "hsa00010"
        mock_response = "PATHWAY DATA FOR TESTING"

        with patch.object(self.kegg_handler.kegg, "get", return_value=mock_response):
            result = self.kegg_handler.fetch_pathway_data(kegg_id)
            self.assertEqual(result, mock_response)

    def test_fetch_pathway_data_exception(self):
        """This function tests the fetch_pathway_data method if an error occurs."""
        kegg_id = "hsa00010"

        with patch.object(self.kegg_handler.kegg, "get", side_effect=Exception("API Error")):
            with pytest.raises(Exception, match="Error fetching pathway data: API Error"):
                self.kegg_handler.fetch_pathway_data(kegg_id)

    def test_parse_pathway_data_valid(self):
        """
        Test `parse_pathway_data` with valid KEGG pathway data.
        Ensures that nodes and edges are extracted correctly.
        """
        # Sample raw KEGG data (mocked for testing)
        kegg_data = """
        GENE 10327 AKR1A1
        COMPOUND C00022 Pyruvate
        REL_PATHWAY hsa00010 hsa00020
        """

        # Expected outputs
        expected_nodes = ['10327', 'C00022']
        expected_edges = [('hsa00010', 'hsa00020')]

        # Invoke the function
        nodes, edges = self.kegg_handler.parse_pathway_data(kegg_data)

        # Assert results
        self.assertEqual(nodes, expected_nodes)
        self.assertEqual(edges, expected_edges)

    def test_parse_pathway_data_empty(self):
        """
        Test `parse_pathway_data` with empty KEGG pathway data.
        Ensures that the function returns empty lists for nodes and edges.
        """
        kegg_data = ""  # Empty input

        # Invoke the function
        nodes, edges = self.kegg_handler.parse_pathway_data(kegg_data)

        # Assert results
        self.assertEqual(nodes, [])
        self.assertEqual(edges, [])

    def test_parse_pathway_data_partial(self):
        """
        Test `parse_pathway_data` with partially valid KEGG pathway data.
        Ensures that the function extracts what it can from the input.
        """
        kegg_data = """
        GENE 10327 AKR1A1
        INVALID_ENTRY
        COMPOUND C00022 Pyruvate
        """

        # Expected outputs
        expected_nodes = ['10327', 'C00022']
        expected_edges = []  # No valid edge entries

        # Invoke the function
        nodes, edges = self.kegg_handler.parse_pathway_data(kegg_data)

        # Assert results
        self.assertEqual(nodes, expected_nodes)
        self.assertEqual(edges, expected_edges)

        def test_process_request_creates_file():
            """
               Test if process_request creates an image file
               when given a valid KEGG pathway ID.
            """
            backend = Backend()

            # Use a  KEGG ID that usually works
            kegg_id = "hsa00010"
            output_file = "output/test_graph.png"

            # Run the function
            backend.process_request(kegg_id, output_file)

            # Check if the file was created
            assert os.path.exists(output_file)

        def test_process_request_invalid_kegg_id():
            """
                Test if process_request raises an exception
                when given an invalid KEGG ID.
                Also checks that no file is created.
            """
            backend = Backend()

            bad_kegg_id = "invalid123"
            output_file = "should_not_exist.png"

            with pytest.raises(Exception):
                backend.process_request(bad_kegg_id, output_file)

            # Make sure the file was not created
            assert not os.path.exists(output_file)

    class TestPathwayVisualizer(unittest.TestCase):
        """
        Simple unit test for the `create_graph` function in the `PathwayVisualizer` class.
        This test only confirms that the function runs without errors.
        """

        @patch('matplotlib.pyplot.savefig')  # Mock the savefig function
        @patch('networkx.draw')  # Mock the draw function
        def test_create_graph(self, mock_draw, mock_savefig):
            """
            Test that the `create_graph` function runs without errors.
            """

            # Arrange: Create test data
            nodes = ['gene1', 'gene2', 'gene3']
            edges = [('gene1', 'gene2'), ('gene2', 'gene3')]
            output_file = 'mock_pathway_graph.png'

            # Create an instance of PathwayVisualizer
            visualizer = PathwayVisualizer()

            # Act: Call the create_graph function
            visualizer.create_graph(nodes, edges, output_file)

            # Assert: Check if savefig was called
            mock_savefig.assert_called_once_with(output_file)

            # Assert: Check if draw was called
            mock_draw.assert_called_once()


if __name__ == '__main__':
    unittest.main()