import whisper
import ssl
import warnings
from pydub import AudioSegment
from concurrent.futures import ProcessPoolExecutor
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# # Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

# # Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# # Load the Whisper model once to avoid reloading it multiple times
model = whisper.load_model("tiny", device="cpu")
gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

GENZ_SLANGS = "mid, rizz, peak, prime, GOAT, alpha, sigma,cap, no cap, Ws in the chat, W, L, Lit, Ick, It's giving, Baddie, Period, Ohio, Slay, Flex, Big Yikes, Bop, Yikes, Bet, gimme, Sus, fanum tax, Gyat, Bussin, lowkey, crap, Delulu, Ate, Mogged, Ate, Gucci"


# Main function to handle the transcription process
def transcribe_audio(file):
    """Transcribes the given audio file."""
    lecture_text = model.transcribe(file)
    final_transcription = text_to_slang(lecture_text["text"])


    return final_transcription
    
def text_to_slang(lecture_text):

    summary_messages = [
        {"role": "system", "content": "You will provide thorough summaries of lectures."},
        {"role": "user", "content": f"Please summarize this text: \n\n {lecture_text}"}
    ]

    summary_completion = gpt_client.chat.completions.create(
        model="gpt-4",
        messages=summary_messages
    )

    summary = summary_completion.choices[0].message.content

    reading_time_seconds = len(lecture_text) / 16.67 # Obtain total read time of original lecture
    time_constraint = reading_time_seconds / 3  # Condense to 1/3rd of the time

    # Now, use the summary in the main task
    messages = [
        {"role": "system", "content": "Your gotta translate lecture into gen-alpha slang.RULES: no emojis, no newlines, try to use these words \n\n " + GENZ_SLANGS + "" },
        {"role": "user", "content": f"Here's a summary of the lecture: {summary} \n\n Now, provide a {time_constraint}-second slangified lecture."}
    ]

    completion = gpt_client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )

    slangified_summary = completion.choices[0].message.content

    return slangified_summary

# Entry point to handle command-line execution or function call
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python whisper_transcriber.py <audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]
    transcription = transcribe_audio(audio_path)
    print(transcription)




