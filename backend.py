import os
from bioservices import KEGG


class GeneHandler:
    def __init__(self, genes, species):
        """
        Initialize GeneHandler with genes and species information.

        Args:
            genes (list): List of genes provided by the user.
            species (str): Species code (e.g., 'hsa' for humans).
        """
        self.genes = genes
        self.species = species
        self.kegg_service = KEGG()
        print(f"KEGG service initialized for species: {self.species}")  # Debugging line

    def get_kegg_ids(self):
        """
        Maps genes to their corresponding KEGG IDs filtered by species.

        Returns:
            dict: A dictionary where keys are genes and values are KEGG IDs.
        """
        gene_to_kegg = {}
        try:
            # Batch request for all genes at once
            genes_batch = " ".join(self.genes)  # Join genes into a single string for batch request
            print(f"Sending batch API request for genes: {genes_batch}")  # Debugging line
            result = self.kegg_service.find("genes", genes_batch)
            print(f"Batch API response: {result}")  # Debugging line

            if result:
                # Parse the response and filter results by species
                for line in result.split("\n"):
                    if line.startswith(f"{self.species}:"):
                        gene_name = line.split("\t")[1].split(";")[0].strip()
                        kegg_id = line.split()[0]
                        gene_to_kegg[gene_name] = kegg_id
                        print(f"Mapped gene '{gene_name}' to KEGG ID: {kegg_id}")  # Debugging line
            else:
                print("No KEGG IDs found for the provided genes in batch request.")  # Debugging line
            return gene_to_kegg
        except Exception as e:
            print(f"Error retrieving KEGG IDs: {str(e)}")  # Debugging line
            raise Exception(f"Error retrieving KEGG IDs: {str(e)}")

    def get_pathway_ids(self, kegg_ids):
        """
        Retrieves pathway IDs associated with KEGG IDs.

        Args:
            kegg_ids (list or str): A single KEGG ID (str) or a list of KEGG IDs.

        Returns:
            dict: A dictionary mapping KEGG IDs to pathway IDs.
        """
        try:
            if isinstance(kegg_ids, list):
                kegg_to_pathways = {}
                # Batch request for pathway data
                kegg_ids_batch = " ".join(kegg_ids)  # Join KEGG IDs into a single batch request
                print(f"Sending batch API request for pathways: {kegg_ids_batch}")  # Debugging line
                pathway_data = self.kegg_service.get(kegg_ids_batch)
                print(f"Batch API response for pathways: {pathway_data}")  # Debugging line

                if pathway_data:
                    # Parse the response and extract pathway IDs
                    for kegg_id in kegg_ids:
                        pathways = [
                            line.split()[0].replace("path:", "")
                            for line in pathway_data.split("\n") if line.startswith("path:")
                        ]
                        kegg_to_pathways[kegg_id] = pathways
                        print(f"Pathways for KEGG ID {kegg_id}: {pathways}")  # Debugging line
                else:
                    print("No pathways found for the provided KEGG IDs in batch request.")  # Debugging line
                return kegg_to_pathways
            else:
                raise ValueError("Invalid input: 'kegg_ids' must be a list.")
        except Exception as e:
            print(f"Error retrieving pathway IDs: {str(e)}")  # Debugging line
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
        print("KEGG service initialized for pathway generation")  # Debugging line

    def save_pathway(self, pathway_id, file_name, highlighted_genes):
        try:
            # Ensure the 'output' folder exists
            output_folder = "output"
            os.makedirs(output_folder, exist_ok=True)

            # Build the full path for the output file
            output_path = os.path.join(output_folder, file_name)

            # Debugging outputs
            print(f"Attempting to save pathway map for pathway ID: {pathway_id}")  # Debugging line
            print(f"File path: {output_path}")  # Debugging line
            print(f"Highlighted genes: {highlighted_genes}")  # Debugging line

            # Call the bioservices save_pathway method
            self.kegg_service.save_pathway(pathway_id, output_path, keggid=highlighted_genes)
            print(f"Pathway map successfully saved to: {output_path}")  # Debugging line
        except Exception as e:
            print(f"Error generating pathway map for pathway ID {pathway_id}: {str(e)}")  # Debugging line
