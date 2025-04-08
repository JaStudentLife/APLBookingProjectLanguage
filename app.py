from flask import Flask, request, jsonify
from parser import parser
import builtins

app = Flask(__name__)

# Store command output
output_log = []

@app.route("/")
def home():
    return "Custom Language + Gemini is alive on Azure!"

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

old_print = print

def custom_print(*args, **kwargs):
    output_log.append(" ".join(map(str, args)))

builtins.print = custom_print
