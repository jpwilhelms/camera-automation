from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hoch', methods=['GET'])
def hoch():
    return jsonify({'message': 'Hoch-Kommando empfangen!'})

@app.route('/greifen', methods=['POST'])
def greifen():
    # Hier könnte man zusätzliche Logik für das "greifen"-Kommando einfügen
    return jsonify({'message': 'Greifen-Kommando empfangen!'})

if __name__ == '__main__':
    app.run(debug=True)

