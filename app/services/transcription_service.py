from moviepy import AudioFileClip, VideoFileClip
import speech_recognition as sr
import os
from sqlalchemy.orm import Session                    
from app.models.transcription import Transcription   


AUDIO_EXTENSIONS = ['.ogg', '.wav', '.mp3', '.flac', '.aac', '.m4a']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']

def extract_audio(media_path, output_wav):
    if any(media_path.lower().endswith(ext) for ext in AUDIO_EXTENSIONS):
        audio_clip = AudioFileClip(media_path)
        video_clip = None
    elif any(media_path.lower().endswith(ext) for ext in VIDEO_EXTENSIONS):
        video_clip = VideoFileClip(media_path)
        audio_clip = video_clip.audio
    else:
        raise ValueError(f"Formato no soportado: {media_path}")
    
    audio_clip.write_audiofile(output_wav)
    audio_clip.close()
    if video_clip:
        video_clip.close()

def transcribe_audio(wav_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data, language="es-ES")
        except sr.UnknownValueError:
            return "No se pudo entender el audio."
        except sr.RequestError:
            return "Error en el servicio de transcripción."
        

def process_file(file_path: str):
    temp_wav = file_path + ".wav"

    extract_audio(file_path, temp_wav)
    text = transcribe_audio(temp_wav)

    # limpiar wav
    if os.path.exists(temp_wav):
        os.remove(temp_wav)

    return text

def save_transcription(db: Session, filename: str, content: str, user_id: int) -> Transcription:
    record = Transcription(filename=filename, content=content, user_id=user_id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record