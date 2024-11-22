import os
from flask import Flask, render_template, request, jsonify
from inference_sdk import InferenceHTTPClient

app = Flask(__name__)

# Initialize Roboflow Inference Client using new API key
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="n59gY3c0QFhpjUrAOrCK"  # Updated API key
)

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/realtime')
def realtime_detection():
    return render_template('realtime-index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')


@app.route('/upload-single-image', methods=['POST'])
def upload_single_image():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    result = CLIENT.infer(file_path, model_id="fish-freshness-6-o2ijt/2")
    return jsonify(result)

@app.route('/upload-batch-images', methods=['POST'])
def upload_batch_images():
    files = request.files.getlist('files')
    results = []

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        result = CLIENT.infer(file_path, model_id="fish-freshness-6-o2ijt/2")
        results.append({file.filename: result})

    return jsonify(results)

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render, or default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
