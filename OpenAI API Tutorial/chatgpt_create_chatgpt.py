from openai import OpenAI
import time, threading
from keys import openai_api_key

client = OpenAI(api_key=openai_api_key)

while True:
  print()
  prompt = input("You: ")
  if prompt=="q":
    break
  response = client.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role": "system", "content": "Act as ChatGPT"},{"role": "user", "content": print}],max_tokens=40)
  print()
  output=response.choices[0].message.content
  print(f"ChatGPT: {output}")

