from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from backend import GeneHandler, PathwayGenerator
from werkzeug.middleware.profiler import ProfilerMiddleware
import os
import glob

# Initialize the Flask app
app = Flask(__name__, template_folder="templates")
# Ensure the "uploads" and "output" folders exist
script_dir = os.path.dirname(os.path.abspath(__file__))
uploads_folder = os.path.join(script_dir, "uploads")
output_folder = os.path.join(script_dir, "output")

os.makedirs(uploads_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)


@app.route("/")
def kegg_home():
    """Homepage with a list of questions about biological pathways."""
    questions = [
        "Which genes are involved in specific biological pathways and processes?",
        "How are certain metabolic pathways organized, and which enzymes play a role in them?",
        "What are the orthologous genes of different species for a given function?",
        "How can experimental data (e.g., gene expression) be integrated with known biological pathways?",
        "What molecular mechanisms underlie certain diseases?",
    ]
    return render_template("home.html", questions=questions)


@app.route('/about')
def about():
    """About page with details about the project and tools used."""
    return render_template('about.html')


@app.route('/contact')
def contact():
    """Contact page with team details."""
    return render_template('contact.html')


@app.route("/kegg_tool", methods=["GET", "POST"])
def kegg_tool():
    """
    Handles input from the KEGG Tool page and interacts with the backend
    to find pathways and generate pathway maps.
    """
    result = None
    error = None

    if request.method == "POST":
        genes_input = request.form.get("genes")  # Text input field for genes
        species = request.form.get("species")  # Species dropdown
        uploaded_file = request.files.get("gene_file")  # File upload field

        try:
            # Validate species selection
            if not species:
                raise ValueError("No species selected. Please choose a species.")

            # Process the input genes
            gene_list = []
            if genes_input:
                # Split input genes by commas
                gene_list = [gene.strip() for gene in genes_input.split(",")]
            elif uploaded_file:
                # Save the uploaded file and read the gene list from it
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join(uploads_folder, filename)
                uploaded_file.save(file_path)

                # Read the file line by line to get gene names
                with open(file_path, "r") as f:
                    gene_list = list(map(str.strip, f))

            if not gene_list:
                raise ValueError("No genes provided. Please enter genes or upload a file.")

            # Map genes to KEGG IDs
            gene_handler = GeneHandler(gene_list, species)
            gene_to_kegg = gene_handler.get_kegg_ids()

            if not gene_to_kegg:
                raise ValueError("No KEGG IDs found for the provided genes.")

            # Retrieve pathways for each KEGG ID
            kegg_ids = list(gene_to_kegg.values())
            kegg_to_pathways = gene_handler.get_pathway_ids(kegg_ids)

            # Generate pathway maps (one map per KEGG ID for its first associated pathway)
            pathway_generator = PathwayGenerator()
            for kegg_id, pathways in kegg_to_pathways.items():
                if pathways:
                    pathway_id = pathways[0]  # Use the first pathway ID for each KEGG ID
                    pathway_generator.save_pathway(pathway_id, [kegg_id], output_folder)

            result = f"Pathway maps generated successfully for the following genes: {', '.join(gene_list)}"
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("kegg_tool.html", result=result, error=error)


@app.route("/pathway")
def generated_image_pathway():
    """Shows the most recent KEGG pathway image on a new page."""
    # Find the latest PNG file in the output directory
    png_files = sorted(
        glob.glob(os.path.join(output_folder, "*.png")),
        key=os.path.getmtime,
        reverse=True
    )

    # Get the path to the most recent PNG file
    image_path = None
    if png_files:
        image_path = f"/output{os.path.basename(png_files[0])}"  # Use the output route

    # Render the template with the image path
    return render_template("pathway.html", image_path=image_path)


@app.route("/latest_image")
def latest_image():
    """Serves the most recent KEGG pathway image as a file stream."""
    try:
        # Find the latest PNG file in the output directory
        png_files = sorted(
            glob.glob(os.path.join(output_folder, "*.png")),
            key=os.path.getmtime,
            reverse=True
        )

        if png_files:
            latest_image_path = png_files[0]
            # Serve the image as a file stream
            return send_file(latest_image_path, mimetype="image/png")

        # If no PNG files are found
        return "No images found in the output folder.", 404

    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir="profiling", restrictions="app.py")
    app.run(debug=True)
