import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [audioFile, setAudioFile] = useState(null);
    const [transcription, setTranscription] = useState('');

    const handleFileChange = (e) => {
        setAudioFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!audioFile) {
            alert('Please select a file first!');
            return;
        }

        const formData = new FormData();
        formData.append('audio', audioFile);

        try {
            const response = await axios.post('http://127.0.0.1:5000/transcribe', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            setTranscription(response.data.transcription);
        } catch (error) {
            console.error(error);
            alert('Error uploading file!');
        }
    };

    return (
        <div className="container mt-5">
            <h1 className="text-center">Audio Transcriber</h1>
            <div className="mb-3">
                <label htmlFor="fileUpload" className="form-label">Upload an audio file</label>
                <input type="file" className="form-control" id="fileUpload" onChange={handleFileChange} />
            </div>
            <button className="btn btn-primary" onClick={handleUpload}>Transcribe</button>
            {transcription && (
                <div className="mt-3">
                    <h3>Transcription:</h3>
                    <p>{transcription}</p>
                </div>
            )}
        </div>
    );
}

export default App;
