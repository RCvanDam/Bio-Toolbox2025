from flask import Flask, render_template

app = Flask(__name__)


@app.route('/kegg_pull')
def kegg_pull():  # put application's code here
    return render_template('tool.html')


if __name__ == '__main__':
    app.run(debug=True)
