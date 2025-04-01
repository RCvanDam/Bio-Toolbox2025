import unittest
from backend import KEGGHandler


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


if __name__ == '__main__':
    unittest.main()
