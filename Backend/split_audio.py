from pydub import AudioSegment 

def split_audio(file_path, chunk_length_ms=60000):
    """Splits audio into chunks of specified length (dafault: 60 seconds)."""
    audio = AudioSegment.form_file(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks 