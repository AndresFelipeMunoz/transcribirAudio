from fastapi import FastAPI
from app.api.routes import auth, transcription

app = FastAPI(title="Transcription API")

app.include_router(transcription.router, prefix="/api")
app.include_router(auth.router, prefix="/api")