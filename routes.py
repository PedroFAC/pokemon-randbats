from flask import Flask, jsonify
import requests
from main import write_randbats_sets_to_file, write_smogon_sets_to_file

app = Flask(__name__)

@app.route("/randbats/<int:gen>")
@app.route("/randbats", defaults={"gen": 1})  # Provide a default value
def get_randbats_sets(gen):
    data = requests.get(f'https://pkmn.github.io/randbats/data/gen{gen}randombattle.json').json()
    write_randbats_sets_to_file(data)
    return jsonify(data)
@app.route("/smogon/<string:format>")
@app.route("/smogon", defaults={"format": "gen9ou"})  # Provide a default value
def get_smogon_sets(format):
    print(f"Received format: {format}")  # Debugging output
    data = requests.get(f'https://pkmn.github.io/smogon/data/sets/{format}.json').json()
    write_smogon_sets_to_file(data, f'{format}.txt')
    return jsonify(data)
@app.route("/formats")
def get_formats():
    data = requests.get(f'https://pkmn.github.io/smogon/data/sets/index.json').json()
    keys = [key.removesuffix('.json') for key in data.keys()]
    return jsonify(keys)

app.run(debug=True)
