from openai import OpenAI
import time, threading
from keys import openai_api_key

model="gpt-3.5-turbo"
client = OpenAI(api_key=openai_api_key)

while True:
  print()
  prompt = input("You: ")
  if prompt=="q":
    break
  messages = [{"role": "system", "content": "You are Alpha, Musham 's Personal assistant"},{"role": "user", "content": prompt}]
  response = client.chat.completions.create(model=model,messages= messages,max_tokens=30)
  print()
  output=response.choices[0].message.content
  print(f"ChatGPT: {output}")

