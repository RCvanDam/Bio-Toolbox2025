import os
from bioservices import KEGG

class GeneHandler:
    def __init__(self, genes):
        self.genes = genes
        self.kegg_service = KEGG()

    def get_kegg_ids(self):
        """
        Maps multiple genes to their corresponding KEGG IDs.

        Returns:
            dict: A dictionary where keys are genes and values are their KEGG IDs.
        """
        gene_to_kegg = {}
        try:
            for gene in self.genes:
                result = self.kegg_service.find("genes", gene)
                if result:
                    for line in result.split("\n"):
                        if line.startswith("genes"):
                            kegg_id = line.split()[1]  # Extract KEGG ID
                            gene_to_kegg[gene] = kegg_id
                            break
            return gene_to_kegg
        except Exception as e:
            raise Exception(f"Error retrieving KEGG IDs: {str(e)}")

    def get_pathway_ids(self, kegg_ids):
        """
        Retrieves pathway IDs associated with multiple KEGG IDs.

        Args:
            kegg_ids (list): A list of KEGG IDs.

        Returns:
            dict: A dictionary where keys are KEGG IDs and values are their pathway IDs.
        """
        kegg_to_pathways = {}
        try:
            for kegg_id in kegg_ids:
                pathway_data = self.kegg_service.get_pathway_by_gene(kegg_id)
                pathways = []
                for line in pathway_data.split("\n"):
                    if line.startswith("path:"):
                        pathways.append(line.split()[0].replace("path:", ""))
                kegg_to_pathways[kegg_id] = pathways
            return kegg_to_pathways
        except Exception as e:
            raise Exception(f"Error retrieving pathway IDs: {str(e)}")

    def get_pathway_ids(self, kegg_id):
        """
        Retrieves pathway IDs associated with a given KEGG ID.

        Args:
            kegg_id (str): The KEGG ID for the gene.

        Returns:
            list: A list of pathway IDs associated with the gene.
        """
        try:
            pathway_data = self.kegg_service.get_pathway_by_gene(kegg_id)
            pathway_ids = []
            for line in pathway_data.split("\n"):
                if line.startswith("path:"):
                    pathway_ids.append(line.split()[0].replace("path:", ""))
            return pathway_ids
        except Exception as e:
            raise Exception(f"Error retrieving pathway IDs: {str(e)}")


class PathwayGenerator:
    """
    Handles interactions with KEGG to generate and save pathway maps.
    """

    def __init__(self):
        """
        Initializes the PathwayGenerator with the KEGG service.
        """
        self.kegg_service = KEGG()

    def save_pathway(self, pathway_id, file_name, highlighted_genes):
        """
        Generates and saves a KEGG pathway map with highlighted genes.

        Args:
            pathway_id (str): The KEGG pathway ID (e.g., 'ko00340').
            file_name (str): Name of the output file (e.g., 'pathway.png').
            highlighted_genes (list): List of KEGG IDs to highlight.

        Returns:
            None
        """
        try:
            # Ensure the `output` folder exists
            output_folder = "output"
            os.makedirs(output_folder, exist_ok=True)

            # Build the full path for the output file
            output_path = os.path.join(output_folder, file_name)

            # Save pathway map as an image
            self.kegg_service.save_pathway(pathway_id, output_path, keggid=highlighted_genes)
            print(f"Pathway map saved to {output_path}")
        except Exception as e:
            raise Exception(f"Error generating pathway map: {str(e)}")