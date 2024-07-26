"""
Speech to Text using OpenAI Whisper Model
Text to Speech using OpenAI TTS Model
"""

"""
Requirements:
Python: (winget install python) for windows only
OpenAI Python Lib: (pip install openai)
Pathlib Python Lib: (pip install pathlib)
"""

from openai import OpenAI
from pathlib import Path

# Paste your OpenAI API key here!
client = OpenAI(api_key="your_openai_api_key")

# Audio file path
audio_file = "your_audio_file_path"

# Speech to text
audio_file = open(audio_file,'rb')
transcript = client.audio.transcriptions.create(model='whisper-1',file=audio_file, response_format='text')
print(transcript)

# Text to speech
speech_file_path = "voice.mp3"
response = client.audio.speech.create(model='tts-1', voice='shimmer', input=transcript)
response.stream_to_file(speech_file_path)
print("Audio Generated Successfully")
