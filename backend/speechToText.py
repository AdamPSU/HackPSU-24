
import whisper
import ssl
import warnings
from pydub import AudioSegment
from concurrent.futures import ProcessPoolExecutor

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Path to the audio file
audio_path = "/Users/sumedhmarathe/Downloads/lecture_audio_big_sample.mp3"

# Function to split audio into chunks 
def split_audio(file, chunk_length_ms=60000,overlap_ms=5000):
    audio = AudioSegment.from_file(file)
    return [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

# Function to transcribe a single audio chunk
def transcribe_chunk(chunk, index):
    """Transcribe a chunk with a new Whisper model instance."""
    chunk_path = f"chunk_{index}.mp3"
    chunk.export(chunk_path, format="mp3")

    if len(chunk) == 0:
        print(f"Skipping empty chunk {index}")
        return ""

    # Load a new Whisper model instance inside the process
    model = whisper.load_model("tiny", device="cpu")
    result = model.transcribe(chunk_path)
    return result["text"]

# Main function to manage multiprocessing
def main():
    # Split the audio into chunks
    print("Splitting audio into chunks...")
    chunks = split_audio(audio_path)

    # Use ProcessPoolExecutor to transcribe chunks in parallel
    print("Transcribing... This may take a while.")
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(transcribe_chunk, chunk, i) for i, chunk in enumerate(chunks)]
        results = [future.result() for future in futures]

    # Combine the results from all chunks
    final_transcription = " ".join(results)

    # Print the final transcription
    print(final_transcription)


if __name__ == '__main__':
    main()
