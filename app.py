from flask import Flask, request, jsonify
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
        return jsonify({"file": file_name, "error": str(e)}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    file_name = data.get('file')
    product_name = data.get('product')
    
    if not file_name:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400
    
    if not product_name:
        return jsonify({"file": file_name, "error": "Invalid JSON input."}), 400
    
    try:
        file_path = os.path.join(pv_dir, file_name)
        if not os.path.exists(file_path):
            return jsonify({"file": file_name, "error": "File not found."}), 404
        
        total = 0
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) != 2:
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
                if parts[0] == product_name:
                    total += int(parts[1])
        
        return jsonify({"file": file_name, "sum": total}), 200
    except Exception as e:
        return jsonify({"file": file_name, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
