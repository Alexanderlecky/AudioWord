from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import whisper
import os 
from split_audio import split_audio 
from transcription import transcribe_chunks, format_transcription_markdown, save_as_srt
import warnings


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
CORS(app)  # Allows frontend to communicate with backend

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

model = whisper.load_model("base")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '' :
        return jsonify({'error': 'No file selected'}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    chunks = split_audio(filepath)
    transcription = transcribe_chunks(chunks)

    markdown_output = os.path.join(OUTPUT_FOLDER, 'transcription.md')
    str_output = os.path.join(OUTPUT_FOLDER, 'transcription.str')
    save_as_srt(transcription, srt_output)

    with open(markdown_output, 'w') as f:
        f.write(format_transcription_markdown(transcription))

    return jsonify({
        'message' : 'Transcription complete', 
        'markdown': markdown_output, 
        'srt': srt_output,
    })

if __name__ == '__main__':
    app.run(debug=True)
