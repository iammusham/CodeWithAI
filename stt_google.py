"""
Speech to text using Python SpeechRecognition with Google
"""

"""
Requirements:
Python: (winget install python) for windows only
SpeechRecognition Lib: (pip install SpeechRecognition)
"""
import speech_recognition as sr

# Audio File Path
audio_file = "your_audio_file_path"

r = sr.Recognizer()
with sr.AudioFile(audio_file) as source:
    audio = r.record(source)
try:
    transcript = r.recognize_google(audio)
except sr.UnknownValueError:
    transcript = "audio error"
except sr.RequestError as e:
    transcript = "Request error"
print(transcript)