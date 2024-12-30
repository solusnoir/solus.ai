from flask import Flask, render_template, request, jsonify
import os
import librosa
import numpy as np

app = Flask(__name__)

# Set up absolute paths for uploads and results
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
RESULTS_FOLDER = os.path.join(BASE_DIR, 'results')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'm4a', 'flac'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to extract BPM
def extract_bpm(file_path):
    y, sr = librosa.load(file_path, sr=None, duration=30)  # Load only the first 30 seconds
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    return float(tempo)  # Return tempo as a float

# Function to extract key and confidence
def extract_key_and_confidence(file_path):
    y, sr = librosa.load(file_path, sr=None, duration=30)  # Load only the first 30 seconds
    harmonic = librosa.effects.harmonic(y)
    chroma = librosa.feature.chroma_cens(y=harmonic, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    key_index = np.argmax(chroma_mean)
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = keys[key_index]
    confidence = round(np.max(chroma_mean) * 100, 2)
    return key, confidence

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    return "Portfolio page is under construction!"  # Temporary placeholder

@app.route('/test')
def test():
    return "Flask is working!"  # Test route to check if Flask is running

@app.route('/find-key', methods=['GET', 'POST'])
def find_key():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            try:
                bpm = extract_bpm(filename)
                key, confidence = extract_key_and_confidence(filename)

                results = {
                    "file_name": file.filename,
                    "bpm": bpm,
                    "key": key,
                    "confidence": confidence
                }

                return jsonify(results)

            except Exception as e:
                app.logger.error(f"Error processing the audio: {str(e)}")  # Log the error
                return jsonify({"error": f"Error processing the audio: {e}"}), 500

    return render_template('find-key.html')


if __name__ == '__main__':
    app.run(debug=True)
