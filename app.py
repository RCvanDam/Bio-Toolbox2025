from flask import Flask, render_template, request
from backend import Backend  # Importing the Backend class for KEGG functionality

app = Flask(__name__, template_folder="templates")
backend = Backend()  # Initialize the Backend instance

@app.route("/")
def kegg_home():
    """This function contains a list of questions that could be
    answered with our website and tool, and represents the homepage in
    which the questions below are shown."""
    questions = [
        "Which genes are involved in specific biological pathways and processes?",
        "How are certain metabolic pathways organized, and which enzymes play a role in them?",
        "What are the orthologous genes of different species for a given function?",
        "How can experimental data (e.g., gene expression) be integrated with known biological pathways?",
        "What molecular mechanisms underlie certain diseases?",
        "Which biochemical reactions are related to specific chemical compounds or enzymes?"
    ]

    return render_template("home.html", questions=questions)

@app.route('/about')
def about():
    """This function represents the about page. The about page gives a
    description of who we are, what the purpose of our website is and a
    short description of the tools we use."""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """This function represents the contact page. The contact page shows
    our first and last names, and our usernames of GitHub."""
    return render_template('contact.html')

@app.route("/kegg_tool", methods=["GET", "POST"])
def kegg_tool():
    image = None
    message = None

    if request.method == "POST":
        single_kegg_id = request.form.get("single_kegg_id")  # Single KEGG ID

        if single_kegg_id:
            output_file = "output/pathway.png"  # Updated path to save the KEGG pathway graph
            try:
                backend.process_request(single_kegg_id, output_file)  # Use the backend to process KEGG ID
                image = output_file
                message = "Pathway visualization generated successfully!"
            except Exception as e:
                message = f"Error: Unable to process the KEGG ID. Details: {str(e)}"
        else:
            message = "Please provide a valid KEGG ID."

    return render_template("kegg_tool.html", image=image, message=message)


if __name__ == '__main__':
    # Setting debug to True will restart the server on each change
    app.run(debug=True)

