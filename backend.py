import os
from bioservices import KEGG
import matplotlib.pyplot as plt
import networkx as nx  # For creating pathway graphs


class KEGGHandler:
    """
    Handles interactions with the KEGG database via bioservices.

    Methods:
        fetch_pathway_data(kegg_id): Fetches pathway data for a given KEGG ID.
        parse_pathway_data(kegg_data): Parses KEGG pathway data into nodes and edges for visualization.
    """

    def __init__(self):
        """
        Initializes the KEGGHandler with bioservices' KEGG module.
        """
        self.kegg = KEGG()

    def fetch_pathway_data(self, kegg_id):
        """
        Fetch pathway data for the given KEGG ID using the KEGG API.

        Args:
            kegg_id (str): The KEGG pathway ID provided by the user (e.g., 'hsa00010').

        Returns:
            str: Raw pathway data fetched dynamically from the KEGG database.
        """
        try:
            data = self.kegg.get(kegg_id)  # Query the KEGG API
            if not data:
                raise ValueError(f"No data found for pathway ID: {kegg_id}")
            return data
        except Exception as e:
            raise Exception(f"Error fetching pathway data: {str(e)}")

    def parse_pathway_data(self, kegg_data):
        """
        Parses the raw KEGG pathway data to extract nodes and edges for graph visualization.

        Args:
            kegg_data (str): Raw pathway data retrieved from the KEGG database.

        Returns:
            tuple: A tuple containing:
                - nodes (list): A list of unique nodes extracted from the pathway. Nodes may represent genes or compounds.
                - edges (list): A list of edges (relationships) between nodes in the pathway.

        Example:
            For a pathway with gene and compound relationships, nodes will include gene IDs
            (e.g., `10327` for AKR1A1) and compound IDs (e.g., `C00022` for pyruvate).
            Edges may represent associations between related genes, compounds, or pathways.

        Notes:
            This method assumes a specific structure of the raw KEGG data, including sections like
            'GENE', 'COMPOUND', and potentially 'REL_PATHWAY' for relationships. Adjustments
            may be needed for different pathway types or irregular data formats.
        """
        nodes, edges = [], []

        # Extract genes and compounds as nodes
        for line in kegg_data.split("\n"):
            if line.startswith("GENE"):
                parts = line.split()
                nodes.append(parts[1])  # Add gene IDs as nodes
            elif line.startswith("COMPOUND"):
                parts = line.split()
                nodes.append(parts[1])  # Add compound IDs as nodes

            # Add edges based on relationships (if RELATION or REL_PATHWAY data exists)
            if line.startswith("REL_PATHWAY"):
                related_pathways = line.split()
                edges.append((related_pathways[0], related_pathways[1]))  # Add pathway relationships as edges

        return nodes, edges


class PathwayVisualizer:
    """
    Visualizes KEGG pathways using Matplotlib and NetworkX.

    Methods:
        create_graph(nodes, edges, output_file): Creates a pathway graph and saves it as an image file.
    """

    def __init__(self):
        """
        Initializes the PathwayVisualizer.
        """
        pass

    def create_graph(self, nodes, edges, output_file):
        """
        Creates and saves a graph of the pathway based on nodes and edges.

        Args:
            nodes (list): List of nodes in the pathway (e.g., enzymes, compounds).
            edges (list): List of edges representing relationships between nodes.
            output_file (str): File path where the graph image will be saved.

        Returns:
            None: The graph is saved as an image file.
        """
        G = nx.DiGraph()  # Create a directed graph
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        plt.figure(figsize=(12, 8))
        nx.draw(G, with_labels=True, node_color="skyblue", font_size=8, node_size=500)
        plt.title("KEGG Pathway Visualization")
        plt.savefig(output_file)


class Backend:
    """
    Combines KEGGHandler and PathwayVisualizer to process user requests and generate pathway maps.

    Methods:
        process_request(kegg_id, output_file): Fetches, parses, and visualizes KEGG pathway data.
    """

    def __init__(self):
        """
        Initializes the Backend with KEGGHandler and PathwayVisualizer instances.
        """
        self.kegg_handler = KEGGHandler()
        self.visualizer = PathwayVisualizer()

    def process_request(self, kegg_id, output_file):
        """
        Processes a user request to fetch pathway data, parse it, and generate a pathway visualization.

        Args:
            kegg_id (str): The KEGG pathway ID input by the user (e.g., 'hsa00010').
            output_file (str): Path to save the generated pathway graph image.

        Returns:
            None: Generates and saves the graph image to the specified file path.
        """
        try:
            # Ensure the directory for the output file exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            # Fetch pathway data dynamically using the KEGG API
            kegg_data = self.kegg_handler.fetch_pathway_data(kegg_id)

            # Parse the data into nodes and edges
            nodes, edges = self.kegg_handler.parse_pathway_data(kegg_data)

            # Generate the pathway visualization
            self.visualizer.create_graph(nodes, edges, output_file)
        except Exception as e:
            raise Exception(f"Error processing pathway ID {kegg_id}: {str(e)}")
