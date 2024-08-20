# pip install openai, speechrecognition
from openai import OpenAI
import speech_recognition as sr
import time, os, wave, subprocess

# Choosing OpenAI Model
model="gpt-4o-mini"

# Paste your OpenAI API Key here
from keys import openai_api_key
client = OpenAI(api_key=openai_api_key)

# Integration with OpenAI API
def ask(user_input):
  messages = [{"role": "system", "content": "You are Alpha, My Personal AI Assistant"},{"role": "user", "content": user_input}]
  response = client.chat.completions.create(model=model,messages= messages,max_tokens=40)
  output=response.choices[0].message.content
  return output

# OpenAI Text to Voice API
def tts(text_input):
  import warnings
  warnings.filterwarnings("ignore", category=DeprecationWarning)
  response = client.audio.speech.create(model="tts-1",voice="onyx",input=text_input)
  response.stream_to_file("response.mp3")
  subprocess.run(["termux-media-player", "play", "response.mp3"],capture_output=True, text=True, check=True)

# Wake Word Detection Function
def detect_wake_word():
  
  # Command
  command = ""
  ct = 0
  
  # Parameters
  file_path = "/data/data/com.termux/files/home/storage/music/Recordings/Standard Recordings/Standard recording 1.wav"
  chunk_duration = 3
  sample_rate = 44100
  
  recognizer = sr.Recognizer()
  last_processed_time = 0
  wake_word_count = 0
  
  while True:
    if os.path.exists(file_path):
      with wave.open(file_path, 'rb') as wf:
        total_duration = wf.getnframes() / sample_rate
        if total_duration > last_processed_time + chunk_duration:
          wf.setpos(int(last_processed_time * sample_rate))
          frames = wf.readframes(int(chunk_duration * sample_rate))
          chunk_file = 'chunk.wav'
          
          with wave.open(chunk_file, 'wb') as chunk_wf:
            chunk_wf.setnchannels(wf.getnchannels())
            chunk_wf.setsampwidth(wf.getsampwidth())
            chunk_wf.setframerate(sample_rate)
            chunk_wf.writeframes(frames)
            
          with sr.AudioFile(chunk_file) as source:
            audio = recognizer.record(source)
            #print(f"{last_processed_time}-{last_processed_time + chunk_duration}")
            
            try:
              transcript = recognizer.recognize_google(audio)
              
              if ct>0:
                command += transcript
                ct -= 1
                print("Command: " + command)
                output = ask(command)
                tts(output)
                print(f"Alpha: {output}")
                
              if "Alpha" in transcript:
                subprocess.run(["termux-media-player", "play", "sound.mp3"],capture_output=True, text=True, check=True)
                ct = 0
                command = ""
                wake_word_count += 1
                ct += 1
                command += transcript
                command += " "
                print(wake_word_count)

            except sr.UnknownValueError:
              if ct>0:
                ct -= 1
                print("Command: " + command)
                output = ask(command)
                tts(output)
                print(f"Alpha: {output}")
              #print("Audio Error")
            except sr.RequestError as e:
              print(f"Request Error {e}")
          os.remove(chunk_file)
          last_processed_time += chunk_duration
    time.sleep(1)

# Run the Detection
detect_wake_word()