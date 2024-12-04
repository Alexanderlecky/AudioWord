import whisper 

def transcribe_chunks(chunks, model_name="base"):
    """Transcribes a list of audio chunks using Whisper."""
    model = whisper.load_model(model_name)
    full_transcription = [] 

    for idx, chunk in enumerate(chunks):
        temp_path = f"chunk_{idx}.mp3"
        chunk.export(temp_path, format="mp3")
        result = model.transcribe(temp_path)
        full_transcription.append({
            "start": idx * 60, #start time 
            "text": result['text']
        })

    return full_transcription

def format_transcription_markdown(transcription):
    """Formats the transcription into markdown text."""
    formatted = ""
    for entry in transcription:
        formatted += f"**[{entry['start']} sec]**: {entry['text']}\n\n"
    return formatted 

def save_as_srt(transcription, output_file="transcribe.srt"):
    """Saves the transcription as an SRT file."""
    with open(output_file, "w") as f:
        for i, entry in enumerate(transcription):
            start_time = entry['start']
            end_time = start_time + 60 
            f.write(f"{i+1}\n")
            f.write(f"00:{start_time:02d}:00 --> 00:{end_time:02d}:00\n")
            f.write(f"{entry['text']}\n\n")