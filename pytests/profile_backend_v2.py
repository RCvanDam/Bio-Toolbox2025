"""
Author: Emiel Bosma
Description: Analyzes the efficiency of the KEGG mapping code.
Uses cProfile and pstats for performance insights.
Date: 06/04/2025
Version: 1.1
"""

import cProfile
import pstats
import io
import os
import subprocess
from backend import GeneHandler, PathwayGenerator  # Import backend classes

# Example gene list for testing
genes = ["BRCA1", "TP53", "EGFR", "MYC", "AKT1"]
species = "hsa"  # Human genes

def run_program():
    """
    Executes KEGG mapping and pathway visualization.
    """
    handler = GeneHandler(genes=genes, species=species)
    generator = PathwayGenerator()

    # Convert genes to KEGG IDs
    gene_to_kegg = handler.get_kegg_ids()

    print("\n~~~~ GENE TO KEGG MAPPING ~~~~")
    for gene, kegg_id in gene_to_kegg.items():
        print(f"{gene} ➜ {kegg_id}")

    # Retrieve pathways for each KEGG ID
    kegg_ids = list(gene_to_kegg.values())
    kegg_to_pathways = handler.get_pathway_ids(kegg_ids)

    print("\n~~~~ PATHWAY ASSOCIATIONS ~~~~")
    for kegg_id, pathways in kegg_to_pathways.items():
        print(f"{kegg_id} ➜ {pathways}")

        # Save one sample pathway map if available
        if pathways:
            pathway_id = pathways[0]
            output_folder = "output_pathways"
            os.makedirs(output_folder, exist_ok=True)
            generator.save_pathway(pathway_id, highlighted_genes=[kegg_id], output_folder=output_folder)
            print(f"Saved pathway: {pathway_id} in {output_folder}")

if __name__ == "__main__":
    """
    Main block that runs profiling and optionally visualizes with SnakeViz.
    """
    profiler = cProfile.Profile()
    profiler.enable()

    run_program()

    profiler.disable()
    stats_buffer = io.StringIO()
    stats = pstats.Stats(profiler, stream=stats_buffer).sort_stats('cumulative')
    stats.print_stats()

    print("\n~~~~ PROFILING SUMMARY ~~~~")
    print(stats_buffer.getvalue())

    # Save profiling stats to a .prof file
    profile_filename = "profile_output.prof"
    profiler.dump_stats(profile_filename)

    # Try launching SnakeViz for visual profiling
    try:
        print("\nLaunching SnakeViz interactive visualization...")
        subprocess.run(["snakeviz", profile_filename])
    except FileNotFoundError:
        print("\n[!] SnakeViz is not installed.")
        print("You can install it by running:")
        print("   pip install snakeviz")
        print(f"Or visualize later with: snakeviz {profile_filename}")
