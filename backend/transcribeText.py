import whisper
import ssl
import warnings
from pydub import AudioSegment
from concurrent.futures import ProcessPoolExecutor
import os
import tempfile
from fastapi import UploadFile

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Load the Whisper model once to avoid reloading it multiple times
model = whisper.load_model("tiny", device="cpu")

# Function to split audio into chunks
def split_audio(file, chunk_length_ms=60000, overlap_ms=5000):
    """Splits the audio file into chunks with optional overlap."""
    audio = AudioSegment.from_file(file)
    return [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

# Function to transcribe a single audio chunk
def transcribe_chunk(chunk, index):
    """Transcribes a chunk with Whisper."""
    chunk_path = f"chunk_{index}.mp3"
    chunk.export(chunk_path, format="mp3")

    if len(chunk) == 0:
        print(f"Skipping empty chunk {index}")
        return ""

    print(f"Transcribing chunk {index}...")
    result = model.transcribe(chunk_path)
    
    # Clean up the temporary chunk file
    os.remove(chunk_path)
    
    return result["text"]

# Main function to handle the transcription process
def transcribe_audio(file):
    """Transcribes the given audio file."""
    # Split the audio into chunks
    print("Splitting audio into chunks...")
    chunks = split_audio(file)

    # Transcribe all chunks in parallel
    print("Transcribing... This may take a while.")
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(transcribe_chunk, chunk, i) for i, chunk in enumerate(chunks)]
        results = [future.result() for future in futures]

    # Combine all transcriptions
    final_transcription = " ".join(results)

    # Return the final transcription
    return final_transcription
    

# Entry point to handle command-line execution or function call
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python whisper_transcriber.py <audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]
    transcription = transcribe_audio(audio_path)
    print(transcription)




