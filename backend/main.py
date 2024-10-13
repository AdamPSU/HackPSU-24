from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Body
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pyht import Client
from pyht.client import TTSOptions
from dotenv import load_dotenv
from transcribeText import transcribe_audio
from pydantic import BaseModel
import os
import io

load_dotenv()

app = FastAPI()

# CORS setup for local development
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize TTS client
client = Client(
    user_id=os.getenv("PLAY_HT_USER_ID"),
    api_key=os.getenv("PLAY_HT_API_KEY"),
)


@app.post("/transcribe-audio/")
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    """
    FastAPI endpoint to handle audio file uploads and return transcriptions.

    This async function receives an audio file upload, saves it temporarily,
    transcribes it using the transcribe_audio function, and returns the
    slangified transcription as a JSON response.

    Args:
        file (UploadFile): The uploaded audio file.

    Returns:
        JSONResponse: A JSON object containing the slangified transcription.

    Raises:
        HTTPException: 500 status code if any error occurs during processing.
    """

    try:
        # Save the uploaded audio file temporarily
        audio_path = f"./{file.filename}"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(await file.read())

        # Call the transcribe_audio function from transcribeText.py
        transcription = transcribe_audio(audio_path)

        # Clean up the saved audio file
        os.remove(audio_path)

        # Return the transcription as a JSON response
        return JSONResponse({"transcription": transcription})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TTSRequest(BaseModel):
    """Defines the structure for TTS requests."""

    text: str


@app.post("/generate-audio/")
async def generate_audio(request: TTSRequest):
    """
    FastAPI endpoint to generate audio from text using Text-to-Speech (TTS).

    This async function receives a TTSRequest containing text, generates audio using
    a TTS client, and returns the audio as a streaming response.

    Args:
        request (TTSRequest): A Pydantic model containing the text to be converted to speech.

    Returns:
        StreamingResponse: An audio stream of the generated speech in MP3 format.

    Raises:
        HTTPException:
            - 400 status code if no text is provided in the request.
            - 500 status code if audio generation fails.
    """

    text = request.text

    if not text:
        raise HTTPException(status_code=400, detail="No text provided for audio generation")

    # Define TTS options
    options = TTSOptions(
        voice="s3://voice-cloning-zero-shot/8218bea1-aad9-49cc-95b3-e9234e28d4a6/wilbursaad/manifest.json",
        speed=1.0,
        temperature=0.5,
    )

    try:
        audio_buffer = io.BytesIO()

        # Generate audio chunks from the TTS client
        for chunk in client.tts(text, options):
            audio_buffer.write(chunk)

        audio_buffer.seek(0)  # Reset buffer to the start

        # Return the audio as a streaming response
        return StreamingResponse(audio_buffer, media_type="audio/mpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio generation failed: {str(e)}")







