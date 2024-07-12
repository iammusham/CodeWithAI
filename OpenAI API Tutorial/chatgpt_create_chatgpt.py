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
  messages = [{"role": "system", "content": "Act as ChatGPT"},{"role": "user", "content": prompt}]
  response = client.chat.completions.create(model=model,messages= messages,max_tokens=30)
  output=response.choices[0].message.content
  print("\nChatGPT: ", end = '')
  for char in output:
    print(char, end='', flush=True)
    time.sleep(0.08)

