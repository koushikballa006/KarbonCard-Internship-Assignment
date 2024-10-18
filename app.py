from flask import Flask, request, jsonify
from flask_cors import CORS
from model import analyze_json_data

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.json'):
        try:
            content = file.read()
            result = analyze_json_data(content)
            return jsonify(result)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "Invalid file type. Please upload a JSON file."}), 400

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True, port=5000)