from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
pv_dir = "/tmp/persistent_volume"

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.get_json()
    file_name = data.get('file')
    file_data = data.get('data')
    
    if not file_name:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400
    
    if not file_data:
        return jsonify({"file": file_name, "error": "Invalid JSON input."}), 400
    
    try:
        file_path = os.path.join(pv_dir, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(file_data)
        return jsonify({"file": file_name, "message": "Success."}), 200
    except Exception as e:
        return jsonify({"file": file_name, "error": "Error while storing the file to the storage."}), 500

@app.route("/calculate", methods=['POST'])
def calculate():
    data = request.get_json()
    if not data or "file" not in data or not data["file"]:
        return jsonify({"file": None, "error": "Invalid JSON input."})
    
    file_name = data["file"]
    product = data.get("product")
    if not os.path.exists(f"/data/{file_name}"):
        return jsonify({"file": file_name, "error": "File not found."})
    
    response = requests.post("http://container2:8080/calculate", json={"file": file_name, "product": product})
    return jsonify(response.json()) 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
