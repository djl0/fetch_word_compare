import json
from flask import Flask, request, jsonify

from word_compare import compare_text

app = Flask(__name__)

@app.route('/compare/', methods=['POST'])
def compare():
    req_data = request.json
    p1 = req_data['phrase1']
    p2 = req_data['phrase2']
    score = compare_text(p1, p2)
    return jsonify({'score': score})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
