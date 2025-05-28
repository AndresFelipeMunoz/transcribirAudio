# transcribirAudio
Este script en Python convierte un archivo de audio en formato .ogg a .wav y luego transcribe su contenido a texto usando la API de reconocimiento de voz de Google. Finalmente, guarda la transcripción en un archivo .txt
##  Descripción del Proyecto

Este script en Python permite convertir un archivo de audio `.ogg` a formato `.wav` y transcribir su contenido a texto utilizando la API de reconocimiento de voz de Google.

### ¿Qué hace?

- Verifica si el archivo `.ogg` existe en la ruta especificada.  
- Convierte el audio `.ogg` a `.wav` con `moviepy`.  
- Transcribe el contenido del audio usando la librería `speech_recognition` en español (`es-ES`).  
- Guarda el texto transcrito en un archivo `.txt`.

Este proyecto es útil para automatizar tareas de transcripción de audios en español.
