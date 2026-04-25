import os
import tempfile
from moviepy import AudioFileClip, VideoFileClip
import speech_recognition as sr

# Extensiones soportadas
AUDIO_EXTENSIONS = ['.ogg', '.wav', '.mp3', '.flac', '.aac', '.m4a']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']

def extract_audio(media_path, output_wav):
    """Extrae audio de un archivo de audio o video y lo guarda como WAV."""
    if any(media_path.lower().endswith(ext) for ext in AUDIO_EXTENSIONS):
        # Es un archivo de audio
        audio_clip = AudioFileClip(media_path)
        video_clip = None
    elif any(media_path.lower().endswith(ext) for ext in VIDEO_EXTENSIONS):
        # Es un archivo de video
        video_clip = VideoFileClip(media_path)
        audio_clip = video_clip.audio
    else:
        raise ValueError(f"Formato no soportado: {media_path}")
    
    audio_clip.write_audiofile(output_wav)
    audio_clip.close()
    if video_clip:
        video_clip.close()

def transcribe_audio(wav_path):
    """Transcribe el audio WAV usando Google Speech Recognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="es-ES")
            return text
        except sr.UnknownValueError:
            return "No se pudo entender el audio."
        except sr.RequestError:
            return "No se pudo realizar la solicitud para transcribir el audio."

# Directorios
audios_dir = "Audios"
transcripcion_dir = "transcripcion"

# Crear directorio de transcripción si no existe
os.makedirs(transcripcion_dir, exist_ok=True)

# Procesar todos los archivos en Audios/
for filename in os.listdir(audios_dir):
    file_path = os.path.join(audios_dir, filename)
    if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in AUDIO_EXTENSIONS + VIDEO_EXTENSIONS):
        print(f"Procesando: {filename}")
        
        # Crear archivo WAV temporal
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
            temp_wav_path = temp_wav.name
        
        try:
            # Extraer audio
            extract_audio(file_path, temp_wav_path)
            
            # Transcribir
            transcription = transcribe_audio(temp_wav_path)
            
            # Guardar transcripción
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(transcripcion_dir, f"{base_name}.txt")
            with open(output_path, "w", encoding="utf-8") as text_file:
                text_file.write(transcription)
            print(f"Transcripción guardada en '{output_path}'.")
            
        except Exception as e:
            print(f"Error procesando {filename}: {e}")
        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_wav_path):
                os.unlink(temp_wav_path)

print("Proceso completado.")
