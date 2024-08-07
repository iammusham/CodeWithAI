from openai import OpenAI
import time

model="gpt-3.5-turbo"

# Paste your_openai_api_key here!
client = OpenAI(api_key="your_openai_api_key")

while True:
  print()
  user_input = input("You: ")
  if user_input=="q":
    break
  messages = [{"role": "system", "content": "Act as ChatGPT"},{"role": "user", "content": user_input}]
  response = client.chat.completions.create(model=model,messages= messages,max_tokens=60)
  output=response.choices[0].message.content
  print("\nChatGPT: ", end = '')
  for char in output:
    print(char, end='', flush=True)
    time.sleep(0.08)
  print()

