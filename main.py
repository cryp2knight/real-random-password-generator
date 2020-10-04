url = "https://api.random.org/json-rpc/2/invoke"
apiKey = "f918927b-eccc-4735-ac7d-fee09f82be87"

import requests
from string import ascii_letters, digits, punctuation

CHARACTERS = ascii_letters+digits+punctuation

def generate_random_numbers(n):
    data = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": apiKey,
            "n": n,
            "min": 0,
            "max": len(CHARACTERS)-1,
            "replacement": True
        },
        "id": 43
    }
    r = requests.post(url, json=data)
    return r.json()['result']['random']['data']

def generate_password(n=8):
    return "".join([CHARACTERS[i] for i in generate_random_numbers(n)])

from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({'password':generate_password()})

@app.route("/<length>")
def with_length(length):
    try:
        l = int(length)
    except ValueError:
        return jsonify({'error': 'string is not allowed. integer only'})
    else:
        if l > 10_000 or l <= 0:
            return jsonify({'error': 'out of range. allowable values are 1-10000'})
    try:
        return jsonify({'password':generate_password(l)})
    except:
        return jsonify({'error': 'an error occured'})

if __name__ == "__main__":
    app.run(debug=True)
