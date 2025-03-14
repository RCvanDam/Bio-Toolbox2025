from flask import Flask, render_template

app = Flask(__name__)


@app.route("/kegg_home")
def kegg_home():
    questions = ["Which genes are involved in specific biological pathways and processes?", "How are certain metabolic \
    pathways organized, and which enzymes play a role in them?", "What are the orthologous genes of different \
    species for a given function? How can experimental data (e.g., gene expression) be integrated with \
    known biological pathways?", "What molecular mechanisms underlie certain diseases?", "Which biochemical \
    reactions are related to specific chemical compounds or enzymes?"]

    return render_template("home_html.html", questions=questions)


if __name__ == "__main__":
    app.debug = True
    app.run()