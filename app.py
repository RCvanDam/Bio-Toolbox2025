from flask import *

app = Flask(__name__, template_folder="templates")

@app.route("/")
def default_route():
    # Redirect to /kegg_home on the first visit
    return redirect("/kegg_home")
@app.route("/kegg_home")
def kegg_home():
    questions = ["Which genes are involved in specific biological pathways and processes?", "How are certain metabolic \
    pathways organized, and which enzymes play a role in them?", "What are the orthologous genes of different \
    species for a given function? How can experimental data (e.g., gene expression) be integrated with \
    known biological pathways?", "What molecular mechanisms underlie certain diseases?", "Which biochemical \
    reactions are related to specific chemical compounds or enzymes?"]

    return render_template("kegg_home.html", questions=questions)
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route("/kegg_tool", methods=["GET", "POST"])
def kegg_tool():
    if request.method == "POST":
        number = request.form["number"]
        if not number:
            return "error: no number entered", 400
        return render_template("kegg_tool.html", number=number)
    return render_template("kegg_tool.html", number=None)


if __name__ == "__main__":
    app.debug = True
    app.run()

if __name__ == '__main__':
    app.run(debug=True)
