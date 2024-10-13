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


GENZ_SLANG = "mid, rizz, peak, prime, GOAT, alpha, sigma,cap, no cap, Ws in the chat, W, L, Lit, Ick, It's giving, Baddie, Period, Ohio, Slay, Flex, Big Yikes, Bop, Yikes, Bet, gimme, Sus, fanum tax, Gyat, Bussin, lowkey, crap, Delulu, Ate, Mogged, Ate, Gucci"




# Main function to handle the transcription process
def transcribe_audio(file):
    """
    Transcribe an audio file and convert the transcription to Gen-Alpha slang.

    This function first transcribes the given audio file using a speech-to-text model,
    then converts the transcription into a slangified version using the text_to_slang function.

    Args:
        file: The audio file to be transcribed (format depends on the transcription model used).

    Returns:
        str: A slangified version of the audio transcription, condensed and translated into Gen-Alpha slang.
    """

    lecture_text = model.transcribe(file)
    slang_lecture_text = text_to_slang(lecture_text["text"])


    return slang_lecture_text
    
def text_to_slang(lecture_text):
    """
    Convert a lecture text into a summarized, slangified version using Gen-Alpha slang.

    This function takes a lecture text, summarizes it using GPT-4, and then converts
    the summary into Gen-Alpha slang. The slangified version is condensed to
    approximately one-third of the original lecture's reading time.

    Args:
        lecture_text (str): The original lecture text to be summarized and slangified.

    Returns:
        str: A condensed, slangified version of the original lecture text.

    Note:
        - The function uses GPT-4 twice: for summarization and slangification.
        - The slangified output prohibits emojis and newlines.
        - The temperature for slangification is set to 0.7 for creative output.
    """

    summary_messages = [
        {"role": "system", "content": "You provide thorough summaries of lectures."},
        {"role": "user", "content": f"Summarize this text. Include all major topics and subtopics. \n\n {lecture_text}"}
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
        {"role": "system", "content": "Translate summaries into gen-Z slang. RULES: no emojis, no newlines, and try to use these words: \n\n " + GENZ_SLANG},
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



