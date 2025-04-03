from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")


@app.route("/")
def kegg_home():
    """This function contains a list of questions that could be
    answered with our website and tool, and represents the homepage in
    which the questions below are shown."""
    questions = ["Which genes are involved in specific biological pathways \
    and processes?", "How are certain metabolic pathways organized, and \
    which enzymes play a role in them?", "What are the orthologous genes \
    of different species for a given function? How can experimental data \
    (e.g., gene expression) be integrated with known biological pathways?",
    "What molecular mechanisms underlie certain diseases?", "Which \
    biochemical reactions are related to specific chemical compounds or \
    enzymes?"]

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
    number = None
    if request.method == "POST":
        number = request.form["number"]
        if not number:
            return "error: no number entered", 400
    return render_template("kegg_tool.html", number=number)


if __name__ == '__main__':
    # Setting debug on True will restart the server on each change.
    app.run(debug=True)
