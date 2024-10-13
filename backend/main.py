from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pyht import Client
from pyht.client import TTSOptions
from dotenv import load_dotenv
import os
import io

#from transcription import transcribe_audio
load_dotenv()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Client(
    user_id=os.getenv("PLAY_HT_USER_ID"),
    api_key=os.getenv("PLAY_HT_API_KEY"),
)

@app.post("/transcribe-audio/")
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    try:
        # Save the uploaded audio file temporarily
        audio_path = f"./{file.filename}"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(await file.read())

        # Call the transcribe_audio function from transcribedText.py
        transcription = transcribe_audio(audio_path)

        # Clean up the saved audio file
        os.remove(audio_path)

        # Return the transcription as a JSON response
        return JSONResponse({"transcription": transcription})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def slang_to_audio():
    # Define the text and options
    text = "So, Kiwan Maeng kicks off the lecture by chatting 'bout the current homework grind,"
    options = TTSOptions(
       # voice="s3://voice-cloning-zero-shot/37e5af8b-800a-4a76-8f31-4203315f8a9e/billysaad/manifest.json",
        voice="s3://voice-cloning-zero-shot/8218bea1-aad9-49cc-95b3-e9234e28d4a6/wilbursaad/manifest.json",
        speed=1.0,
        temperature=0.5,
    )
    # Create an in-memory buffer to hold the audio
    audio_buffer = io.BytesIO()

    # Generate the audio and write to the buffer
    for chunk in client.tts(text, options):
        audio_buffer.write(chunk)
    
    # Reset buffer position to the beginning
    audio_buffer.seek(0)

    # Send the audio back to the frontend as a streaming response
    return StreamingResponse(audio_buffer, media_type="audio/mpeg")

@app.post("/generate-audio/")
async def generate_audio():
    # Sumedhs func
    # Text to slang 
    return slang_to_audio()