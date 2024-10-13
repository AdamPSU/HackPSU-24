import whisper
import ssl
import warnings
import os
from pydub import AudioSegment
from concurrent.futures import ProcessPoolExecutor
import sys

# Disable SSL verification and suppress warnings
ssl._create_default_https_context = ssl._create_unverified_context
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

model = whisper.load_model("tiny", device="cpu")

def transcribe_audio(file_path, chunk_length_ms=60000):
    
    def split_audio(file, chunk_length):
        audio = AudioSegment.from_file(file)
        return [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]

    def transcribe_chunk(chunk, index):
        chunk_path = f"chunk_{index}.mp3"
        chunk.export(chunk_path, format="mp3")

        if len(chunk) == 0:
            return ""  

        result = model.transcribe(chunk_path)
        os.remove(chunk_path)  
        return result["text"]

    # Split the audio file into chunks
    chunks = split_audio(file_path, chunk_length_ms)
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(transcribe_chunk, chunk, i) for i, chunk in enumerate(chunks)]
        results = [future.result() for future in futures]

    # Combine and print the final transcription
    final_transcription = " ".join(results)
    print(final_transcription)

# Entry point for command-line usage
if __name__ == '__main__':
    audio_path = sys.argv[1]  # Get audio file path from command line
    transcribe_audio(audio_path)
