import os
import time
import requests


class GeneHandler:
    """
    A class to handle gene-to-KEGG ID mapping and pathway retrieval.

    Attributes:
        genes (list): List of gene names provided by the user.
        species (str): Species code (e.g., 'hsa' for humans).
        base_url (str): Base URL for the KEGG REST API.
    """

    def __init__(self, genes, species):
        """
        Initialize GeneHandler with genes and species information.

        Args:
            genes (list): List of genes provided by the user.
            species (str): Species code (e.g., 'hsa' for humans).
        """
        self.genes = genes
        self.species = species
        self.base_url = "http://rest.kegg.jp"

    def get_kegg_ids(self):
        """
        Maps genes to their corresponding KEGG IDs filtered by species.

        Returns:
            dict: A dictionary where keys are gene names and values are KEGG IDs.
        """
        gene_to_kegg = {}
        for gene in self.genes:
            try:
                url = f"{self.base_url}/find/genes/{gene}"
                response = requests.get(url)
                time.sleep(5)  # Avoid overwhelming the KEGG server

                if response.status_code == 200:
                    for line in response.text.split("\n"):
                        if line.startswith(f"{self.species}:"):
                            kegg_id = line.split("\t")[0]
                            gene_to_kegg[gene] = kegg_id
                            break
            except Exception:
                continue

        return gene_to_kegg

    def get_pathway_ids(self, kegg_ids):
        """
        Retrieves pathway IDs for a list of KEGG IDs.

        Args:
            kegg_ids (list): List of KEGG IDs.

        Returns:
            dict: A dictionary mapping KEGG IDs to lists of pathway IDs.
        """
        kegg_to_pathways = {}
        for kegg_id in kegg_ids:
            try:
                url = f"{self.base_url}/get/{kegg_id}"
                response = requests.get(url)
                time.sleep(5)  # Avoid overwhelming the KEGG server

                if response.status_code == 200:
                    pathways = []
                    for line in response.text.split("\n"):
                        if line.startswith("PATHWAY"):
                            pathway_id = line.split()[1]
                            pathways.append(pathway_id)
                    kegg_to_pathways[kegg_id] = pathways
            except Exception:
                continue

        return kegg_to_pathways


class PathwayGenerator:
    """
    A class to handle the generation and saving of pathway maps.

    Attributes:
        base_url (str): Base URL for the KEGG REST API.
    """

    def __init__(self):
        """
        Initialize PathwayGenerator with the KEGG REST API base URL.
        """
        self.base_url = "http://rest.kegg.jp"

    def save_pathway(self, pathway_id, highlighted_genes, output_folder: str):
        """
        Fetches and saves pathway map data using the KEGG REST API.

        Args:
            pathway_id (str): KEGG pathway ID (e.g., 'hsa04137').
            highlighted_genes (list): List of KEGG IDs to highlight (currently unused).
            output_folder: folder where png is stored

        Raises:
            Exception: If there is an error retrieving or saving the pathway map.
        """
        try:
            # Get the directory of the script
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Use the pathway ID as the file name
            sanitized_file_name = f"{pathway_id}.png"

            # Define the full output path
            output_path = os.path.join(output_folder, sanitized_file_name)

            # Fetch pathway details from the KEGG REST API
            url = f"{self.base_url}/get/{pathway_id}/image"
            response = requests.get(url, stream=True)
            time.sleep(5)  # Avoid overwhelming the KEGG server

            if response.status_code == 200 and response.headers.get("Content-Type") == "image/png":
                # Save the image data to a file
                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            else:
                # Fallback: Save response content as a text file
                fallback_path = output_path.replace(".png", ".txt")
                with open(fallback_path, "w") as f:
                    f.write(response.text)
        except Exception as e:
            # Use the pathway ID as the file name
            sanitized_file_name = f"{pathway_id}.png"

            output_path = os.path.join(output_folder, sanitized_file_name)
            fallback_path = output_path.replace(".png", "_error.txt")

            with open(fallback_path, "w") as f:
                f.write(f"Error retrieving pathway map: {str(e)}")