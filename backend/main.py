from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
app = FastAPI()
from fastapi import File, UploadFile

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create-rap")
async def create_rap(file: UploadFile = File(...)):
    return {"message": "Rap created"}