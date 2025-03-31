import unittest
from backend import PathwayVisualizer
from unittest.mock import patch

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
