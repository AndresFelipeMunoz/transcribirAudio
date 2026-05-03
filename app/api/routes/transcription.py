from fastapi import APIRouter, UploadFile, File, Depends, HTTPException  
import shutil
import tempfile
import os
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db 
from app.services.transcription_service import process_file, save_transcription
from app.models.user import User

router = APIRouter(prefix="/transcription", tags=["Transcription"])

@router.post("/", summary="Transcribir audio",
    description="Recibe un archivo de audio o video y retorna el texto transcrito")
async def transcribe(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    _, ext = os.path.splitext(file.filename)

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp:
        shutil.copyfileobj(file.file, temp)
        temp_path = temp.name

    try:
        text = process_file(temp_path)
        save_transcription(db, file.filename, text, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  
    finally:
        os.remove(temp_path)  # ← limpia el archivo temporal siempre

    return {
        "filename": file.filename,
        "transcription": text,
        "user": current_user.email  # ← opcional, útil para verificar que el auth funciona
    }
