from flask import Flask, request, jsonify, render_template
from parser import parser
import builtins
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# Store output from commands
output_log = []

# Custom print function to capture command output
old_print = print
def custom_print(*args, **kwargs):
    output_log.append(" ".join(map(str, args)))
builtins.print = custom_print

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_command():
    command = request.json.get("command")
    if not command:
        return jsonify({"error": "Missing 'command'"}), 400

    try:
        output_log.clear()
        parser.parse(command)
        return jsonify({"response": output_log})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "UP"}), 200

if __name__ == "__main__":
    app.run(debug=True)
