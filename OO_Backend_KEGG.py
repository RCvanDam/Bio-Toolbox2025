"""
Authors: Emiel Bosma & Ruben van Dam
Description: This programme runs the backend part of our website
Version: 1.0
Date: 25/03/2025
"""


from flask import Flask, request, jsonify  # imports the library flask and its associated parts
import subprocess


app = Flask(__name__)


class Kmapper:
    def __init__(self, input_file, output_file, tool="kegg-mapper"):
        """
        This starts the mapper
        :param input_file: Name of the input file
        :param output_file: Name of the output file
        :param tool: Name of the KEGG tool: "kegg-mapper"
        """
        self.tool = tool
        self.input_file = input_file
        self.output_file = output_file


    def run(self):
        """
        Executes the KEGG-mapper tool

        """

        try:
            result = subprocess.run(
                [self.tool, "-i", self.input_file, "-o", self.output_file],
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}


    def __str__(self):
        """
        Gives a string representation of the object, useful for debugging purposes
        :return: string representation of the object
        """
        return f"Kmapper(tool= '{self.tool}', input_file= '{self.input_file}', output_file= '{self.output_file}')"


    @app.route("/run_kmapper", methods=["POST"])
    def run_kmapper(self):
        """
        API-endpoint to run KEGG-mapper via HTTP POST-request
        :return:
        """
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Not a valid json-file"})

        input_file = data.get("input_file")
        output_file = data.get("output_file")

        if not input_file or not output_file:
            return jsonify({"success": False, "error": "Not a valid json-file"})

        kmapper = Kmapper(input_file, output_file)
        result = kmapper.run()
        return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)