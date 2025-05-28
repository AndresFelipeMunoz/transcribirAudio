import os
from moviepy.editor import AudioFileClip  # Asegúrate de tener moviepy instalado
import speech_recognition as sr

# Ruta del archivo OGG
ogg_file_path = r"C:\Users\Anderson Parra\Desktop\Backup Andres Muñoz\transcribir audio\Audios\audio1.ogg"  # Asegúrate de que la ruta sea correcta
# Verificar si el archivo OGG existe
if not os.path.exists(ogg_file_path):
    print("El archivo OGG no se encontró en la ruta especificada.")
else:
    # Convertir OGG a WAV
    wav_file_path = r"C:\Users\Anderson Parra\Desktop\Backup Andres Muñoz\transcribir audio\audio.wav"
    
    # Convertir a WAV
    audio_clip = AudioFileClip(ogg_file_path)
    audio_clip.write_audiofile(wav_file_path)

    # Transcribir el audio WAV
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="es-ES")
            print("Transcripción:", text)
            
            # Guardar la transcripción en un archivo de texto
            output_path = r"C:\Users\Anderson Parra\Desktop\Backup Andres Muñoz\transcribir audio\transcripcion\transcripcion.txt"
            with open(output_path, "w", encoding="utf-8") as text_file:
                text_file.write(text)
            print("Transcripción guardada en 'transcripcion.txt'.")
            
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
        except sr.RequestError:
            print("No se pudo realizar la solicitud para transcribir el audio.")
