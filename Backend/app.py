from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os 
import warnings


app = Flask(__name__)
CORS(app)  # Allows frontend to communicate with backend

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

model = whisper.load_model("base")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    file_path = f"uploads/{audio_file.filename}"
    os.makedirs("uploads", exist_ok=True)
    audio_file.save(file_path)

    result = model.transcribe(file_path)
    return jsonify({'transcription': result['text']})

if __name__ == "__main__":
    app.run(debug=True)
