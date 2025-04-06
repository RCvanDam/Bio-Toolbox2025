"""
Author: Emiel Bosma
Description: This program analyses the efficiency of the code.
Using cProfile and pstats this program visualizes the efficiency of the code.
Date: 06/04/2025
Version: 1.0
"""


import cProfile
import pstats
import io
import os
import subprocess
from backend import GeneHandler, PathwayGenerator  # Import the classes from your backend module

# Define a list of example gene names for analysis
genes = ["BRCA1", "TP53", "EGFR", "MYC", "AKT1"]


def run_program():
    """
    Runs the analysis using the classes GeneHandler and PathwayGenerator from backend.py.

    This function:
    - Instantiates a GeneHandler object with a list of genes
    - Maps each gene to its KEGG ID
    - Retrieves associated pathway IDs for each gene
    - Instantiates a PathwayGenerator and saves a sample pathway map
    - Prints the mapping and pathway information

    Return: None
    """
    handler = GeneHandler(genes)
    generator = PathwayGenerator()
    gene_to_kegg = handler.get_kegg_ids()

    for gene, kegg_id in gene_to_kegg.items():
        pathways = handler.get_pathway_ids(kegg_id)
        print(f"Gene: {gene}\n  KEGG ID: {kegg_id}\n  Pathways: {pathways}\n")

        # If at least one pathway exists, save a pathway image
        if pathways:
            pathway_id = pathways[0]  # Take the first pathway for demonstration
            output_filename = f"{gene}_pathway.png"
            generator.save_pathway(pathway_id, output_filename, [kegg_id])


if __name__ == "__main__":
    """
    Main code block that runs the whole program

    This block:
    - Profiles the run_program() function using cProfile
    - Prints profiling statistics to the console
    - Attempts to visualize profiling data with SnakeViz (if installed)

    requirements:
    - snakeviz (install via: pip install snakeviz)
    
    Note: the many print-statements have been added to make the output more user friendly

    Return: None
    """
    # Initialize the profiler
    profiler = cProfile.Profile()
    profiler.enable()

    # Runs the program
    run_program()

    # Stop the profiler
    profiler.disable()

    # Collect and format profiling statistics
    stats_buffer = io.StringIO()
    stats = pstats.Stats(profiler, stream=stats_buffer).sort_stats('cumulative')
    stats.print_stats()

    # Display the profiling summary in the console
    print("\n~~~~ PROFILING SUMMARY ~~~~")
    print(stats_buffer.getvalue())

    # Save the profiling output to a .prof file
    profile_filename = "profile_output.prof"
    profiler.dump_stats(profile_filename)

    # Try to launch SnakeViz automatically
    try:
        print("\nLaunching SnakeViz interactive visualization...")
        subprocess.run(["snakeviz", profile_filename])
    except FileNotFoundError:
        # Menu that shows up if SnakeViz is not installed
        print("\n[!] SnakeViz is not installed.")
        print("You can install it by typing this in the terminal:")
        print("-pip install snakeviz")
        print("\nProfiling data has been saved to:")
        print(f"    {profile_filename}")
        print("To visualize it later, run:")
        print(f"    snakeviz {profile_filename}")
